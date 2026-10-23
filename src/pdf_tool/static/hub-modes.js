/* Shared application identity and real Hub modes. Independent of drawer wiring. */
(function () {
  const bar = document.querySelector('.hub-bar');
  const brandGroup = bar?.querySelector('.hub-brand-group');
  const brand = brandGroup?.querySelector('.hub-brand');
  const nav = bar?.querySelector('.hub-nav');
  if (!brand || !nav) return;

  brand.replaceChildren();
  const icon = document.createElement('img');
  icon.src = '/_hub/hub-app-icon.svg';
  icon.alt = '';
  icon.width = icon.height = 28;
  const name = document.createElement('span');
  name.className = 'hub-app-name';
  name.textContent = 'PDF Designer';
  brand.append(icon, name);
  brand.setAttribute('aria-label', 'PDF Designer — home and templates');
  brand.title = 'PDF Designer — home and templates';
  brandGroup.append(nav);
  nav.classList.add('hub-modes');
  nav.setAttribute('aria-label', 'Workspace modes');

  const modes = {
    '/': ['Library', 'Documents and templates', '<rect x="4" y="3" width="13" height="16" rx="2"/><path d="M8 7h5M8 11h5M8 15h3M17 7h3v14H7v-2"/>'],
    '/recipes': ['Recipes', 'Layout and palette templates', '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 10h18M11 10v11"/>'],
    '/vault': ['Vault', 'Skills and source-backed claims', '<path d="m12 3 8 4v6c0 4-8 8-8 8s-8-4-8-8V7z"/><path d="m8 12 3 3 5-6"/>'],
    '/wizard': ['Wizard', 'Create a resume workspace', '<path d="m4 20 11-11 3 3L7 23zM16 2v4M14 4h4M21 6v4M19 8h4M8 3v4M6 5h4"/>']
  };
  const currentPath = location.pathname.replace(/\/$/, '') || '/';
  const key = 'pdf-designer.hub.modeLocations';
  let remembered = {};
  try {
    const stored = JSON.parse(sessionStorage.getItem(key) || '{}');
    if (stored && typeof stored === 'object' && !Array.isArray(stored)) remembered = stored;
  } catch (_) {}
  const saveLocation = () => {
    remembered[currentPath] = location.pathname + location.search + location.hash;
    try { sessionStorage.setItem(key, JSON.stringify(remembered)); } catch (_) {}
  };
  for (const link of nav.querySelectorAll('a')) {
    const path = new URL(link.href).pathname;
    const mode = modes[path];
    if (!mode) continue;
    link.setAttribute('aria-label', mode[0]);
    link.title = `${mode[0]} — ${mode[1]}`;
    link.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">${mode[2]}</svg><span class="hub-mode-name">${mode[0]}</span>`;
    const active = currentPath === path;
    link.classList.toggle('on', active);
    if (active) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
    // Retain a selected Library document (?doc=...) when returning from another mode.
    const saved = remembered[path];
    if (typeof saved === 'string') {
      try {
        const url = new URL(saved, location.origin);
        if (url.origin === location.origin && url.pathname === path) link.href = url.pathname + url.search + url.hash;
      } catch (_) { /* Ignore invalid saved locations without disabling navigation. */ }
    }
    link.addEventListener('click', (event) => {
      saveLocation();
      if (active && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey && event.button === 0) event.preventDefault();
    });
  }
  window.addEventListener('pagehide', saveLocation);
})();
