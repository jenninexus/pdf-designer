/* Design Hub pane resizing. Local browser preference only; no server state.
   Dockview-inspired sash (persisted width, keyboard, double-click reset) —
   not the Dockview library. www-theme-kit/profiles/pdf-designer.json */
(function () {
  function wireSash(opts) {
    const pane = document.getElementById(opts.paneId);
    const handle = document.getElementById(opts.handleId);
    if (!pane || !handle) return;
    const min = opts.min;
    const defaultWidth = opts.defaultWidth;
    const invert = !!opts.invert;
    const stackedMq = window.matchMedia("(max-width: 575.98px)");
    const maxWidth = () => {
      const cap = typeof opts.max === "function" ? opts.max() : opts.max;
      return Math.max(min, cap);
    };
    const clamp = value => Math.round(Math.max(min, Math.min(maxWidth(), value)));
    const setWidth = (value, persist = true) => {
      if (stackedMq.matches && opts.hideWhenStacked) return;
      const width = clamp(value);
      document.documentElement.style.setProperty(opts.cssVar, width + "px");
      handle.setAttribute("aria-valuemin", String(min));
      handle.setAttribute("aria-valuemax", String(maxWidth()));
      handle.setAttribute("aria-valuenow", String(width));
      if (persist) try { localStorage.setItem(opts.key, String(width)); } catch (_) {}
    };
    try {
      const saved = Number(localStorage.getItem(opts.key));
      if (Number.isFinite(saved)) setWidth(saved, false);
    } catch (_) {}
    window.addEventListener("resize", () => {
      if (stackedMq.matches && opts.hideWhenStacked) return;
      setWidth(pane.getBoundingClientRect().width, false);
    });
    handle.addEventListener("pointerdown", event => {
      if (stackedMq.matches && opts.hideWhenStacked) return;
      event.preventDefault();
      const startX = event.clientX;
      const startWidth = pane.getBoundingClientRect().width;
      handle.setPointerCapture(event.pointerId);
      document.documentElement.classList.add("drawer-resizing");
      const move = e => {
        const delta = invert ? (startX - e.clientX) : (e.clientX - startX);
        setWidth(startWidth + delta);
      };
      const finish = e => {
        handle.releasePointerCapture?.(e.pointerId);
        document.documentElement.classList.remove("drawer-resizing");
        handle.removeEventListener("pointermove", move);
        handle.removeEventListener("pointerup", finish);
        handle.removeEventListener("pointercancel", finish);
      };
      handle.addEventListener("pointermove", move);
      handle.addEventListener("pointerup", finish);
      handle.addEventListener("pointercancel", finish);
    });
    handle.addEventListener("keydown", event => {
      const width = pane.getBoundingClientRect().width;
      const grow = invert ? "ArrowLeft" : "ArrowRight";
      const shrink = invert ? "ArrowRight" : "ArrowLeft";
      if (event.key === grow) { event.preventDefault(); setWidth(width + 16); }
      if (event.key === shrink) { event.preventDefault(); setWidth(width - 16); }
      if (event.key === "Home") { event.preventDefault(); setWidth(min); }
      if (event.key === "End") { event.preventDefault(); setWidth(maxWidth()); }
    });
    handle.addEventListener("dblclick", () => {
      try { localStorage.removeItem(opts.key); } catch (_) {}
      setWidth(defaultWidth, false);
    });
  }

  wireSash({
    paneId: "hubDrawer",
    handleId: "drawerResize",
    key: "pdf-designer.hub.drawerWidth",
    cssVar: "--hub-drawer-w",
    min: 280,
    defaultWidth: 320,
    invert: true,
    max: () => Math.min(560, window.innerWidth - (window.innerWidth <= 576 ? 16 : 24)),
  });

  wireSash({
    paneId: "hubLibrary",
    handleId: "libraryResize",
    key: "pdf-designer.hub.libraryWidth",
    cssVar: "--hub-library-w",
    min: 200,
    defaultWidth: 300,
    invert: false,
    hideWhenStacked: true,
    max: () => Math.min(480, Math.round(window.innerWidth * 0.45)),
  });
})();
