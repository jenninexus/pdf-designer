'use strict';
// Run with node browser-extension/test-helper.cjs; no browser, profile, or network required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, 'popup.js'), 'utf8');
const functionSource = source.slice(source.indexOf('function inspectPage('), source.indexOf("$('scan').addEventListener"));
class Input {
  constructor(label, value = '', type = 'text') { this.labels=[{innerText:label}]; this._value=value; this.type=type; this.disabled=false; this.readOnly=false; this.name=''; this.id=''; this.autocomplete=''; this.events=[]; }
  get value() { return this._value; }
  set value(v) { this._value=v; }
  getClientRects() { return [1]; }
  getAttribute() { return null; }
  dispatchEvent(e) { this.events.push(e.type); }
}
const inputs = [new Input('First name'), new Input('Email address','old@example.com','email'), new Input('Salary'), new Input('Resume','','file'), new Input('Work authorization')];
const context = {document:{querySelectorAll:()=>inputs}, HTMLInputElement:Input, getComputedStyle:()=>({visibility:'visible'}), Event:class { constructor(type) {this.type=type;} }};
vm.createContext(context); vm.runInContext(functionSource,context);
const scan = context.inspectPage('scan',[]);
assert.deepEqual(Array.from(scan,x=>x.key),['firstName','email']);
const first = scan[0];
const result = context.inspectPage('fill',[{...first,previous:first.value,value:'Alex',overwrite:false}]);
assert.equal(result.filled,1); assert.equal(inputs[0].value,'Alex'); assert.deepEqual(inputs[0].events,['input','change']);
const email = scan[1];
assert.equal(context.inspectPage('fill',[{...email,previous:email.value,value:'new@example.com',overwrite:false}]).skipped,1);
assert.equal(inputs[1].value,'old@example.com');
assert.equal(context.inspectPage('fill',[{...email,previous:email.value,value:'new@example.com',overwrite:true}]).filled,1);
assert.equal(inputs[1].value,'new@example.com');
assert.equal(context.inspectPage('fill',[{...email,previous:email.value,value:'again@example.com',overwrite:true}]).skipped,1);
const manifest = JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'manifest.json'),'utf8').replace(/^\uFEFF/,''));
assert.deepEqual(manifest.permissions.sort(),['activeTab','scripting','storage']);
assert.equal(manifest.host_permissions,undefined); assert.equal(manifest.content_scripts,undefined);
assert.doesNotMatch(source,/\.submit\s*\(|requestSubmit\s*\(|sendMessage\s*\(/);
assert.match(source,/TRUSTED_CONTEXTS/);
assert.match(source,/documentIds:\[documentId\]/);
assert.match(source,/result\.documentId!==documentId/);
assert.match(source,/tab\.url!==tabUrl/);
assert.match(source,/\['fullName','currentTitle','currentCompany'\]\.includes\(m\.key\)/);
console.log('Helper checks passed: mapping, sensitive exclusion, events, overwrite, stale fields, permissions and no submit.');
