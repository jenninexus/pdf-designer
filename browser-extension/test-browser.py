"""Fictional-only integration for installed Chrome/Edge, in an isolated browser profile.

Run on the routed QA host's interactive desktop; requires Playwright and websocket-client.
Never points at an employer site or the user's browser profile. No substitute extension APIs.
"""
import argparse
import ctypes
import hashlib
import http.server
import json
from pathlib import Path
import shutil
import socket
import tempfile
import threading
import time
import urllib.request

from playwright.sync_api import sync_playwright
import websocket

ROOT = Path(__file__).resolve().parent


def wait_for(check, seconds=8):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        result = check()
        if result:
            return result
        time.sleep(.1)
    raise AssertionError('Timed out waiting for browser result')


def action(form, port):
    """Invoke the real browser action with an OS gesture on the owned fixture window."""
    form.bring_to_front()
    title = form.title()
    user = ctypes.windll.user32
    handles = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def visit(handle, _):
        text = ctypes.create_unicode_buffer(1024)
        user.GetWindowTextW(handle, text, 1024)
        if title in text.value and user.IsWindowVisible(handle):
            handles.append(handle)
        return True

    user.EnumWindows(visit, 0)
    assert len(handles) == 1, 'Refuse to type unless the owned QA window is unique'
    user.ShowWindow(handles[0], 9)
    user.SetForegroundWindow(handles[0])
    time.sleep(.3)
    assert user.GetForegroundWindow() == handles[0], 'Refuse to type into another window'
    for key in (0x11, 0x10, 0x59):
        user.keybd_event(key, 0, 0, 0)
    for key in (0x59, 0x10, 0x11):
        user.keybd_event(key, 0, 2, 0)
    # Let Playwright process the new action target before raw CDP attaches to it.
    form.wait_for_timeout(700)
    def targets():
        return json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list', timeout=3))
    target = wait_for(lambda: next((x for x in targets() if x['url'].endswith('/popup.html')), None))
    ws = websocket.create_connection(target['webSocketDebuggerUrl'], timeout=.15, suppress_origin=True)
    popup = Popup(ws,form)
    wait_for(lambda: popup.evaluate("Boolean(document.querySelector('#scan'))"))
    wait_for(lambda: 'Review imported values' in popup.text('#profile'))
    return popup


class Popup:
    def __init__(self, ws, form):
        self.ws, self.counter, self.form = ws, 0, form

    def call(self, method, params):
        self.form.wait_for_timeout(20)
        self.counter += 1
        self.ws.send(json.dumps({'id':self.counter,'method':method,'params':params}))
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            try:
                response = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                # New extension targets can await Playwright's attach/resume handshake.
                self.form.wait_for_timeout(50)
                continue
            if response.get('id') == self.counter:
                assert 'error' not in response, response
                return response['result']
        raise AssertionError('Timed out waiting for action CDP response')

    def evaluate(self, expression):
        result = self.call('Runtime.evaluate', {'expression':expression,'returnByValue':True})
        assert 'exceptionDetails' not in result, result
        return result['result'].get('value')

    def text(self, selector):
        return self.evaluate(f'document.querySelector({json.dumps(selector)}).textContent')

    def click(self, selector):
        literal = json.dumps(selector)
        self.evaluate(f'document.querySelector({literal}).scrollIntoView({{block:"center"}})')
        rect = self.evaluate(f'(()=>{{let r=document.querySelector({literal}).getBoundingClientRect();return {{x:r.x+r.width/2,y:r.y+r.height/2}}}})()')
        for kind in ('mousePressed','mouseReleased'):
            self.call('Input.dispatchMouseEvent',{'type':kind,**rect,'button':'left','clickCount':1})


