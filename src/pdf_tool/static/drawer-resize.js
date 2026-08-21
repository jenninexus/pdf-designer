/* Design Hub drawer resizing. Local browser preference only; no server state. */
(function () {
  const drawer = document.getElementById("hubDrawer");
  const handle = document.getElementById("drawerResize");
  if (!drawer || !handle) return;
  const key = "pdf-designer.hub.drawerWidth";
  const min = 280;
  const maxWidth = () => Math.max(min, Math.min(560, window.innerWidth - (window.innerWidth <= 576 ? 16 : 24)));
  const clamp = value => Math.round(Math.max(min, Math.min(maxWidth(), value)));
  const setWidth = (value, persist = true) => {
    const width = clamp(value);
    document.documentElement.style.setProperty("--hub-drawer-w", width + "px");
    handle.setAttribute("aria-valuemin", String(min));
    handle.setAttribute("aria-valuemax", String(maxWidth()));
    handle.setAttribute("aria-valuenow", String(width));
    if (persist) try { localStorage.setItem(key, String(width)); } catch (_) {}
  };
  try {
    const saved = Number(localStorage.getItem(key));
    if (Number.isFinite(saved)) setWidth(saved, false);
  } catch (_) {}
  window.addEventListener("resize", () => setWidth(drawer.getBoundingClientRect().width, false));
  handle.addEventListener("pointerdown", event => {
    event.preventDefault();
    const startX = event.clientX;
    const startWidth = drawer.getBoundingClientRect().width;
    handle.setPointerCapture(event.pointerId);
    document.documentElement.classList.add("drawer-resizing");
    const move = e => setWidth(startWidth + (startX - e.clientX));
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
    const width = drawer.getBoundingClientRect().width;
    if (event.key === "ArrowLeft") { event.preventDefault(); setWidth(width + 16); }
    if (event.key === "ArrowRight") { event.preventDefault(); setWidth(width - 16); }
    if (event.key === "Home") { event.preventDefault(); setWidth(min); }
    if (event.key === "End") { event.preventDefault(); setWidth(maxWidth()); }
  });
  handle.addEventListener("dblclick", () => {
    try { localStorage.removeItem(key); } catch (_) {}
    setWidth(320, false);
  });
})();
