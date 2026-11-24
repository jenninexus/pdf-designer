/* Shared Design Hub drawer and page-scroll controls. */
(function () {
  const drawer = document.getElementById("hubDrawer");
  const backdrop = document.getElementById("hubDrawerBackdrop");
  const toggle = document.getElementById("drawerToggle");
  const closeBtn = document.getElementById("drawerClose");
  const drawerRefresh = document.getElementById("drawerRefresh");
  if (!drawer || !toggle || !closeBtn) return;

  const compactNav = window.matchMedia("(max-width: 991.98px)");
  const isOpen = () => drawer.classList.contains("open");
  let previousFocus;
  let background = [];
  drawer.inert = true;
  drawer.setAttribute("role", "dialog");
  drawer.setAttribute("aria-modal", "true");

  function openDrawer() {
    if (isOpen() || !compactNav.matches) return;
    previousFocus = document.activeElement;
    background = [...document.body.children].filter(el =>
      el !== drawer && el !== backdrop && el.tagName !== "SCRIPT" && !el.inert);
    drawer.inert = false;
    drawer.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    if (backdrop) { backdrop.hidden = false; backdrop.classList.add("open"); }
    document.body.classList.add("drawer-open");
    toggle.setAttribute("aria-expanded", "true");
    closeBtn.focus({ preventScroll: true });
    background.forEach(el => { el.inert = true; });
  }

  function closeDrawer() {
    if (!isOpen()) return;
    window.hubCloseContainedSelects?.();
    background.forEach(el => { el.inert = false; });
    background = [];
    const returnFocus = previousFocus?.getClientRects().length && previousFocus !== document.body
      ? previousFocus
      : compactNav.matches ? toggle : document.querySelector(".hub-brand");
    returnFocus?.focus({ preventScroll: true });
    drawer.inert = true;
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    if (backdrop) { backdrop.classList.remove("open"); backdrop.hidden = true; }
    document.body.classList.remove("drawer-open");
    toggle.setAttribute("aria-expanded", "false");
  }
  window.hubOpenDrawer = openDrawer;
  window.hubCloseDrawer = closeDrawer;

  toggle.addEventListener("click", openDrawer);
  closeBtn.addEventListener("click", closeDrawer);
  backdrop?.addEventListener("click", closeDrawer);
  drawerRefresh?.addEventListener("click", () => {
    document.getElementById("refreshBtn")?.click();
    closeDrawer();
  });
  compactNav.addEventListener("change", () => {
    if (!compactNav.matches) closeDrawer();
  });
  drawer.addEventListener("keydown", event => {
    if (event.key === "Escape") closeDrawer();
    if (event.key !== "Tab") return;
    const focusable = [...drawer.querySelectorAll("a[href], button, input, select, [tabindex]")]
      .filter(el => !el.disabled && el.tabIndex >= 0 && el.getClientRects().length);
    const first = focusable[0];
    const last = focusable.at(-1);
    if (!first) return;
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  /* Back-to-top on document-scroll pages only (vault / recipes / wizard). */
  if (document.body.classList.contains("hub-page")) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.id = "hubToTop";
    btn.className = "hub-to-top";
    btn.title = "Back to top";
    btn.setAttribute("aria-label", "Back to top");
    btn.setAttribute("aria-hidden", "true");
    btn.tabIndex = -1;
    btn.innerHTML = '<span class="hub-fa-icon fa-chevron-up" aria-hidden="true"></span>';
    document.body.appendChild(btn);

    const showAt = 280;
    const sync = () => {
      const show = window.scrollY > showAt && !document.body.classList.contains("drawer-open");
      btn.classList.toggle("is-visible", show);
      btn.setAttribute("aria-hidden", show ? "false" : "true");
      btn.tabIndex = show ? 0 : -1;
    };
    window.addEventListener("scroll", sync, { passive: true });
    btn.addEventListener("click", () => {
      const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
    });
    sync();
  }
})();
