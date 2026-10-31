"""Fictional-only integration for installed Chrome/Edge, in an isolated browser profile.

Run on the authorized QA host's interactive desktop; requires Playwright.
Never points at an employer site or the user's browser profile. No substitute extension APIs.
"""
import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import tempfile
import threading
import time

from playwright.sync_api import sync_playwright, Error as PlaywrightError

ROOT = Path(__file__).resolve().parent


def wait_for(check, seconds=8):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        result = check()
        if result:
            return result
        time.sleep(.1)
    raise AssertionError('Timed out waiting for browser result')


def action(form, extension_id):
    """Run the browser's actual default action on the owned fixture tab, granting activeTab."""
    previous_pages = set(form.context.pages)
    form.bring_to_front()
    browser_session = form.context.browser.new_browser_cdp_session()
    try:
        targets = browser_session.send('Target.getTargets',{'filter':[{'type':'tab','exclude':False},{'exclude':True}]})['targetInfos']
        tabs = [target for target in targets if target['url'] == form.url]
        assert len(tabs) == 1, ('Expected one owned fixture tab target',targets)
        target_id = tabs[0]['targetId']
        browser_session.send('Extensions.triggerAction',{'id':extension_id,'targetId':target_id})
    finally:
        browser_session.detach()
    def action_page():
        form.wait_for_timeout(50)
        return next((page for page in form.context.pages if page not in previous_pages and page.url.endswith('/popup.html')), None)
    page = wait_for(action_page)
    page.wait_for_selector('#scan',timeout=60000)
    popup = Popup(page)
    page.wait_for_function("() => document.querySelector('#profile').textContent.includes('Review imported values')")
    return popup


class Popup:
    def __init__(self, page):
        self.page = page

    def close(self):
        if not self.page.is_closed(): self.page.close()

    def evaluate(self, expression):
        # Function callbacks preserve the extension's strict CSP and follow its live frame.
        return self.page.evaluate(f'() => ({expression})')

    def text(self, selector):
        return self.evaluate(f'document.querySelector({json.dumps(selector)}).textContent')

    def click(self, selector):
        self.page.locator(selector).click(timeout=10000)


def review_scenarios(context, base, server_port, extension_id, receipt):
    receipt['invalidation'] = []
    store = context.new_page(); store.goto(base+'editor.html'); store.wait_for_selector('#firstName')
    form = context.new_page(); form.goto(f'http://127.0.0.1:{server_port}/review-transitions.html')
    markup = form.locator('body').inner_html()
    ui = None
    cases = ['push-same-url','replace-same-url','entry-state','heading','step','form-action',
             'form-id','form-replacement','control-replacement','control-move','form-owner',
             'reverted-dom','label','disabled','readonly','value','event-mutation',
             'invisible-state','history-back','history-forward','hash','url','reload','navigate','tab-hidden','expired']
    try:
        for kind in cases:
            print('REVIEW START',kind,flush=True)
            # Reset fictional light DOM and counters without executing new scripts or replacing
            # the document. Reuse the real action until browser navigation dismisses it.
            form.evaluate("""(markup) => {
                document.body.innerHTML=markup;
                fixtureEvents={input:0,change:0,submits:0,files:0};
                history.replaceState({},'', '/review-transitions.html');
            }""",markup)
            if kind in ['history-back','history-forward']:
                form.evaluate("history.pushState({step:1},'',location.href)")
                if kind == 'history-forward':
                    form.evaluate('history.back()'); form.wait_for_timeout(150)
            if ui is None or ui.page.is_closed(): ui = action(form,extension_id)
            other = None
            try:
                ui.click('#scan')
                wait_for(lambda: ui.evaluate("document.querySelectorAll('#results input').length===2"))
                if kind == 'event-mutation': ui.click('#results input[data-index="1"]')
                if kind == 'expired':
                    clock = context.new_cdp_session(form)
                    clock.send('Emulation.setVirtualTimePolicy',{'policy':'advance','budget':300001})
                    form.wait_for_timeout(250)
                    clock.detach()
                elif kind == 'tab-hidden':
                    other = context.new_page(); other.goto('about:blank'); other.bring_to_front()
                    form.wait_for_timeout(150); form.bring_to_front()
                elif kind in ['history-back','history-forward']:
                    form.evaluate('history.back()' if kind == 'history-back' else 'history.forward()')
                    form.wait_for_timeout(150)
                elif kind in ['reload','navigate']:
                    with form.expect_navigation(wait_until='load'):
                        form.evaluate('(kind)=>transition(kind)',kind)
                    form.wait_for_function("() => typeof transition==='function'")
                else:
                    form.evaluate('(kind)=>transition(kind)',kind)
                dismissed = False
                try:
                    ui.click('#fill')
                    if kind in ['invisible-state','event-mutation','value']:
                        wait_for(lambda: ui.text('#status').startswith('Filled '))
                    else:
                        wait_for(lambda: 'Review it again' in ui.text('#status') or ui.evaluate("document.querySelector('#fill').hidden"))
                except PlaywrightError:
                    if not ui.page.is_closed(): raise
                    dismissed = True
                first = form.locator('#first_name').input_value()
                expected = 'Alex' if kind in ['invisible-state','event-mutation'] else ('Other person' if kind == 'value' else '')
                assert first == expected, (kind,first,expected)
                assert form.locator('#email').input_value() == 'existing@example.org', kind
                assert form.locator('input[type=file]').evaluate('(el)=>el.files.length') == 0, kind
                events = form.evaluate('fixtureEvents')
                assert events['submits'] == 0 and events['files'] == 0, (kind,events)
                if kind not in ['invisible-state','event-mutation']:
                    assert events['input'] == 0 and events['change'] == 0, (kind,events)
                if not dismissed:
                    assert ui.evaluate("document.querySelector('#fill').hidden"), kind
                    if kind in ['push-same-url','replace-same-url','heading','form-replacement','control-replacement','expired']:
                        ui.click('#scan'); wait_for(lambda: ui.evaluate("document.querySelectorAll('#results input').length===2"))
                        ui.click('#fill'); wait_for(lambda: form.locator('#first_name').input_value() == 'Alex')
                result = {'case':kind,'status':'dismissed safely' if dismissed else 'checked by actual action','before_fresh_review':first,'events':events}
                receipt['invalidation'].append(result)
                print('REVIEW',kind,result['status'],flush=True)
            finally:
                if other: other.close()
    finally:
        if ui: ui.close()
        form.close(); store.close()


