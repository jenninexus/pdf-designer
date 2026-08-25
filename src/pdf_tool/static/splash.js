/* Design Hub launch title. Holds 3s, then fades 2s; click / Enter / Escape skips. */
(function () {
  const splash = document.getElementById("hubSplash");
  if (!splash) return;
  if (document.documentElement.classList.contains("hub-splash-skip")) {
    splash.remove();
    return;
  }

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const HOLD_MS = reduced ? 400 : 3000;
  const FADE_MS = reduced ? 0 : 2000;
  let closed = false;

  function dismiss() {
    if (closed) return;
    closed = true;
    window.removeEventListener("keydown", skip);
    splash.removeEventListener("click", skip);
    try { sessionStorage.setItem("pdf-designer.hub.splash", "1"); } catch (_) {}
    splash.classList.add("is-out");
    const drop = function () { splash.remove(); };
    if (reduced) {
      drop();
      return;
    }
    splash.addEventListener("transitionend", drop, { once: true });
    setTimeout(drop, FADE_MS + 120);
  }

  const timer = setTimeout(dismiss, HOLD_MS);
  function skip(event) {
    if (event && event.type === "keydown" && !["Enter", "Escape", " "].includes(event.key)) return;
    if (event && event.key === " ") event.preventDefault();
    clearTimeout(timer);
    dismiss();
  }
  splash.addEventListener("click", skip);
  window.addEventListener("keydown", skip);
})();
