/* Design Hub launch title. Stays until Open, Start wizard, Enter, or Escape. */
(function () {
  const splash = document.getElementById("hubSplash");
  if (!splash) return;
  if (document.documentElement.classList.contains("hub-splash-skip")) {
    splash.remove();
    return;
  }

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const FADE_MS = reduced ? 0 : 2000;
  let closed = false;
  const openBtn = document.getElementById("hubSplashOpen");
  const wizardLink = document.getElementById("hubSplashWizard");

  function samePath(href) {
    const here = (location.pathname.replace(/\/+$/, "") || "/");
    const there = (href.replace(/\/+$/, "") || "/");
    return here === there;
  }

  function dismiss(href) {
    if (closed) return;
    closed = true;
    window.removeEventListener("keydown", onKey);
    try { sessionStorage.setItem("pdf-designer.hub.splash", "1"); } catch (_) {}
    splash.classList.add("is-out");
    const drop = function () {
      splash.remove();
      if (href && !samePath(href)) location.assign(href);
    };
    if (reduced) {
      drop();
      return;
    }
    splash.addEventListener("transitionend", drop, { once: true });
    setTimeout(drop, FADE_MS + 120);
  }

  function onKey(event) {
    if (event.key === "Escape") {
      event.preventDefault();
      dismiss();
      return;
    }
    if (event.key === "Enter" && event.target && event.target.closest("a, button")) return;
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      dismiss("/");
    }
  }

  if (openBtn) {
    openBtn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      dismiss("/");
    });
  }
  if (wizardLink) {
    wizardLink.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      dismiss("/wizard");
    });
  }

  window.addEventListener("keydown", onKey);
  if (openBtn) {
    try { openBtn.focus(); } catch (_) {}
  }
})();
