'use strict';
// Shared by trusted extension pages and deterministic Node checks. No page or network access.
globalThis.HelperProfile = (() => {
  const editable = ['firstName','lastName','email','phone','city','region','country','postalCode','linkedin','website'];
  const retained = ['fullName','currentTitle','currentCompany'];
  const allowed = [...editable, ...retained];
  function validate(data) {
    if (!data || ![1,2].includes(data.version) || !data.fields || typeof data.fields !== 'object' || Array.isArray(data.fields)) throw Error('Expected a version 1 or 2 profile with a fields object.');
    if (Object.keys(data).some(k => !['version','fields'].includes(k)) || Object.keys(data.fields).some(k => !allowed.includes(k))) throw Error('Unknown profile field. Use only the documented approved fields.');
    const fields = {};
    for (const key of allowed.filter(k => Object.hasOwn(data.fields,k))) {
      const value = data.fields[key];
      const controls = data.version === 1 ? /[\x00-\x1f]/ : /[\x00-\x1f\x7f-\x9f\u2028\u2029]/;
      if (typeof value !== 'string' || value.length > 500 || controls.test(value)) throw Error(`${key}: use a single line of at most 500 characters.`);
      const text = value.trim();
      if (!text) continue;
      // v1 is read-compatible: strict validation/migration happens only on explicit editor save.
      if (data.version === 2) {
        if (key === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text)) throw Error('email: enter an email address without a display name.');
        if (['website','linkedin'].includes(key)) {
          let url;
          try { url = new URL(text); } catch { throw Error(`${key}: enter a complete http:// or https:// URL.`); }
          if (!['https:','http:'].includes(url.protocol) || !url.hostname || url.username || url.password || /\s/.test(text)) throw Error(`${key}: use an HTTP(S) URL without credentials or spaces.`);
        }
      }
      fields[key] = text;
    }
    if (!Object.keys(fields).length) throw Error('Approve at least one nonempty field, or remove the saved profile.');
    return {version:data.version, fields};
  }
  async function lockStorage() {
    if (!chrome.storage.local.setAccessLevel) throw Error('This browser cannot restrict extension storage. Update it before saving.');
    await chrome.storage.local.setAccessLevel({accessLevel:'TRUSTED_CONTEXTS'});
  }
  return Object.freeze({editable:Object.freeze(editable),retained:Object.freeze(retained),validate,lockStorage});
})();
if (typeof module !== 'undefined') module.exports = globalThis.HelperProfile;
