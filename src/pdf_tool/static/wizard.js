(() => {
  const byId = id => document.getElementById(id);
  const steps = [...document.querySelectorAll('[data-step]')];
  const progress = [...document.querySelectorAll('.wizard-progress li')];
  const form = byId('starterReview');
  const jobs = byId('starterJobs');
  const jobTemplate = byId('starterJob');
  const palette = byId('starterPalette');
  const layout = byId('starterLayout');
  const fieldInput = field => form.querySelector(`[name="${field}"]`);
  const saveButton = byId('starterSave');
  const reviewed = byId('starterReviewed');
  const personalFields = ['displayName', 'slug', 'headline', 'summary', 'email', 'phone', 'web', 'coverLetterNotes'];
  const jobFields = ['role', 'org', 'dates', 'summary'];
  const claimFields = ['skills', 'education'];
  const lines = value => value.split('\n').map(line => line.trim()).filter(Boolean);
  let options;
  let imported = {};
  let current = 0;

  function show(index) {
    current = index;
    steps.forEach((step, i) => {
      step.hidden = i !== index;
      step.classList.toggle('on', i === index);
    });
    progress.forEach((item, i) => {
      item.classList.toggle('on', i <= index);
      if (i === index) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
    steps[index].querySelector('h2').focus();
  }

  async function post(url, payload) {
    const response = await fetch(url, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.error || 'The local request failed.');
    return result;
  }

  async function loadOptions() {
    if (options) return;
    const response = await fetch('/api/starter-options', { cache: 'no-store' });
    if (!response.ok) throw new Error('Style choices could not load. Go back and try again.');
    const result = await response.json();
    if (!result.palettes.length) throw new Error('The installed palettes could not be found.');
    palette.replaceChildren(...result.palettes.map(item => new Option(item.label, item.id)));
    if (result.palettes.some(item => item.id === 'slate-ink')) palette.value = 'slate-ink';
    layout.replaceChildren(...Object.entries(result.layouts).map(([id, title]) => new Option(title, id)));
    options = result;
    showSwatches();
  }

  function showSwatches() {
    const selected = options.palettes.find(item => item.id === palette.value);
    for (const swatch of byId('starterSwatches').children) {
      swatch.style.setProperty('--draft-swatch', selected[swatch.dataset.swatch]);
    }
  }
  palette.addEventListener('change', showSwatches);

  function addJob(job = {}, focus = false) {
    const card = jobTemplate.content.firstElementChild.cloneNode(true);
    for (const field of jobFields) card.querySelector(`[name="${field}"]`).value = job[field] || '';
    card.querySelector('[name="bullets"]').value = (job.bullets || []).join('\n');
    card.querySelector('[data-remove-job]').addEventListener('click', () => {
      const next = card.nextElementSibling || card.previousElementSibling;
      card.remove();
      (next?.querySelector('input') || byId('addStarterJob')).focus();
    });
    jobs.append(card);
    if (focus) card.querySelector('input').focus();
  }

  function edit(draft) {
    imported = draft;
    form.reset();
    for (const field of personalFields) fieldInput(field).value = draft[field] || '';
    for (const field of claimFields) form.elements[field].value = (draft[field] || []).map(row => row.claim).join('\n');
    jobs.replaceChildren();
    for (const job of draft.jobs || []) addJob(job);
    const warnings = byId('starterWarnings');
    warnings.textContent = (draft.warnings || []).join(' ');
    warnings.hidden = !warnings.textContent;
    byId('reviewStatus').textContent = '';
    show(1);
  }

  function readDraft() {
    const draft = { ...imported };
    for (const field of personalFields) draft[field] = fieldInput(field).value.trim();
    for (const field of claimFields) draft[field] = lines(form.elements[field].value).map(claim => ({ claim }));
    draft.jobs = [...jobs.children].map(card => ({
      ...Object.fromEntries(jobFields.map(field => [field, card.querySelector(`[name="${field}"]`).value.trim()])),
      bullets: lines(card.querySelector('[name="bullets"]').value)
    }));
    return draft;
  }

  async function readFile(file, kind) {
    const bytes = new Uint8Array(await file.arrayBuffer());
    let data = '';
    for (let i = 0; i < bytes.length; i += 0x8000) {
      data += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
    }
    return { name: file.name, kind, contentBase64: btoa(data) };
  }

  byId('starterImport').addEventListener('click', async event => {
    const button = event.currentTarget;
    const status = byId('importStatus');
    const resume = byId('starterFiles').files[0];
    const letter = byId('starterLetter').files[0];
    const paste = byId('starterPaste').value.trim();
    button.disabled = true;
    byId('starterBlank').disabled = true;
    status.textContent = 'Reading locally…';
    try {
      if (!(resume || letter || paste)) throw new Error('Choose a résumé file or paste its text.');
      if (resume && paste) throw new Error('Choose either the résumé file or the pasted text.');
      await loadOptions();
      const size = (resume?.size || 0) + (letter?.size || 0) + new TextEncoder().encode(paste).length;
      if (size > options.maxImportBytes) throw new Error('Choose files totaling 2 MB or less, or paste the résumé text.');
      const files = [];
      if (resume) files.push(await readFile(resume, 'resume'));
      if (paste) files.push(await readFile(new File([paste], 'pasted-résumé.txt'), 'resume'));
      if (letter) files.push(await readFile(letter, 'cover-letter'));
      edit((await post('/api/import-resume', { files })).draft);
      status.textContent = '';
    } catch (error) {
      status.textContent = error.message;
    } finally {
      button.disabled = false;
      byId('starterBlank').disabled = false;
    }
  });

  byId('starterBlank').addEventListener('click', () => {
    byId('importStatus').textContent = '';
    edit({ source: 'Entered by the owner in the local wizard' });
  });
  byId('addStarterJob').addEventListener('click', () => addJob({}, true));
  fieldInput('displayName').addEventListener('change', () => {
    const slug = fieldInput('slug');
    if (!slug.value) {
      slug.value = fieldInput('displayName').value.toLowerCase().normalize('NFD')
        .replace(/\p{Mark}/gu, '').replace(/[^a-z0-9]+/g, '-').replace(/^[^a-z]+|-+$/g, '').slice(0, 32);
    }
  });
  document.querySelectorAll('[data-back]').forEach(button => button.addEventListener('click', () => show(current - 1)));
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const status = byId('reviewStatus');
    const button = event.submitter;
    const draft = readDraft();
    if (draft.jobs.some(job => !job.role || !job.org)) {
      status.textContent = 'Fill in the role and organization, or remove the job.';
      return;
    }
    if (!(draft.jobs.length || draft.skills.length || draft.education.length)) {
      status.textContent = 'Add at least one job, skill, or education entry.';
      return;
    }
    button.disabled = true;
    try {
      await loadOptions();
      status.textContent = '';
      byId('starterContinue').disabled = false;
      show(2);
    } catch (error) {
      status.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  });

  byId('starterContinue').addEventListener('click', () => {
    byId('starterStatus').textContent = '';
    byId('starterLinks').hidden = true;
    reviewed.checked = false;
    saveButton.disabled = true;
    show(3);
  });
  reviewed.addEventListener('change', () => { saveButton.disabled = !reviewed.checked; });
  saveButton.addEventListener('click', async () => {
    const status = byId('starterStatus');
    saveButton.disabled = true;
    reviewed.disabled = true;
    const back = steps[3].querySelector('[data-back]');
    back.disabled = true;
    status.textContent = 'Saving locally…';
    try {
      const result = await post('/api/save-starter', {
        draft: readDraft(),
        resumeOptions: {
          palette: palette.value,
          layout: layout.value,
          headingCase: byId('starterHeadingCase').value,
          resumeMaxPages: Number(byId('starterResumePages').value),
          reviewed: reviewed.checked
        }
      });
      byId('openStarterResume').href = '/?' + new URLSearchParams({ doc: result.resumePath });
      byId('openStarterVault').href = result.vaultHref;
      byId('starterLinks').hidden = false;
      status.textContent = 'Saved locally. Check page fit before sharing a PDF.';
      byId('openStarterResume').focus();
    } catch (error) {
      status.textContent = error.message;
      saveButton.disabled = false;
    } finally {
      reviewed.disabled = false;
      back.disabled = false;
    }
  });

  byId('voicePreview').addEventListener('click', async () => {
    const profile = byId('voiceProfile').value.trim();
    const card = byId('voiceCard');
    card.textContent = 'Loading…';
    try {
      const url = '/api/voice-card' + (profile ? '?' + new URLSearchParams({ profile }) : '');
      const payload = await (await fetch(url, { cache: 'no-store' })).json();
      card.textContent = payload.ok ? JSON.stringify(payload.card, null, 2) : payload.reason;
    } catch {
      card.textContent = 'Voice Seed preview is unavailable.';
    }
  });
})();
