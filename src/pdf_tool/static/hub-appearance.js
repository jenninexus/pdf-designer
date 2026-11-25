/* Hub appearance is local chrome state, separate from the document palette. */
(() => {
  const key = "pdf-designer.hub.appearance";
  const root = document.documentElement;
  function apply(value) {
    root.dataset.hubAppearance = value === "light" ? "light" : "dark";
    root.dataset.theme = root.dataset.hubAppearance;
    root.dataset.bsTheme = root.dataset.hubAppearance;
    for (const input of document.querySelectorAll("[data-hub-appearance-choice]")) {
      input.checked = input.value === root.dataset.hubAppearance;
    }
  }
  try { apply(localStorage.getItem(key)); }
  catch (_) { apply(null); }
  window.addEventListener("storage", event => {
    if (event.key === key) apply(event.newValue);
  });
  document.addEventListener("change", event => {
    const input = event.target;
    if (!input.matches("[data-hub-appearance-choice]")) return;
    apply(input.value);
    try { localStorage.setItem(key, root.dataset.hubAppearance); } catch (_) {}
  });
})();
