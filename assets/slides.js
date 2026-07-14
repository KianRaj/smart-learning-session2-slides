/* ============================================================
   KIET Deep Learning — slide engine (vanilla JS, no deps)
   Works from a local file:// path or GitHub Pages.
   ============================================================ */
(function () {
  const slides = Array.from(document.querySelectorAll(".slide"));
  if (!slides.length) return;

  // number each slide in the margin
  slides.forEach((s, i) => {
    const no = document.createElement("div");
    no.className = "slide-no";
    no.textContent = String(i + 1).padStart(2, "0");
    s.appendChild(no);
  });

  const progress = document.querySelector(".progress");
  const counter  = document.querySelector(".counter");
  const total    = slides.length;

  // deep-link support: #3 opens slide 3
  let idx = Math.min(Math.max(parseInt(location.hash.slice(1)) || 1, 1), total) - 1;

  function show(n, animate) {
    idx = Math.min(Math.max(n, 0), total - 1);
    slides.forEach((s, i) => {
      s.classList.toggle("active", i === idx);
      if (i === idx && animate) {
        s.classList.remove("turn"); void s.offsetWidth; s.classList.add("turn");
      }
    });
    if (progress) progress.style.width = ((idx + 1) / total * 100) + "%";
    if (counter)  counter.innerHTML = "<b>" + (idx + 1) + "</b> / " + total;
    history.replaceState(null, "", "#" + (idx + 1));
    slides[idx].scrollTop = 0;
  }
  const next = () => show(idx + 1, true);
  const prev = () => show(idx - 1, true);

  // keyboard
  document.addEventListener("keydown", (e) => {
    if (["ArrowRight", "ArrowDown", " ", "PageDown"].includes(e.key)) { e.preventDefault(); next(); }
    else if (["ArrowLeft", "ArrowUp", "PageUp"].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === "Home") show(0, true);
    else if (e.key === "End")  show(total - 1, true);
    else if (e.key === "f" || e.key === "F") {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
      else document.exitFullscreen?.();
    }
  });

  // click zones (ignore clicks on links / buttons)
  document.addEventListener("click", (e) => {
    if (e.target.closest("a,button,pre,.no-advance")) return;
    const x = e.clientX / window.innerWidth;
    if (x > 0.6) next(); else if (x < 0.12) prev();
  });

  // touch swipe
  let sx = 0;
  document.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener("touchend", (e) => {
    const dx = e.changedTouches[0].clientX - sx;
    if (Math.abs(dx) > 60) (dx < 0 ? next : prev)();
  }, { passive: true });

  // nav buttons
  document.querySelector(".nav .up")?.addEventListener("click", prev);
  document.querySelector(".nav .down")?.addEventListener("click", next);

  show(idx, false);
})();
