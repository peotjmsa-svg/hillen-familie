// Kaart met plaatsen uit de stamboom (Leaflet + OpenStreetMap).
(function () {
  "use strict";

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function yearsLabel(p) {
    const b = p.birth_year != null ? p.birth_year : "?";
    const d = p.death_year != null ? p.death_year : "";
    return d ? `${b}–${d}` : `${b}`;
  }

  const ROLE_LABEL = { geboren: "geboren", overleden: "overleden", woonachtig: "woonachtig" };

  Promise.all([fetch("data/stamboom.json").then((r) => r.json()), fetch("data/plaatsen.json").then((r) => r.json())])
    .then(([stamboom, plaatsen]) => {
      const map = L.map("map").setView([51.6, 5.8], 7);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-bijdragers',
      }).addTo(map);

      // Group people by place.
      const byPlace = {};
      Object.values(stamboom.people).forEach((p) => {
        (p.place_events || []).forEach((ev) => {
          if (!ev.place) return;
          byPlace[ev.place] = byPlace[ev.place] || [];
          byPlace[ev.place].push({ person: p, role: ev.role, year: ev.year });
        });
      });

      const bounds = [];
      Object.keys(byPlace).forEach((placeName) => {
        const geo = plaatsen[placeName];
        if (!geo || geo.lat == null || geo.lon == null) return;
        const entries = byPlace[placeName];
        const radius = Math.min(8 + entries.length * 1.5, 26);
        const marker = L.circleMarker([geo.lat, geo.lon], {
          radius,
          color: "#7a1f22",
          weight: 2,
          fillColor: "#d9ae5c",
          fillOpacity: 0.75,
        }).addTo(map);

        const uniquePeople = [];
        const seen = new Set();
        entries.forEach((e) => {
          if (!seen.has(e.person.id)) {
            seen.add(e.person.id);
            uniquePeople.push(e);
          }
        });
        uniquePeople.sort((a, b) => (a.year || 9999) - (b.year || 9999));

        const listHtml = uniquePeople
          .slice(0, 25)
          .map(
            (e) =>
              `<li>${escapeHtml(e.person.name)} — ${ROLE_LABEL[e.role] || e.role} (${yearsLabel(e.person)})${
                e.person.occupation ? ", " + escapeHtml(e.person.occupation) : ""
              }</li>`
          )
          .join("");
        const more = uniquePeople.length > 25 ? `<li><em>+ ${uniquePeople.length - 25} andere(n)</em></li>` : "";

        marker.bindPopup(
          `<h4>${escapeHtml(placeName)}</h4><p style="margin:0 0 0.3rem;">${uniquePeople.length} familielid/leden</p>` +
            `<ul>${listHtml}${more}</ul>`
        );
        bounds.push([geo.lat, geo.lon]);
      });

      if (bounds.length) {
        map.fitBounds(bounds, { padding: [30, 30] });
      }
    })
    .catch((err) => {
      document.getElementById("map").innerHTML =
        '<p style="padding:2rem;color:#7a1f22;">Kon de kaartgegevens niet laden.</p>';
      console.error(err);
    });
})();
