/* In-drawer select menus stay inside the sheet (native <select> popups
   overflow Chrome device-mode / some tablet browsers). */
(function () {
  function optionLabel(opt) {
    return (opt && (opt.textContent || opt.label || opt.value)) || "";
  }

  function closeWrap(wrap) {
    if (!wrap) return;
    wrap.classList.remove("open");
    const menu = wrap.querySelector(".hub-select-menu");
    const btn = wrap.querySelector(".hub-select-trigger");
    if (menu) menu.hidden = true;
    if (btn) btn.setAttribute("aria-expanded", "false");
  }

  function closeAll(except) {
    document.querySelectorAll(".hub-select-wrap.open").forEach((wrap) => {
      if (wrap !== except) closeWrap(wrap);
    });
  }

  function renderMenu(wrap, select, menu) {
    menu.innerHTML = "";
    [...select.options].forEach((opt, i) => {
      if (opt.hidden) return;
      const row = document.createElement("button");
      row.type = "button";
      row.className = "hub-select-option";
      row.setAttribute("role", "option");
      if (i === select.selectedIndex) row.setAttribute("aria-selected", "true");
      row.textContent = optionLabel(opt);
      row.addEventListener("click", () => {
        select.selectedIndex = i;
        select.dispatchEvent(new Event("change", { bubbles: true }));
        closeWrap(wrap);
      });
      menu.appendChild(row);
    });
  }

  function containSelect(select) {
    if (!select || select.dataset.contained === "1") return;
    if (select.classList.contains("hub-folder-native")) return;
    select.dataset.contained = "1";
    const wrap = document.createElement("div");
    wrap.className = "hub-select-wrap";
    select.parentNode.insertBefore(wrap, select);
    wrap.appendChild(select);
    select.classList.add("hub-select-native");
    select.setAttribute("tabindex", "-1");
    select.setAttribute("aria-hidden", "true");

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "hub-select-trigger";
    btn.id = select.id ? select.id + "Trigger" : "";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    if (select.getAttribute("aria-label")) {
      btn.setAttribute("aria-label", select.getAttribute("aria-label"));
    }

    const menu = document.createElement("div");
    menu.className = "hub-select-menu";
    menu.setAttribute("role", "listbox");
    menu.hidden = true;

    wrap.appendChild(btn);
    wrap.appendChild(menu);

    const field = wrap.closest(".hub-drawer-field");
    const label = field && field.querySelector(`label[for="${select.id}"]`);
    if (label && btn.id) label.setAttribute("for", btn.id);

    const syncLabel = () => {
      const opt = select.options[select.selectedIndex];
      btn.textContent = optionLabel(opt) || "—";
    };

    btn.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      const open = !wrap.classList.contains("open");
      closeAll(wrap);
      if (open) {
        wrap.classList.add("open");
        menu.hidden = false;
        btn.setAttribute("aria-expanded", "true");
        renderMenu(wrap, select, menu);
        menu.style.top = "";
        menu.style.bottom = "";
        requestAnimationFrame(() => {
          const r = menu.getBoundingClientRect();
          if (r.bottom > window.innerHeight - 8) {
            menu.style.top = "auto";
            menu.style.bottom = "calc(100% + 4px)";
          }
        });
      } else {
        closeWrap(wrap);
      }
    });

    select.addEventListener("change", syncLabel);
    const mo = new MutationObserver(syncLabel);
    mo.observe(select, { childList: true, subtree: true, characterData: true });
    syncLabel();
  }

  function scan() {
    document.querySelectorAll(".hub-drawer select").forEach(containSelect);
  }

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".hub-select-wrap")) closeAll();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    if (!document.querySelector(".hub-select-wrap.open")) return;
    event.stopPropagation();
    closeAll();
  }, true);

  const drawer = document.getElementById("hubDrawer");
  if (drawer) {
    new MutationObserver(() => {
      if (!drawer.classList.contains("open")) closeAll();
    }).observe(drawer, { attributes: true, attributeFilter: ["class"] });
  }
  window.hubCloseContainedSelects = closeAll;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
  window.hubContainSelects = scan;
})();
