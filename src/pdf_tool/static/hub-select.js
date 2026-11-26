/* One themed picker for the Hub, drawer, Wizard and PDF reader. */
(() => {
  const favoritesKey = "pdf-designer.hub.favoritePalettes";
  const hiddenKey = "pdf-designer.hub.hiddenPalettes";
  const pickers = new Map();

  function loadSet(key) {
    try {
      const stored = JSON.parse(localStorage.getItem(key) || "[]");
      if (Array.isArray(stored)) return new Set(stored.filter(value => typeof value === "string"));
    } catch (_) {}
    return new Set();
  }

  function saveSet(key, values) {
    try { localStorage.setItem(key, JSON.stringify([...values])); } catch (_) {}
  }

  const favorites = loadSet(favoritesKey);
  const hiddenPalettes = loadSet(hiddenKey);

  function iconButton(className, label, iconClass) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.setAttribute("aria-label", label);
    const icon = document.createElement("span");
    icon.className = iconClass;
    icon.setAttribute("aria-hidden", "true");
    button.append(icon);
    return button;
  }

  let active;
  function close(restoreFocus = false) {
    if (!active) return;
    const { wrap, trigger, menu } = active;
    active = null;
    wrap.classList.remove("open");
    trigger.setAttribute("aria-expanded", "false");
    menu.hidden = true;
    if (restoreFocus && trigger.getClientRects().length && !trigger.closest("[inert]")) {
      trigger.focus({ preventScroll: true });
    }
  }

  function position() {
    if (!active || active.inline) return;
    const { trigger, menu } = active;
    const rect = trigger.getBoundingClientRect();
    const { clientHeight, clientWidth } = document.documentElement;
    if (!rect.width || rect.bottom < 0 || rect.top > clientHeight) {
      close();
      return;
    }
    const width = Math.min(Math.max(180, rect.width), clientWidth - 16);
    const below = clientHeight - rect.bottom - 12;
    const above = rect.top - 12;
    const flip = below < Math.min(menu.scrollHeight + 2, 320) && above > below;
    menu.style.width = width + "px";
    menu.style.left = Math.max(8, Math.min(rect.left, clientWidth - width - 8)) + "px";
    menu.style.maxHeight = Math.max(0, Math.min(320, flip ? above : below)) + "px";
    menu.style.top = flip ? "" : rect.bottom + 4 + "px";
    menu.style.bottom = flip ? clientHeight - rect.top + 4 + "px" : "";
  }

  function reveal(button) {
    if (!button) return;
    button.focus({ preventScroll: true });
    const menu = button.closest(".hub-select-menu");
    const rect = button.getBoundingClientRect();
    const viewport = menu.getBoundingClientRect();
    if (rect.top < viewport.top) menu.scrollTop += rect.top - viewport.top;
    const restore = menu.querySelector(".hub-select-restore");
    const bottom = restore ? Math.min(viewport.bottom, restore.getBoundingClientRect().top) : viewport.bottom;
    if (rect.bottom > bottom) menu.scrollTop += rect.bottom - bottom;
  }

  function render(picker, focusKey) {
    const { select, menu } = picker;
    menu.replaceChildren();
    let favoriteToFocus;
    const available = [...select.options].filter(option => !option.hidden);
    const options = available.filter(option => !hiddenPalettes.has(option.dataset.favoriteKey));
    options.sort((a, b) => Number(favorites.has(b.dataset.favoriteKey)) - Number(favorites.has(a.dataset.favoriteKey)));
    for (const [index, option] of options.entries()) {
      const row = document.createElement("div");
      row.className = "hub-select-row";
      const choice = document.createElement("button");
      choice.type = "button";
      choice.className = "hub-select-option";
      choice.disabled = option.disabled;
      choice.textContent = option.label;
      choice.setAttribute("aria-pressed", String(option.selected));
      choice.addEventListener("click", () => {
        select.selectedIndex = option.index;
        close(true);
        select.dispatchEvent(new Event("change", { bubbles: true }));
      });
      row.append(choice);

      const favoriteKey = option.dataset.favoriteKey;
      if (favoriteKey) {
        const pin = iconButton("hub-select-pin", "Favorite " + option.label, "hub-select-star");
        pin.setAttribute("aria-pressed", String(favorites.has(favoriteKey)));
        pin.title = favorites.has(favoriteKey) ? "Remove favorite" : "Add favorite";
        pin.addEventListener("click", () => {
          if (favorites.has(favoriteKey)) favorites.delete(favoriteKey);
          else favorites.add(favoriteKey);
          saveSet(favoritesKey, favorites);
          const nextPin = render(picker, favoriteKey);
          position();
          reveal(nextPin);
        });
        if (favoriteKey === focusKey) favoriteToFocus = pin;

        const hide = iconButton("hub-select-hide", "Hide " + option.label, "hub-select-remove-icon");
        hide.title = "Hide this palette";
        hide.addEventListener("click", () => {
          hiddenPalettes.add(favoriteKey);
          saveSet(hiddenKey, hiddenPalettes);
          if (option.selected) {
            select.value = "";
            select.dispatchEvent(new Event("change", { bubbles: true }));
          }
          render(picker);
          position();
          const choices = menu.querySelectorAll(".hub-select-option:enabled");
          reveal(choices[index] || choices[choices.length - 1]);
        });
        row.append(pin, hide);
      }
      menu.append(row);
    }

    if (available.some(option => hiddenPalettes.has(option.dataset.favoriteKey))) {
      const restore = document.createElement("button");
      restore.type = "button";
      restore.className = "hub-select-restore";
      restore.textContent = "Restore hidden palettes";
      restore.addEventListener("click", () => {
        hiddenPalettes.clear();
        saveSet(hiddenKey, hiddenPalettes);
        render(picker);
        position();
        reveal(menu.querySelector('.hub-select-option[aria-pressed="true"]:enabled')
          || menu.querySelector(".hub-select-option:enabled"));
      });
      menu.append(restore);
    }
    return favoriteToFocus;
  }

  function containSelect(select) {
    if (pickers.has(select) || select.classList.contains("hub-folder-native")) return;
    const label = select.labels?.[0];
    const name = select.getAttribute("aria-label") || label?.textContent.trim() || select.title;
    const wrap = document.createElement("div");
    wrap.className = "hub-select-wrap";
    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.id = select.id + "Trigger";
    trigger.className = "hub-select-trigger";
    trigger.setAttribute("aria-expanded", "false");
    if (name) trigger.setAttribute("aria-label", name);
    if (label?.htmlFor === select.id) label.htmlFor = trigger.id;
    const value = document.createElement("span");
    value.id = select.id + "Value";
    const describedBy = [select.getAttribute("aria-describedby"), value.id].filter(Boolean).join(" ");
    trigger.setAttribute("aria-describedby", describedBy);
    trigger.append(value);

    const menu = document.createElement("div");
    menu.id = select.id + "Menu";
    menu.className = "hub-select-menu";
    menu.setAttribute("role", "group");
    if (name) menu.setAttribute("aria-label", name + " choices");
    trigger.setAttribute("aria-controls", menu.id);
    menu.hidden = true;

    select.before(wrap);
    wrap.append(select, trigger, menu);
    select.classList.add("hub-select-native");
    select.tabIndex = -1;
    select.setAttribute("aria-hidden", "true");

    const sync = () => {
      value.textContent = select.selectedOptions[0]?.label || "—";
      trigger.title = value.textContent;
      trigger.disabled = select.disabled || !select.options.length;
    };
    const picker = { select, wrap, trigger, menu, sync, inline: Boolean(wrap.closest(".hub-drawer")) };
    pickers.set(select, picker);
    function open() {
      close();
      active = picker;
      wrap.classList.add("open");
      trigger.setAttribute("aria-expanded", "true");
      menu.hidden = false;
      render(picker);
      position();
      if (picker.inline) menu.scrollIntoView({ block: "nearest" });
      if (active === picker) reveal(menu.querySelector('.hub-select-option[aria-pressed="true"]:enabled')
        || menu.querySelector(".hub-select-option:enabled"));
    }
    trigger.addEventListener("click", () => active === picker ? close(true) : open());
    trigger.addEventListener("keydown", event => {
      if (event.key !== "ArrowDown" && event.key !== "ArrowUp") return;
      event.preventDefault();
      open();
    });
    menu.addEventListener("keydown", event => {
      const options = [...menu.querySelectorAll(".hub-select-option:enabled")];
      const index = options.indexOf(event.target.closest(".hub-select-row")?.querySelector(".hub-select-option"));
      const next = { ArrowDown: options[index + 1], ArrowUp: options[index - 1], Home: options[0], End: options.at(-1) };
      if (!(event.key in next)) return;
      event.preventDefault();
      reveal(next[event.key]);
    });
    wrap.closest("details")?.addEventListener("toggle", event => {
      if (!event.currentTarget.open && active === picker) close();
    });
    select.addEventListener("change", sync);
    sync();
  }

  function scan() {
    document.querySelectorAll("select[id]").forEach(containSelect);
  }

  document.addEventListener("pointerdown", event => {
    if (active && !active.wrap.contains(event.target)) close();
  });
  document.addEventListener("focusin", event => {
    if (active && !active.wrap.contains(event.target)) close();
  });
  document.addEventListener("keydown", event => {
    if (!active || event.key !== "Escape") return;
    event.preventDefault();
    event.stopPropagation();
    close(true);
  }, true);
  window.addEventListener("resize", position);
  window.addEventListener("scroll", event => {
    if (event.target !== active?.menu) position();
  }, true);

  window.hubCloseContainedSelects = close;
  window.hubSyncSelects = () => pickers.forEach(picker => picker.sync());
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", scan);
  else scan();
})();
