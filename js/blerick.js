// Kaart van Blerick met huizen, bedrijven en foto's van de familie Hillen (Leaflet + OpenStreetMap).
(function () {
  "use strict";

  const COLOR = { wonen: "#7a1f22", bedrijf: "#b8862b", foto: "#2f5d8a" };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function linkHtml([label, url]) {
    const ext = /^https?:/.test(url) ? ' target="_blank" rel="noopener"' : "";
    return `<a href="${escapeHtml(url)}"${ext}>${escapeHtml(label)}</a>`;
  }

  function popupHtml(p) {
    const img = p.img ? `<img src="${escapeHtml(p.img)}" alt="" style="width:100%;max-height:160px;object-fit:cover;margin:0.3rem 0;border-radius:4px">` : "";
    const links = p.links.map((l) => `<li>${linkHtml(l)}</li>`).join("");
    return `<h4>${escapeHtml(p.title)}</h4><p style="margin:0;font-size:0.8rem;color:#666">${escapeHtml(p.when)}</p>` +
      `${img}<p style="margin:0.3rem 0">${escapeHtml(p.text)}</p><ul>${links}</ul>`;
  }

  fetch("data/blerick.json").then((r) => r.json()).then((points) => {
    const map = L.map("map").setView([51.3655, 6.151], 16);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-bijdragers',
    }).addTo(map);

    const list = document.getElementById("blerick-lijst");
    const bounds = [];
    points.forEach((p, i) => {
      const marker = L.circleMarker([p.lat, p.lon], {
        radius: 10,
        color: COLOR[p.cat] || "#333",
        weight: 3,
        dashArray: p.approx ? "4 4" : null,
        fillColor: COLOR[p.cat] || "#333",
        fillOpacity: 0.55,
      }).addTo(map).bindPopup(popupHtml(p), { maxWidth: 300 });
      marker.bindTooltip(p.title);
      bounds.push([p.lat, p.lon]);

      const item = document.createElement("p");
      item.innerHTML = `<a href="#map" data-i="${i}"><strong>${escapeHtml(p.title)}</strong></a> · ${escapeHtml(p.when)}`;
      item.querySelector("a").addEventListener("click", () => {
        map.setView([p.lat, p.lon], 18);
        marker.openPopup();
      });
      list.appendChild(item);
    });
    map.fitBounds(bounds, { padding: [30, 30] });
  });
})();
