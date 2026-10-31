'use strict';
const {validate, lockStorage} = HelperProfile;
const $ = id => document.getElementById(id);
let profile = null, matches = [], tabId = null, documentId = null, tabUrl = null, reviewToken = null, reviewEpoch = 0;
async function load() { await lockStorage(); const data = await chrome.storage.local.get('profile'); profile = data.profile ? validate(data.profile) : null; $('profile').textContent = profile ? 'Review imported values: ' + Object.entries(profile.fields).map(([key, value]) => `${key}: ${value}`).join(' · ') : 'No profile imported.'; }
function clearReview() { reviewEpoch++; matches=[]; tabId=null; documentId=null; tabUrl=null; reviewToken=null; $('results').replaceChildren(); $('fill').hidden=true; }
function error(e) { $('status').textContent = e.message || String(e); }
$('file').addEventListener('change', async e => { try { const file=e.target.files[0]; if (!file) return; if (file.size > 50000) throw Error('Profile is too large.'); const next=validate(JSON.parse(await file.text())); await lockStorage(); await chrome.storage.local.set({profile:next}); clearReview(); await load(); $('status').textContent='Profile imported locally.'; } catch(err) { error(err); } finally { e.target.value=''; } });
$('remove').addEventListener('click', async () => { try { await lockStorage(); await chrome.storage.local.remove('profile'); clearReview(); await load(); $('status').textContent='Saved profile removed.'; } catch(err) {error(err);} });
// Runs in the isolated extension world on the current page only. No messages or storage access.
function inspectPage(action, selections, token) {
  const aliases = {firstName:['first name','given name','firstname','given-name'],lastName:['last name','family name','surname','lastname','family-name'],fullName:['full name','your name','name'],email:['email','email address'],phone:['phone','phone number','telephone','tel'],city:['city','city town'],region:['state','province','state province','region','address-level1'],country:['country','country name'],postalCode:['zip','zip code','postal code','postcode','postal-code'],linkedin:['linkedin','linkedin url','linkedin profile','linkedin profile url'],website:['website','portfolio','portfolio url','website url','personal website'],currentTitle:['current job title','current title','job title'],currentCompany:['current company','current employer','company name']};
  const normalize = s => (s || '').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  const risky = /\b(salary|compensation|pay|gender|sex|race|ethnicity|veteran|disability|age|birth|citizen|citizenship|visa|sponsor|authorization|authorisation|eligible|eligibility|password|social security|ssn|cover letter|resume|cv|address line|street)\b/;
  const controls = [...document.querySelectorAll('input')];
  function candidate(el, index) {
    if (el.disabled || el.readOnly || !['text','email','tel','url'].includes(el.type) || !el.getClientRects().length || getComputedStyle(el).visibility === 'hidden') return null;
    const labels = [...(el.labels || [])].map(x=>x.innerText).join(' ');
    const label = (labels || el.getAttribute('aria-label') || el.placeholder || el.name || el.id || '').trim();
    const clues = [labels,el.getAttribute('aria-label'),el.placeholder,el.name,el.id,el.autocomplete].filter(Boolean).map(normalize);
    if (!label || clues.some(c=>risky.test(c))) return null;
    const keys = Object.entries(aliases).filter(([,list])=>clues.some(c=>list.some(a=>normalize(a)===c))).map(([k])=>k);
    if (keys.length !== 1) return null;
    return {index,key:keys[0],label:label.slice(0,200),value:el.value,signature:clues.join('|')};
  }
  if (action === 'scan') {
    globalThis.__pdfHelperReview?.dispose();
    // Observe native navigation across isolated worlds without patching site methods.
    if (!globalThis.navigation?.addEventListener || document.visibilityState !== 'visible') throw Error('This page cannot support a guarded review.');
    const state = {token:crypto.randomUUID(), controls, forms:controls.map(el=>el.form),
      root:document.documentElement, url:location.href, created:performance.now(), wall:Date.now(), invalid:false};
    const listeners = [];
    const observer = new MutationObserver(() => invalidate());
    let timer;
    state.dispose = () => {
      observer.disconnect(); clearTimeout(timer);
      for (const [target,type,listener] of listeners) target.removeEventListener(type,listener);
    };
    function invalidate() { state.invalid = true; state.dispose(); }
    function listen(target,type,listener=invalidate) { target.addEventListener(type,listener); listeners.push([target,type,listener]); }
    // Conservative: any light-DOM mutation requires review again, even if reverted.
    observer.observe(document,{subtree:true,childList:true,characterData:true,attributes:true});
    listen(navigation,'navigate'); listen(navigation,'currententrychange');
    for (const type of ['popstate','hashchange','pagehide','pageshow']) listen(globalThis,type);
    listen(document,'visibilitychange',() => { if (document.visibilityState !== 'visible') invalidate(); });
    timer = setTimeout(invalidate,300000);
    state.fresh = () => {
      if (observer.takeRecords().length || performance.now()-state.created >= 300000 ||
          Date.now()-state.wall >= 300000 || Date.now() < state.wall || document.visibilityState !== 'visible' ||
          document.documentElement !== state.root || location.href !== state.url) invalidate();
      return !state.invalid;
    };
    globalThis.__pdfHelperReview = state;
    return {token:state.token,matches:controls.map(candidate).filter(Boolean)};
  }
  const state = globalThis.__pdfHelperReview;
  if (!state || state.token !== token || !state.fresh()) return {invalidated:true,filled:0,skipped:selections.length};
  let filled=0, skipped=0;
  for (const item of selections) {
    const el=controls[item.index], now=el && candidate(el,item.index);
    if (!state.fresh() || !now || state.controls[item.index] !== el || state.forms[item.index] !== el.form || now.key!==item.key || now.signature!==item.signature || now.value!==item.previous || (now.value && !item.overwrite)) { skipped++; continue; }
    const setter=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;
    setter.call(el,item.value); el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true})); filled++;
  }
  state.invalid = true; state.dispose(); // Single-use, including zero-fill attempts.
  return {filled,skipped};
}
$('scan').addEventListener('click', async () => {
  clearReview();
  const epoch = reviewEpoch;
  try {
    if (!profile) throw Error('Import a profile first.');
    const [tab] = await chrome.tabs.query({active:true,currentWindow:true});
    if (!tab || !tab.id) throw Error('No active page.');
    const [result] = await chrome.scripting.executeScript({target:{tabId:tab.id},func:inspectPage,args:['scan',[]]});
    if (epoch !== reviewEpoch) return;
    if (!result || typeof result.documentId !== 'string' || !result.documentId ||
        !result.result?.token || !Array.isArray(result.result.matches)) throw Error('This browser cannot bind the review to the current document.');
    tabId = tab.id; tabUrl = tab.url; documentId = result.documentId; reviewToken = result.result.token;
    matches = result.result.matches.filter(x=>profile.fields[x.key]);
    for (const m of matches) {
      const row = document.createElement('label'); row.className = 'field';
      const check = document.createElement('input'); check.type = 'checkbox';
      check.checked = !m.value && !['fullName','currentTitle','currentCompany'].includes(m.key);
      check.dataset.index = String(m.index); row.append(check);
      const content = document.createElement('span'); content.textContent = `${m.label} → ${profile.fields[m.key]}`; row.append(content);
      const note = document.createElement('small'); note.textContent = m.value ? `Currently: ${m.value} · check to overwrite` : 'Empty'; row.append(note);
      $('results').append(row);
    }
    $('fill').hidden = !matches.length;
    $('status').textContent = matches.length ? 'Check fields to fill. Existing values require an explicit check.' : 'No matching approved fields found on this page.';
  } catch (err) { if (epoch === reviewEpoch) { clearReview(); error(err); } }
});
$('fill').addEventListener('click', async () => {
  const epoch = reviewEpoch;
  try {
    const saved = await chrome.storage.local.get('profile');
    if (!profile || JSON.stringify(validate(saved.profile)) !== JSON.stringify(profile) || epoch !== reviewEpoch) throw Error('Profile changed. Review it again.');
    const [tab] = await chrome.tabs.query({active:true,currentWindow:true});
    if (!tab || tab.id!==tabId || tab.url!==tabUrl || !documentId || epoch !== reviewEpoch) throw Error('Page changed. Review it again.');
    const checked = new Set([...$('results').querySelectorAll('input:checked')].map(x=>Number(x.dataset.index)));
    const selected = matches.filter(x=>checked.has(x.index)).map(x=>({index:x.index,key:x.key,signature:x.signature,previous:x.value,overwrite:Boolean(x.value),value:profile.fields[x.key]}));
    if (!selected.length) throw Error('Select at least one field.');
    const [result] = await chrome.scripting.executeScript({target:{tabId,documentIds:[documentId]},func:inspectPage,args:['fill',selected,reviewToken]});
    if (!result || result.documentId!==documentId || !result.result) throw Error('Document changed. Review it again.');
    if (result.result.invalidated) throw Error('Review expired or page changed. Review it again.');
    const {filled,skipped} = result.result;
    clearReview(); $('status').textContent = `Filled ${filled}; skipped ${skipped} changed or unavailable fields. Review the page before submitting.`;
  } catch (err) { clearReview(); error(err); }
});
$("edit").addEventListener("click", () => chrome.runtime.openOptionsPage().catch(error));
chrome.storage.onChanged.addListener((changes, area) => { if (area === "local" && changes.profile) { clearReview(); load().catch(error); } });
load().catch(error);
