// Klik op een foto om hem op volledige grootte te bekijken (Esc, klik of × sluit).
(function () {
  "use strict";

  var overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.hidden = true;
  overlay.innerHTML =
    '<button class="lightbox-close" type="button" aria-label="Sluiten">&times;</button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>';
  document.body.appendChild(overlay);

  var bigImg = overlay.querySelector("img");
  var caption = overlay.querySelector("figcaption");
  var lastFocus = null;

  function captionFor(img) {
    var fig = img.closest("figure");
    var fc = fig && fig.querySelector("figcaption");
    if (fc && fc.textContent.trim()) return fc.textContent.trim();
    var hero = img.closest(".article-hero");
    var cap = hero && hero.querySelector(".caption");
    if (cap) return cap.textContent.trim();
    return img.alt || "";
  }

  function open(img) {
    lastFocus = document.activeElement;
    bigImg.src = img.currentSrc || img.src;
    bigImg.alt = img.alt || "";
    caption.textContent = captionFor(img);
    overlay.hidden = false;
    document.body.classList.add("lightbox-open");
    overlay.querySelector(".lightbox-close").focus();
  }

  function close() {
    overlay.hidden = true;
    bigImg.src = "";
    document.body.classList.remove("lightbox-open");
    if (lastFocus) lastFocus.focus();
  }

  function zoomable(img) {
    return img.closest("main") && !img.closest("a") && !img.closest(".lightbox");
  }

  document.querySelectorAll("main img").forEach(function (img) {
    if (!zoomable(img)) return;
    img.classList.add("zoomable");
    img.setAttribute("tabindex", "0");
    img.setAttribute("title", "Klik om te vergroten");
  });

  document.addEventListener("click", function (e) {
    var img = e.target.closest && e.target.closest("img.zoomable");
    if (img) { e.preventDefault(); open(img); return; }
    if (!overlay.hidden && e.target !== bigImg) close();
  });

  document.addEventListener("keydown", function (e) {
    if (!overlay.hidden && e.key === "Escape") { close(); return; }
    if ((e.key === "Enter" || e.key === " ") && document.activeElement &&
        document.activeElement.classList && document.activeElement.classList.contains("zoomable")) {
      e.preventDefault();
      open(document.activeElement);
    }
  });
})();
