/* Shared Design Hub drawer chrome (recipes / vault / wizard).
   Library page wires its own drawer because it syncs chips/selects. */
(function () {
  function openDrawer() {
    const drawer = document.getElementById("hubDrawer");
    const backdrop = document.getElementById("hubDrawerBackdrop");
    const toggle = document.getElementById("drawerToggle");
    if (!drawer) return;
    drawer.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    if (backdrop) { backdrop.hidden = false; backdrop.classList.add("open"); }
    document.body.classList.add("drawer-open");
    if (toggle) toggle.setAttribute("aria-expanded", "true");
  }
  function closeDrawer() {
    const drawer = document.getElementById("hubDrawer");
    const backdrop = document.getElementById("hubDrawerBackdrop");
    const toggle = document.getElementById("drawerToggle");
    if (!drawer) return;
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    if (backdrop) { backdrop.classList.remove("open"); backdrop.hidden = true; }
    document.body.classList.remove("drawer-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    window.hubCloseContainedSelects?.();
  }
  window.hubOpenDrawer = openDrawer;
  window.hubCloseDrawer = closeDrawer;

  const toggle = document.getElementById("drawerToggle");
  const closeBtn = document.getElementById("drawerClose");
  const backdrop = document.getElementById("hubDrawerBackdrop");
  const drawerRefresh = document.getElementById("drawerRefresh");
  if (toggle) toggle.addEventListener("click", () => {
    const open = document.getElementById("hubDrawer")?.classList.contains("open");
    if (open) closeDrawer(); else openDrawer();
  });
  if (closeBtn) closeBtn.addEventListener("click", closeDrawer);
  if (backdrop) backdrop.addEventListener("click", closeDrawer);
  if (drawerRefresh) drawerRefresh.addEventListener("click", () => {
    document.getElementById("refreshBtn")?.click();
    closeDrawer();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeDrawer();
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
