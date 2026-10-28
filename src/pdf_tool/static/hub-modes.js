/* Shared application identity and real Hub modes. Independent of drawer wiring. */
(function () {
  const bar = document.querySelector('.hub-bar');
  const brandGroup = bar?.querySelector('.hub-brand-group');
  const brand = brandGroup?.querySelector('.hub-brand');
  const nav = bar?.querySelector('.hub-nav');
  if (!brand || !nav) return;

  brand.replaceChildren();
  const icon = document.createElement('img');
  icon.src = '/_hub/hub-app-icon.png';
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
    '/': ['Library', 'Documents and templates', 'file-lines'],
    '/recipes': ['Recipes', 'Layout and palette templates', 'table-columns'],
    '/vault': ['Vault', 'Skills and source-backed claims', 'shield-halved'],
    '/wizard': ['Wizard', 'Create a resume workspace', 'wand-magic-sparkles']
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
    link.innerHTML = `<span class="hub-fa-icon fa-${mode[2]}" aria-hidden="true"></span><span class="hub-mode-name">${mode[0]}</span>`;
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
  // Desktop Support lives beside actions; compact layouts keep it in the existing drawer.
  const support = document.querySelector('.hub-drawer .hub-support');
  const pin = bar.querySelector('.hub-bar-pin');
  if (support && pin) {
    const menu = document.createElement('details');
    menu.className = 'hub-more hub-support-menu';
    const summary = document.createElement('summary');
    summary.textContent = 'Support';
    summary.setAttribute('aria-label', 'Support PDF Designer');
    const panel = document.createElement('div');
    panel.className = 'hub-more-panel';
    panel.append(support.cloneNode(true));
    menu.append(summary, panel);
    pin.prepend(menu);
    document.addEventListener('keydown', event => { if (event.key === 'Escape') menu.open = false; });
    document.addEventListener('pointerdown', event => { if (!menu.contains(event.target)) menu.open = false; });
  }
  window.addEventListener('pagehide', saveLocation);
})();
