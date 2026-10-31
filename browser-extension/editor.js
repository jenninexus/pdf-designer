'use strict';
const $ = id => document.getElementById(id);
const {editable, retained, validate, lockStorage} = HelperProfile;
const labels = {firstName:'First name',lastName:'Last name',email:'Email',phone:'Phone',city:'City',region:'State / province / region',country:'Country',postalCode:'Postal code',linkedin:'LinkedIn URL',website:'Website / portfolio URL',fullName:'Full name',currentTitle:'Current title',currentCompany:'Current company'};
let original = null, saved = null, stale = false, saving = false;
const rows = new Map();
const fingerprint = data => JSON.stringify(data ? validate(data) : null);
function error(e) { $('status').textContent = e.message || String(e); }
function draft() {
  const fields = {};
  for (const [key, row] of rows) if (row.check.checked && row.input.value.trim()) fields[key] = row.input.value;
  return validate({version:2,fields});
}
function update() {
  $('export').disabled = true;
  $('save').disabled = true;
  try {
    const next = draft();
    $('preview').textContent = JSON.stringify(next,null,2) + '\n';
    $('save').disabled = stale;
    $('export').disabled = stale || JSON.stringify(next) !== JSON.stringify(saved);
  } catch (e) { $('preview').textContent = e.message; }
}
function addRow(key, value, readOnly) {
  const row = document.createElement('div'); row.className = 'field';
  const label = document.createElement('label'); label.className = 'value'; label.textContent = labels[key];
  const input = document.createElement('input'); input.id = key; input.type = 'text'; input.maxLength = 500;
  input.autocomplete = 'off'; input.spellcheck = false; input.value = value || ''; input.readOnly = readOnly;
  label.append(input);
  const approval = document.createElement('label'); approval.className = 'approve';
  const check = document.createElement('input'); check.type = 'checkbox'; check.id = 'approve-' + key;
  check.checked = Boolean(value); approval.append(check, document.createTextNode(' Approve ' + labels[key]));
  input.addEventListener('input', () => { check.checked = false; update(); $('status').textContent = 'Value changed. Check it again to approve, then save.'; });
  check.addEventListener('change', update);
  row.append(label, approval); $(readOnly ? 'retained' : 'fields').append(row); rows.set(key,{input,check});
}
async function load() {
  await lockStorage(); const data = await chrome.storage.local.get('profile');
  // Validate before clearing drafts; malformed/unsupported stored data remains untouched.
  const profile = data.profile ? validate(data.profile) : null;
  original = fingerprint(data.profile); saved = profile; stale = false;
  rows.clear(); $('fields').replaceChildren(); $('retained').replaceChildren();
  for (const key of editable) addRow(key,profile?.fields[key],false);
  for (const key of retained) if (profile?.fields[key]) addRow(key,profile.fields[key],true);
  $('retained-section').hidden = !retained.some(k => profile?.fields[k]);
  $('version').textContent = profile?.version === 1 ? 'Version 1 retained. Save explicitly to migrate approved values to version 2; the original stays stored until then.' : 'Version 2 · approved fields only';
  update();
}
$('save').addEventListener('click',async () => { try {
  if (stale) throw Error('Saved profile changed in another helper page. Reload before saving.');
  const next = draft(); await lockStorage(); const current = await chrome.storage.local.get('profile');
  if (fingerprint(current.profile) !== original) { stale = true; update(); throw Error('Saved profile changed. Reload before saving.'); }
  saving = true; await chrome.storage.local.set({profile:next});
  original = JSON.stringify(next); saved = next; $('version').textContent = 'Version 2 · approved fields only'; update();
  $('status').textContent = 'Approved values saved locally. Unchecked drafts will disappear on reopen.';
} catch(e) {error(e);} finally {saving = false;} });
$('export').addEventListener('click',async () => { try {
  const next = draft(); await lockStorage(); const current = await chrome.storage.local.get('profile');
  if (stale || JSON.stringify(next) !== JSON.stringify(saved) || fingerprint(current.profile) !== original) throw Error('Save approved values before exporting, or reload if the saved profile changed.');
  const url = URL.createObjectURL(new Blob([JSON.stringify(next,null,2)+'\n'],{type:'application/json'}));
  const link = document.createElement('a'); link.href = url; link.download = 'approved-contact-profile.json';
  link.click(); setTimeout(() => URL.revokeObjectURL(url),1000);
  $('status').textContent = 'Exported approved JSON. Keep this personal file private.';
} catch(e) {error(e);} });
$('reload').addEventListener('click',() => load().then(() => { $('status').textContent = 'Saved values reloaded; unsaved drafts cleared.'; }).catch(error));
$('remove').addEventListener('click',async () => { try {
  await lockStorage(); saving = true; await chrome.storage.local.remove('profile'); await load();
  $('status').textContent = 'Saved profile removed. Editor drafts cleared; exported files are unchanged.';
} catch(e) {error(e);} finally {saving = false;} });
chrome.storage.onChanged.addListener((changes,area) => {
  if (area === 'local' && changes.profile && !saving) {
    stale = true; update(); $('status').textContent = 'Saved profile changed in another helper page. Reload before saving or exporting.';
  }
});
load().catch(error);
