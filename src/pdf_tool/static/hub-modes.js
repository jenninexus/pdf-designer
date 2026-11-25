/* Shared application identity and real Hub modes. Independent of drawer wiring. */
(function () {
  const bar = document.querySelector('.hub-bar');
  const brand = bar?.querySelector('.hub-brand');
  const nav = bar?.querySelector('.hub-nav');
  if (!brand || !nav) return;

  // Identity and mode icons are in the HTML so navigation never paints a text
  // toolbar first and replaces it after scripts/data finish loading.

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
  const modeLinks = document.querySelectorAll('.hub-modes a, .hub-drawer .hub-nav a');
  for (const link of modeLinks) {
    const path = new URL(link.href).pathname;
    const mode = modes[path];
    if (!mode) continue;
    link.setAttribute('aria-label', mode[0]);
    link.title = `${mode[0]} — ${mode[1]}`;
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
      if (active && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey && event.button === 0) {
        event.preventDefault();
        window.hubCloseDrawer?.();
      }
    });
  }
  // Warm the destination HTML on intent. Keep normal links, back/forward and
  // each page's existing lifecycle; never cache private API responses in storage.
  const warmed = new Set();
  const canHover = matchMedia('(hover: hover) and (pointer: fine)');
  for (const link of modeLinks) {
    const warm = () => {
      const url = new URL(link.href, location.origin);
      if (url.origin !== location.origin || !modes[url.pathname] || url.pathname === currentPath || warmed.has(url.href)) return;
      if (navigator.connection?.saveData) return;
      warmed.add(url.href);
      const hint = document.createElement('link');
      hint.rel = 'prefetch';
      hint.href = url.href;
      hint.as = 'document';
      document.head.append(hint);
    };
    link.addEventListener('pointerenter', () => { if (canHover.matches) warm(); });
    link.addEventListener('focus', warm, { once: true });
  }
  // Share one settings layout across desktop chrome and the compact drawer.
  const support = document.querySelector('.hub-drawer .hub-support');
  const pin = bar.querySelector('.hub-bar-pin');
  function appearance(group) {
    const settings = document.createElement('details');
    settings.className = 'hub-appearance-settings';
    settings.innerHTML = `
      <summary>Appearance</summary>
      <fieldset aria-label="Hub color mode">
        <label><input type="radio" name="hub-appearance-${group}" value="dark" data-hub-appearance-choice> Dark</label>
        <label><input type="radio" name="hub-appearance-${group}" value="light" data-hub-appearance-choice> Light</label>
      </fieldset>`;
    settings.querySelectorAll('input').forEach(input => {
      input.checked = input.value === document.documentElement.dataset.hubAppearance;
    });
    return settings;
  }
  if (support && pin) {
    const menu = document.createElement('details');
    menu.className = 'hub-more hub-support-menu';
    const summary = document.createElement('summary');
    summary.innerHTML = 'Settings <span class="hub-fa-icon fa-chevron-down hub-chevron" aria-hidden="true"></span>';
    const panel = document.createElement('div');
    panel.className = 'hub-more-panel';
    panel.append(appearance('desktop'), support.cloneNode(true));
    menu.append(summary, panel);
    pin.append(menu);
    const compactSettings = document.createElement('div');
    compactSettings.className = 'hub-drawer-section';
    compactSettings.append(appearance('drawer'));
    support.before(compactSettings);
  }
  window.addEventListener('pagehide', saveLocation);
})();
