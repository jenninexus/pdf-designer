(function () {
  const params = new URLSearchParams(location.search);
  const doc = params.get("doc") || "";
  const canvas = document.getElementById("pdfCanvas");
  const loading = document.getElementById("pdfLoading");
  const title = document.getElementById("pdfTitle");
  const current = document.getElementById("currentPage");
  const total = document.getElementById("pageCount");
  const open = document.getElementById("openPdf");
  let zoom = 1;
  let pages = [];

  function applyZoom(next) {
    zoom = Math.max(0.35, Math.min(2.5, next));
    document.documentElement.style.setProperty("--page-zoom", String(zoom));
  }

  function fitWidth() {
    if (!pages.length) return;
    const maxWidth = Math.max(...pages.map(page => page.widthPt * 4 / 3));
    applyZoom(Math.min(1.5, (canvas.clientWidth - 56) / maxWidth));
  }

  document.getElementById("zoomOut").addEventListener("click", () => applyZoom(zoom - 0.1));
  document.getElementById("zoomIn").addEventListener("click", () => applyZoom(zoom + 0.1));
  document.getElementById("fitWidth").addEventListener("click", fitWidth);
  window.addEventListener("resize", () => { if (zoom <= 1.5) fitWidth(); }, { passive: true });

  if (!doc) {
    loading.className = "pdf-error";
    loading.textContent = "No PDF was selected.";
    return;
  }
  open.href = "/" + doc;

  fetch("/api/pdf-info?doc=" + encodeURIComponent(doc))
    .then(response => response.json())
    .then(info => {
      if (!info.ok) throw new Error(info.error || "PDF preview failed");
      pages = info.pages || [];
      title.textContent = info.name || "PDF preview";
      total.textContent = String(info.pageCount || pages.length);
      loading.remove();
      for (const page of pages) {
        const image = document.createElement("img");
        image.className = "pdf-page";
        image.loading = page.index < 2 ? "eager" : "lazy";
        image.alt = `PDF page ${page.index + 1}`;
        image.dataset.page = String(page.index + 1);
        image.style.setProperty("--page-width", `${page.widthPt * 4 / 3}px`);
        image.src = "/api/pdf-page?doc=" + encodeURIComponent(doc) + "&page=" + page.index + "&scale=2";
        canvas.appendChild(image);
      }
      fitWidth();
      const observer = new IntersectionObserver(entries => {
        const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) current.textContent = visible.target.dataset.page;
      }, { threshold: [0.2, 0.5, 0.8] });
      canvas.querySelectorAll(".pdf-page").forEach(page => observer.observe(page));
    })
    .catch(error => {
      loading.className = "pdf-error";
      loading.textContent = error.message;
    });
})();
