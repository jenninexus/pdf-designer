/* Design Hub pane resizing. Local browser preference only; no server state.
   Dockview-inspired sash (persisted width, keyboard, double-click reset) —
   not the Dockview library. www-theme-kit/profiles/pdf-designer.json */
(function () {
  function wireSash(opts) {
    const pane = document.getElementById(opts.paneId);
    const handle = document.getElementById(opts.handleId);
    if (!pane || !handle) return;
    const min = opts.min;
    const invert = !!opts.invert;
    const stackedMq = window.matchMedia("(max-width: 575.98px)");
    const phoneSheetMq = window.matchMedia("(max-width: 575.98px), (max-height: 480px)");
    const compactNavMq = window.matchMedia("(max-width: 1399.98px)");
    const compactPanel = () => compactNavMq.matches && !phoneSheetMq.matches;
    const defaultWidth = () => {
      if (typeof opts.defaultWidth === "function") return opts.defaultWidth();
      return opts.defaultWidth;
    };
    const maxWidth = () => {
      const cap = typeof opts.max === "function" ? opts.max() : opts.max;
      return Math.max(min, cap);
    };
    const clamp = value => Math.round(Math.max(min, Math.min(maxWidth(), value)));
    const sheetOff = () => (opts.hideWhenPhoneSheet && phoneSheetMq.matches)
      || (opts.hideWhenStacked && stackedMq.matches);
    const setWidth = (value, persist = true) => {
      if (sheetOff()) return;
      const width = clamp(value);
      document.documentElement.style.setProperty(opts.cssVar, width + "px");
      handle.setAttribute("aria-valuemin", String(min));
      handle.setAttribute("aria-valuemax", String(maxWidth()));
      handle.setAttribute("aria-valuenow", String(width));
      if (persist) try { localStorage.setItem(opts.key, String(width)); } catch (_) {}
    };
    try {
      const saved = Number(localStorage.getItem(opts.key));
      const legacyDefault = typeof opts.legacyDefault === "number" ? opts.legacyDefault : 320;
      // Compact-nav used to force 100vw, so a stored 320 was never a real choice.
      if (compactPanel() && opts.migrateSkinnyDefault && (!Number.isFinite(saved) || saved <= legacyDefault)) {
        setWidth(defaultWidth(), false);
      } else if (Number.isFinite(saved)) {
        setWidth(saved, false);
      }
    } catch (_) {}
    window.addEventListener("resize", () => {
      if (sheetOff()) return;
      if (compactPanel() && opts.migrateSkinnyDefault) {
        const saved = Number(localStorage.getItem(opts.key));
        if (!Number.isFinite(saved) || saved <= (opts.legacyDefault || 320)) {
          setWidth(defaultWidth(), false);
          return;
        }
      }
      setWidth(pane.getBoundingClientRect().width, false);
    });
    handle.addEventListener("pointerdown", event => {
      if (sheetOff()) return;
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
      setWidth(defaultWidth(), false);
    });
  }

  wireSash({
    paneId: "hubDrawer",
    handleId: "drawerResize",
    key: "pdf-designer.hub.drawerWidth",
    cssVar: "--hub-drawer-w",
    min: 280,
    legacyDefault: 320,
    migrateSkinnyDefault: true,
    defaultWidth: () => {
      if (window.matchMedia("(max-width: 1399.98px)").matches
          && window.matchMedia("(min-width: 576px)").matches
          && window.matchMedia("(min-height: 481px)").matches) {
        return Math.round(window.innerWidth * 0.92);
      }
      return 320;
    },
    invert: true,
    hideWhenPhoneSheet: true,
    max: () => {
      const peek = 24;
      if (window.matchMedia("(max-width: 1399.98px)").matches
          && window.matchMedia("(min-width: 576px)").matches
          && window.matchMedia("(min-height: 481px)").matches) {
        return window.innerWidth - peek;
      }
      return Math.min(560, window.innerWidth - peek);
    },
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