def run(channel, work):
    print('START',channel,flush=True)
    work = work.resolve()
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args,directory=str(ROOT/'fixtures'),**kwargs)
    server = http.server.ThreadingHTTPServer(('127.0.0.1',0), handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    receipt = {'channel':channel,'fixtures':[],'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.suffix in ('.js','.css','.html','.json')}}
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0)); port = sock.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='helper-qa-',dir=work) as temp, sync_playwright() as p:
        # Python fixture checks can create __pycache__; Chrome refuses reserved _ names.
        # Load exact production bytes without Python caches or test-only files.
        extension = Path(temp)/'extension'; extension.mkdir()
        for name in ['manifest.json','profile.js','popup.js','popup.html','popup.css','editor.js','editor.html','editor.css']:
            shutil.copyfile(ROOT/name,extension/name)
        context = p.chromium.launch_persistent_context(str(Path(temp)/'profile'),channel=channel,headless=False,
            ignore_default_args=['--disable-extensions'], accept_downloads=True,
            args=['--no-first-run','--enable-unsafe-extension-debugging',f'--remote-debugging-port={port}','--remote-allow-origins=*'])
        try:
            cdp = context.browser.new_browser_cdp_session()
            ident = cdp.send('Extensions.loadUnpacked',{'path':str(extension)})['id']
            receipt['browser'] = cdp.send('Browser.getVersion')
            print('LOADED',receipt['browser']['product'],flush=True)
            base = f'chrome-extension://{ident}/'
            launcher = context.new_page(); launcher.goto(base+'popup.html')
            with context.expect_page() as opened:
                launcher.locator('#edit').click()
            editor = opened.value
            editor.wait_for_load_state(); launcher.close()
            editor.wait_for_selector('#firstName')
            assert editor.locator('#firstName').input_value() == ''
            assert not editor.locator('#approve-firstName').is_checked()
            assert editor.locator('#export').is_disabled()
            values = {'firstName':'Alex','lastName':'Example','email':'alex@example.com','phone':'+1 202 555 0142','website':'https://example.com'}
            for key,value in values.items():
                editor.locator('#'+key).fill(value)
                assert not editor.locator('#approve-'+key).is_checked()
                editor.locator('#approve-'+key).check()
            editor.locator('#save').click()
            editor.wait_for_function("() => document.querySelector('#status').textContent.startsWith('Approved values saved')")
            assert json.loads(editor.locator('#preview').inner_text()) == {'version':2,'fields':values}
            editor.screenshot(path=str(work/(channel+'-editor.png')),full_page=True)
            editor.close(); editor = context.new_page(); editor.goto(base+'editor.html'); editor.wait_for_selector('#firstName')
            assert editor.locator('#firstName').input_value() == 'Alex'
            assert editor.locator('#approve-firstName').is_checked()
            editor.locator('#firstName').fill('Updated')
            assert not editor.locator('#approve-firstName').is_checked()
            assert 'firstName' not in json.loads(editor.locator('#preview').inner_text())['fields']
            assert editor.locator('#export').is_disabled()
            editor.locator('#approve-firstName').check(); editor.locator('#save').click()
            editor.wait_for_function("() => !document.querySelector('#export').disabled")
            editor.reload(); editor.wait_for_selector('#firstName'); assert editor.locator('#firstName').input_value() == 'Updated'
            editor.locator('#approve-phone').uncheck(); editor.locator('#save').click()
            editor.wait_for_function("() => !document.querySelector('#export').disabled")
            editor.reload(); editor.wait_for_selector('#phone'); assert editor.locator('#phone').input_value() == ''
            editor.locator('#website').fill('javascript:alert(1)'); editor.locator('#approve-website').check()
            assert editor.locator('#save').is_disabled(); assert editor.locator('#export').is_disabled()
            editor.locator('#reload').click(); editor.wait_for_function("() => document.querySelector('#website').value==='https://example.com'")
            # Import v1 through the real import handler, preserve extra approved values without splitting names.
            legacy = {'version':1,'fields':{'fullName':'Alex Example','currentTitle':'Designer','currentCompany':'Fictional Studio','email':'alex@example.com','website':'https://example.com'}}
            popup = context.new_page(); popup.goto(base+'popup.html')
            popup.locator('#file').set_input_files({'name':'legacy.json','mimeType':'application/json','buffer':json.dumps(legacy).encode()})
            popup.wait_for_function("() => document.querySelector('#status').textContent==='Profile imported locally.'")
            editor.wait_for_function("() => document.querySelector('#save').disabled && document.querySelector('#status').textContent.includes('another helper page')")
            editor.locator('#reload').click(); editor.wait_for_function("() => document.querySelector('#fullName')!==null")
            assert editor.locator('#firstName').input_value() == '' and editor.locator('#lastName').input_value() == ''
            assert editor.evaluate("async()=> (await chrome.storage.local.get('profile')).profile") == legacy
            editor.locator('#save').click(); editor.wait_for_function("() => !document.querySelector('#export').disabled")
            migrated = editor.evaluate("async()=> (await chrome.storage.local.get('profile')).profile")
            assert migrated == {'version':2,'fields':legacy['fields']}
            print('EDITOR save, reopen, update, removal, migration passed',flush=True)
            with editor.expect_download() as download:
                editor.locator('#export').click()
            exported = Path(temp)/'export.json'; download.value.save_as(exported)
            assert json.loads(exported.read_text()) == migrated
            print('EXPORT round trip downloaded',flush=True)
            editor.locator('#remove').click(); editor.wait_for_function("() => document.querySelector('#fullName')===null")
            assert editor.evaluate("async()=> (await chrome.storage.local.get('profile')).profile ?? null") is None
            popup.locator('#file').set_input_files(str(exported))
            popup.wait_for_function("() => document.querySelector('#status').textContent==='Profile imported locally.'")
            assert popup.evaluate("async()=> (await chrome.storage.local.get('profile')).profile") == migrated
            # Invalid import is atomic and does not discard saved values.
            popup.locator('#file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"version":2,"fields":{"salary":"secret"}}'})
            popup.wait_for_function("() => document.querySelector('#status').textContent.includes('Unknown profile field')")
            assert popup.evaluate("async()=> (await chrome.storage.local.get('profile')).profile") == migrated
            # Import a fictional explicit v2 profile for actual activeTab action tests.
            popup.locator('#file').set_input_files({'name':'contact.json','mimeType':'application/json','buffer':json.dumps({'version':2,'fields':values}).encode()})
            popup.wait_for_function("() => document.querySelector('#status').textContent==='Profile imported locally.'")
            popup.close(); editor.close()
            receipt['editor'] = 'approval, save/reopen, update, per-field removal, URL rejection, v1 preservation/migration, export/import, invalid-import preservation, full removal passed'
            for fixture in ['associated-labels','wrapped-labels','aria-labels']:
                print('ACTION',fixture,flush=True)
                store = context.new_page(); store.goto(base+'editor.html'); store.wait_for_selector('#firstName')
                form = context.new_page(); form.goto(f'http://127.0.0.1:{server.server_port}/{fixture}.html')
                ui = action(form,port)
                try:
                    ui.click('#scan'); wait_for(lambda: ui.evaluate("document.querySelectorAll('#results input').length===5"))
                    assert ui.evaluate("document.querySelectorAll('#results input:checked').length") == 4
                    assert not ui.evaluate("document.querySelector('#results input[data-index=\"2\"]').checked")
                    ui.click('#fill'); wait_for(lambda: ui.text('#status').startswith('Filled 4;'))
                    actual = form.locator('form input').evaluate_all('(els)=>els.slice(0,5).map(x=>x.value)')
                    assert actual == ['Alex','Example','existing@example.org',values['phone'],values['website']], actual
                    assert form.evaluate('fixtureEvents') == {'input':4,'change':4,'submits':0,'files':0}
                    ui.click('#scan'); wait_for(lambda: ui.evaluate("document.querySelectorAll('#results input').length===5"))
                    ui.click('#results input[data-index="2"]'); ui.click('#fill')
                    wait_for(lambda: form.locator('input[type=email]').input_value() == 'alex@example.com')
                    form.evaluate("document.querySelector('form input').value=''")
                    ui.click('#scan'); wait_for(lambda: ui.evaluate("document.querySelectorAll('#results input').length===5"))
                    form.evaluate("let el=document.querySelector('form input');el.replaceWith(el.cloneNode(true))")
                    ui.click('#fill'); wait_for(lambda: ui.text('#status').startswith('Filled 0; skipped 1'))
                    ui.click('#scan'); wait_for(lambda: ui.evaluate("document.querySelectorAll('#results input').length===5"))
                    store.evaluate('(profile)=>chrome.storage.local.set({profile})',{'version':2,'fields':{**values,'firstName':'Changed'}})
                    wait_for(lambda: ui.evaluate("document.querySelector('#fill').hidden && document.querySelectorAll('#results input').length===0"))
                    store.evaluate('(profile)=>chrome.storage.local.set({profile})',{'version':2,'fields':values})
                    wait_for(lambda: 'Alex' in ui.text('#profile'))
                    ui.click('#scan'); wait_for(lambda: ui.evaluate("document.querySelectorAll('#results input').length===5"))
                    form.evaluate("history.pushState({},'', '?step=changed')")
                    try:
                        ui.click('#fill'); wait_for(lambda: 'Page changed' in ui.text('#status'))
                        url_change = 'Page changed: review required'
                    except websocket.WebSocketConnectionClosedException:
                        # Some browsers dismiss the real action when the tab URL changes.
                        assert form.locator('form input').first.input_value() == ''
                        url_change = 'browser dismissed action on URL change; no fill'
                    assert form.locator('input[type=file]').evaluate('(el)=>el.files.length') == 0
                    assert form.evaluate('fixtureEvents.submits===0 && fixtureEvents.files===0')
                    if fixture == 'aria-labels':
                        assert form.locator('#ambiguous').input_value() == ''
                        assert form.frame_locator('iframe').locator('#frame-first').input_value() == ''
                    receipt['fixtures'].append({'name':fixture,'result':'real action: 5 matches, empty-only defaults, consent overwrite, native events, replaced-control rejection, profile-change invalidation, zero submits/uploads','url_change':url_change})
                finally:
                    ui.ws.close(); form.close(); store.close()
                popup = context.new_page(); popup.goto(base+'popup.html'); popup.locator('#remove').click()
                popup.wait_for_function("() => document.querySelector('#status').textContent==='Saved profile removed.'")
                assert 'No profile imported' in popup.locator('#profile').inner_text(); popup.close()
                if fixture != 'aria-labels':
                    popup = context.new_page(); popup.goto(base+'popup.html'); popup.locator('#file').set_input_files({'name':'contact.json','mimeType':'application/json','buffer':json.dumps({'version':2,'fields':values}).encode()})
                    popup.wait_for_function("() => document.querySelector('#status').textContent==='Profile imported locally.'"); popup.close()
        finally:
            context.close(); server.shutdown(); server.server_close()
    receipt['cleanup'] = 'owned context closed, temporary profile/export removed'
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--channel',required=True,choices=['chrome','msedge'])
    parser.add_argument('--work-dir',type=Path,required=True)
    args = parser.parse_args(); args.work_dir.mkdir(parents=True,exist_ok=True)
    result = run(args.channel,args.work_dir)
    (args.work_dir/(args.channel+'-receipt.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
