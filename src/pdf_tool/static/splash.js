/* Decorative launch, never a loading gate: max 2.7s including its short exit. */
(function () {
  const splash = document.getElementById('hubSplash');
  if (!splash) return;
  if (document.documentElement.classList.contains('hub-splash-skip')) {
    splash.remove();
    return;
  }
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const styles = getComputedStyle(document.documentElement);
  const MAX_MS = Math.min(2700, parseFloat(styles.getPropertyValue('--hub-splash-max-ms')) || 2700);
  const EXIT_MS = Math.min(180, parseFloat(styles.getPropertyValue('--hub-splash-exit-ms')) || 180);
  const started = window.__pdfSplashStart ?? performance.now();
  const previousFocus = document.activeElement;
  const inertStates = [...document.body.children].filter(el => el !== splash && el.tagName !== 'SCRIPT')
    .map(el => [el, el.inert]);
  inertStates.forEach(([el]) => { el.inert = true; });
  const openBtn = document.getElementById('hubSplashOpen');
  const wizardLink = document.getElementById('hubSplashWizard');
  let closed = false;
  let finished = false;
  let deadline;
  let fallback;
  function finish(href) {
    if (finished) return;
    finished = true;
    clearTimeout(deadline);
    clearTimeout(fallback);
    inertStates.forEach(([el, inert]) => { el.inert = inert; });
    const needsFocus = splash.contains(document.activeElement);
    splash.remove();
    if (href && location.pathname !== href) { location.assign(href); return; }
    if (needsFocus) {
      const target = previousFocus !== document.body && previousFocus?.isConnected
        ? previousFocus : document.querySelector('.hub-brand, main button, main a');
      target?.focus({ preventScroll: true });
    }
  }
  function dismiss(href) {
    if (closed) return;
    closed = true;
    window.removeEventListener('keydown', onKey);
    reduced.removeEventListener('change', onMotionChange);
    try { sessionStorage.setItem('pdf-designer.hub.splash', '1'); } catch (_) {}
    clearTimeout(deadline);
    if (reduced.matches) { finish(href); return; }
    splash.classList.add('is-out');
    splash.addEventListener('transitionend', event => {
      if (event.target === splash && event.propertyName === 'opacity') finish(href);
    });
    fallback = setTimeout(() => finish(href), EXIT_MS);
  }
  function onMotionChange() { if (reduced.matches) dismiss(); }
  function onKey(event) {
    if (event.key === 'Escape') { event.preventDefault(); dismiss(); }
    else if (event.key === 'Tab') {
      const buttons = [openBtn, wizardLink].filter(Boolean);
      if (!buttons.length) return;
      if (event.shiftKey && document.activeElement === buttons[0]) {
        event.preventDefault(); buttons[buttons.length - 1].focus();
      } else if (!event.shiftKey && document.activeElement === buttons[buttons.length - 1]) {
        event.preventDefault(); buttons[0].focus();
      }
    } else if ((event.key === 'Enter' || event.key === ' ') && !event.target.closest('a, button')) {
      event.preventDefault(); dismiss();
    }
  }
  openBtn?.addEventListener('click', event => { event.preventDefault(); dismiss(); });
  wizardLink?.addEventListener('click', event => { event.preventDefault(); dismiss('/wizard'); });
  window.addEventListener('keydown', onKey);
  reduced.addEventListener('change', onMotionChange);
  if (reduced.matches) { dismiss(); return; }
  openBtn?.focus({ preventScroll: true });
  deadline = setTimeout(() => dismiss(), Math.max(0, MAX_MS - EXIT_MS - (performance.now() - started)));
})();
