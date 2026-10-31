'use strict';
// Run with node browser-extension/test-helper.cjs; no browser, profile, or network required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, 'popup.js'), 'utf8');
const functionSource = source.slice(source.indexOf('function inspectPage('), source.indexOf("$('scan').addEventListener"));
// Minimal event/observer model for deterministic invalidation and queued-record checks.
class Target {
  constructor() { this.handlers = new Map(); }
  addEventListener(type,fn) { if (!this.handlers.has(type)) this.handlers.set(type,new Set()); this.handlers.get(type).add(fn); }
  removeEventListener(type,fn) { this.handlers.get(type)?.delete(fn); }
  dispatchEvent(e) { for (const fn of this.handlers.get(e.type) || []) fn(e); }
}
class Input {
  constructor(label, value = '', type = 'text') { this.labels=[{innerText:label}]; this._value=value; this.type=type; this.disabled=false; this.readOnly=false; this.name=''; this.id=''; this.autocomplete=''; this.events=[]; this.form={}; }
  get value() { return this._value; }
  set value(v) { this._value=v; }
  getClientRects() { return [1]; }
  getAttribute() { return null; }
  dispatchEvent(e) { this.events.push(e.type); this.onEvent?.(e); }
}
function setup() {
  const inputs = [new Input('First name'), new Input('Email address','old@example.com','email'), new Input('Salary'), new Input('Resume','','file'), new Input('Work authorization')];
  let observer, clock=0, uuid=0, timeout;
  const doc=Object.assign(new Target(),{querySelectorAll:()=>inputs,visibilityState:'visible',documentElement:{}});
  class Observer {
    constructor(callback) { this.callback=callback; this.records=[]; observer=this; }
    observe() { this.connected=true; }
    disconnect() { this.connected=false; this.records=[]; }
    takeRecords() { return this.records.splice(0); }
  }
  const context=Object.assign(new Target(),{document:doc,navigation:new Target(),location:{href:'https://example.test/form'},crypto:{randomUUID:()=>String(++uuid)},
    performance:{now:()=>clock},Date:{now:()=>clock},setTimeout:fn=>{timeout=fn;return 1;},clearTimeout:()=>{},MutationObserver:Observer,
    HTMLInputElement:Input,getComputedStyle:()=>({visibility:'visible'}),Event:class { constructor(type) {this.type=type;} }});
  vm.createContext(context); vm.runInContext(functionSource,context);
  const scan=()=>context.inspectPage('scan',[]);
  const fill=(r,index=0,overwrite=false)=>context.inspectPage('fill',[{...r.matches[index],previous:r.matches[index].value,value:'Alex',overwrite}],r.token);
  return {context,inputs,doc,scan,fill,mutate:()=>observer.records.push({type:'childList'}),expire:()=>{clock=300000;},timer:()=>timeout()};
}
let env=setup(), review=env.scan();
assert.deepEqual(Array.from(review.matches,x=>x.key),['firstName','email']);
assert.equal(env.fill(review).filled,1); assert.deepEqual(env.inputs[0].events,['input','change']);
assert.equal(env.fill(review).invalidated,true,'single-use token');
env=setup(); review=env.scan(); assert.equal(env.fill(review,1).skipped,1); assert.equal(env.inputs[1].value,'old@example.com');
review=env.scan(); assert.equal(env.fill(review,1,true).filled,1);
for (const [name,change] of Object.entries({
  queuedMutation:e=>e.mutate(), expiry:e=>e.expire(), timeout:e=>e.timer(),
  navigate:e=>e.context.navigation.dispatchEvent({type:'navigate'}), entryChange:e=>e.context.navigation.dispatchEvent({type:'currententrychange'}),
  popstate:e=>e.context.dispatchEvent({type:'popstate'}), hashchange:e=>e.context.dispatchEvent({type:'hashchange'}),
  pagehide:e=>e.context.dispatchEvent({type:'pagehide'}), pageshow:e=>e.context.dispatchEvent({type:'pageshow'}),
  hidden:e=>{e.doc.visibilityState='hidden';e.doc.dispatchEvent({type:'visibilitychange'});e.doc.visibilityState='visible';},
  root:e=>{e.doc.documentElement={};}, url:e=>{e.context.location.href+='?changed';}
})) {
  env=setup(); review=env.scan(); change(env);
  assert.equal(env.fill(review).invalidated,true,name); assert.equal(env.inputs[0].value,'',name);
  console.log('Blocked:',name);
}
for (const [name,change] of Object.entries({replacement:e=>{e.inputs[0]=new Input('First name');},form:e=>{e.inputs[0].form={};},value:e=>{e.inputs[0].value='changed';},signature:e=>{e.inputs[0].labels[0].innerText='Last name';}})) {
  env=setup(); review=env.scan(); change(env); assert.equal(env.fill(review).skipped,1,name);
}
env=setup(); review=env.scan(); env.scan(); assert.equal(env.fill(review).invalidated,true,'superseded token');
env=setup(); env.context.navigation=null; assert.throws(()=>env.scan(),/guarded review/);
// A framework mutating semantics in response to the first input blocks later writes.
env=setup(); review=env.scan(); env.inputs[0].onEvent=()=>env.mutate();
const batch=env.context.inspectPage('fill',review.matches.map(x=>({...x,previous:x.value,value:'Alex',overwrite:true})),review.token);
assert.equal(batch.filled,1); assert.equal(batch.skipped,1); assert.equal(env.inputs[1].value,'old@example.com');
const manifest = JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'manifest.json'),'utf8').replace(/^\uFEFF/,''));
assert.deepEqual(manifest.permissions.sort(),['activeTab','scripting','storage']);
assert.equal(manifest.host_permissions,undefined); assert.equal(manifest.content_scripts,undefined);
assert.deepEqual(manifest.options_ui,{page:'editor.html',open_in_tab:true});
for (const name of ['popup.js','profile.js','editor.js']) {
  const production = fs.readFileSync(require('node:path').join(__dirname,name),'utf8');
  assert.doesNotMatch(production,/fetch\s*\(|XMLHttpRequest|WebSocket\s*\(|\.submit\s*\(|requestSubmit\s*\(|sendMessage\s*\(/);
}
assert.doesNotMatch(fs.readFileSync(require('node:path').join(__dirname,'editor.js'),'utf8'),/chrome\.scripting|inspectPage/,'editor cannot fill a page');
assert.doesNotMatch(source,/\.submit\s*\(|requestSubmit\s*\(|sendMessage\s*\(/);
assert.match(fs.readFileSync(require('node:path').join(__dirname,'profile.js'),'utf8'),/TRUSTED_CONTEXTS/);
assert.match(source,/documentIds:\[documentId\]/);
assert.match(source,/result\.documentId!==documentId/);
assert.match(source,/tab\.url!==tabUrl/);
assert.match(source,/\['fullName','currentTitle','currentCompany'\]\.includes\(m\.key\)/);
console.log('Helper checks passed: mapping, sensitive exclusion, events, overwrite, stale fields, permissions and no submit.');
