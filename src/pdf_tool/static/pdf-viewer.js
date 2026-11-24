(function () {
  const params = new URLSearchParams(location.search);
  const doc = params.get("doc") || "";
  const canvas = document.getElementById("pdfCanvas");
  const loading = document.getElementById("pdfLoading");
  const title = document.getElementById("pdfTitle");
  const open = document.getElementById("openPdf");
  const fit = document.getElementById("fitWidth");
  const pairedLayout = window.matchMedia("(min-width: 576px)");
  let zoom = 1;
  let pages = [];

  function applyZoom(next, fitting = false) {
    zoom = Math.max(0.01, Math.min(2.5, next));
    document.documentElement.style.setProperty("--page-zoom", String(zoom));
    fit.setAttribute("aria-pressed", String(fitting));
  }

  function fitWidth() {
    if (!pages.length) return;
    const styles = getComputedStyle(canvas);
    const contentWidth = canvas.clientWidth - parseFloat(styles.paddingLeft) - parseFloat(styles.paddingRight);
    let fittedZoom = Math.min(1.5, contentWidth / Math.max(...pages.map(page => page.widthPt * 4 / 3)));
    if (pairedLayout.matches && canvas.classList.contains("reader-two-up")) {
      for (const spread of canvas.querySelectorAll(".reader-spread")) {
        if (spread.childElementCount < 2) continue;
        const width = Array.from(spread.children).reduce((sum, image) => {
          return sum + pages[Number(image.dataset.page) - 1].widthPt * 4 / 3;
        }, 0);
        const gap = parseFloat(getComputedStyle(spread).columnGap);
        fittedZoom = Math.min(fittedZoom, (contentWidth - gap) / width);
      }
    }
    applyZoom(fittedZoom, true);
  }

  function stepZoom(direction) {
    if (pages.length) applyZoom(zoom * 1.15 ** direction);
  }

  document.getElementById("zoomOut").addEventListener("click", () => stepZoom(-1));
  document.getElementById("zoomIn").addEventListener("click", () => stepZoom(1));
  fit.addEventListener("click", fitWidth);
  window.addEventListener("resize", () => {
    if (fit.getAttribute("aria-pressed") === "true") fitWidth();
  });
  canvas.addEventListener("wheel", event => {
    if (!event.ctrlKey && !event.metaKey) return;
    event.preventDefault();
    if (event.deltaY) stepZoom(-Math.sign(event.deltaY));
  }, { passive: false });
  document.addEventListener("keydown", event => {
    if (!(event.ctrlKey || event.metaKey) || !canvas.matches(":hover")) return;
    if (event.key === "+" || event.key === "=") stepZoom(1);
    else if (event.key === "-") stepZoom(-1);
    else if (event.key === "0") fitWidth();
    else return;
    event.preventDefault();
  });

  if (!doc) {
    loading.className = "pdf-error";
    loading.textContent = "No PDF was selected.";
    return;
  }
  open.href = "/" + doc.split("/").map(encodeURIComponent).join("/");

  fetch("/api/pdf-info?doc=" + encodeURIComponent(doc))
    .then(response => response.json())
    .then(info => {
      if (!info.ok) throw new Error(info.error || "PDF preview failed");
      pages = info.pages || [];
      title.textContent = info.name || "PDF preview";
      loading.remove();
      for (const page of pages) {
        const image = document.createElement("img");
        image.className = "pdf-page";
        image.loading = page.index < 2 ? "eager" : "lazy";
        image.alt = `PDF page ${page.index + 1}`;
        image.dataset.page = String(page.index + 1);
        image.style.setProperty("--page-width", `${page.widthPt * 4 / 3}px`);
        image.style.aspectRatio = `auto ${page.widthPt} / ${page.heightPt}`;
        image.src = "/api/pdf-page?doc=" + encodeURIComponent(doc) + "&page=" + page.index + "&scale=2";
        canvas.appendChild(image);
      }
      fitWidth();
    })
    .catch(error => {
      loading.className = "pdf-error";
      loading.textContent = error.message;
    });
})();