def run(channel, work, headless=False):
    print('START',channel,flush=True)
    # Extension action targets are classified as "other" on the browser protocol.
    # Opt this isolated QA driver into managing them instead of racing a raw debugger.
    os.environ['PW_CHROMIUM_ATTACH_TO_OTHER'] = '1'
    work = work.resolve()
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args,directory=str(ROOT/'fixtures'),**kwargs)
    server = http.server.ThreadingHTTPServer(('127.0.0.1',0), handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    receipt = {'channel':channel,'headless':headless,'action':'native Extensions.triggerAction on a tab target','fixtures':[],'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.suffix in ('.js','.css','.html','.json')}}
    with tempfile.TemporaryDirectory(prefix='helper-qa-',dir=work) as temp, sync_playwright() as p:
        # Python fixture checks can create __pycache__; Chrome refuses reserved _ names.
        # Load exact production bytes without Python caches or test-only files.
        extension = Path(temp)/'extension'; extension.mkdir()
        for name in ['manifest.json','profile.js','popup.js','popup.html','popup.css','editor.js','editor.html','editor.css']:
            shutil.copyfile(Path(os.environ['HELPER_QA_BASELINE_POPUP']) if name == 'popup.js' and os.environ.get('HELPER_QA_BASELINE_POPUP') else ROOT/name,extension/name)
        context = p.chromium.launch_persistent_context(str(Path(temp)/'profile'),channel=channel,headless=headless,
            ignore_default_args=['--disable-extensions'], accept_downloads=True,
            args=['--no-first-run','--enable-unsafe-extension-debugging'])
        context.on('page',lambda page: page.on('pageerror',lambda error: print('PAGEERROR',page.url,str(error),flush=True)))
        try:
            cdp = context.browser.new_browser_cdp_session()
            ident = cdp.send('Extensions.loadUnpacked',{'path':str(extension)})['id']
            receipt['staged_hashes'] = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in extension.iterdir()}
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
            review_scenarios(context, base, server.server_port, ident, receipt)
            for fixture in ['associated-labels','wrapped-labels','aria-labels']:
                print('ACTION',fixture,flush=True)
                store = context.new_page(); store.goto(base+'editor.html'); store.wait_for_selector('#firstName')
                form = context.new_page(); form.goto(f'http://127.0.0.1:{server.server_port}/{fixture}.html')
                ui = action(form,ident)
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
                    ui.click('#fill'); wait_for(lambda: 'Review it again' in ui.text('#status'))
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
                    except PlaywrightError:
                        if not ui.page.is_closed(): raise
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
                    ui.close(); form.close(); store.close()
                popup = context.new_page(); popup.goto(base+'popup.html'); popup.locator('#remove').click()
                popup.wait_for_function("() => document.querySelector('#status').textContent==='Saved profile removed.'")
                assert 'No profile imported' in popup.locator('#profile').inner_text(); popup.close()
                if fixture != 'aria-labels':
                    popup = context.new_page(); popup.goto(base+'popup.html'); popup.locator('#file').set_input_files({'name':'contact.json','mimeType':'application/json','buffer':json.dumps({'version':2,'fields':values}).encode()})
                    popup.wait_for_function("() => document.querySelector('#status').textContent==='Profile imported locally.'"); popup.close()
        except Exception as error:
            print('FAILURE',repr(error),flush=True)
            for page in context.pages:
                try:
                    print('FAILURE DOCUMENT',page.url,page.locator('body').inner_text(timeout=2000)[:2000],flush=True)
                except PlaywrightError:
                    print('FAILURE DOCUMENT UNAVAILABLE',page.url,flush=True)
            raise
        finally:
            context.close(); server.shutdown(); server.server_close()
    receipt['cleanup'] = 'owned context closed, temporary profile/export removed'
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--channel',required=True,choices=['chrome','msedge'])
    parser.add_argument('--work-dir',type=Path,required=True)
    parser.add_argument('--headless',action='store_true',help='Use the installed browser without focus-sensitive desktop bubbles; still invokes its real default action.')
    args = parser.parse_args(); args.work_dir.mkdir(parents=True,exist_ok=True)
    result = run(args.channel,args.work_dir,args.headless)
    (args.work_dir/(args.channel+'-receipt.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
