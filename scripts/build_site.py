#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the static HTML pages for the Familie Hillen website.

Run after parse_gedcom.py and geocode_places.py:
    python scripts/build_site.py

This writes index.html, stamboom.html, wapen.html, artikelen.html,
artikelen/<slug>.html (x4) and kaart.html at the repository root.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_ITEMS = [
    ("index.html", "Home"),
    ("stamboom.html", "Stamboom"),
    ("wapen.html", "Familiewapen"),
    ("artikelen.html", "Artikelen"),
    ("kaart.html", "Kaart"),
    ("plekken.html", "Plekken"),
    ("onderzoek.html", "Onderzoek"),
]

NAV_TOGGLE_SCRIPT = """<script>
document.getElementById('nav-toggle').addEventListener('click', function() {
  this.classList.toggle('open');
  document.getElementById('main-nav').classList.toggle('open');
});
</script>"""

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&'
    'family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">'
)


def rel(depth, path):
    return ("../" * depth) + path


def nav_html(active, depth):
    items = []
    for href, label in NAV_ITEMS:
        cls = ' class="active"' if href == active else ""
        items.append(f'<li><a href="{rel(depth, href)}"{cls}>{label}</a></li>')
    return "\n        ".join(items)


def base_page(*, title, description, active_nav, body_html, depth=0, extra_head="", extra_scripts=""):
    css = rel(depth, "css/style.css")
    home = rel(depth, "index.html")
    scripts = "\n".join(s for s in (NAV_TOGGLE_SCRIPT, extra_scripts,
                                     f'<script src="{rel(depth, "js/lightbox.js")}"></script>') if s)
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Familie Hillen</title>
<meta name="description" content="{description}">
{FONT_LINK}
<link rel="stylesheet" href="{css}">
{extra_head}
</head>
<body>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{home}">Familie Hillen <small>Stamboom &amp; archief</small></a>
    <button class="nav-toggle" id="nav-toggle" type="button" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" id="main-nav">
      <ul>
        {nav_html(active_nav, depth)}
      </ul>
    </nav>
  </div>
</header>
<main>
{body_html}
</main>
<footer class="site-footer">
  <div class="container">
    <span>&copy; Familie Hillen — persoonlijk archiefproject, samengesteld uit de familie-stamboom en historische bronnen.</span>
    <span>Kaartgegevens &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>-bijdragers</span>
  </div>
</footer>
{scripts}
</body>
</html>
"""


def write(path, html):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(html, encoding="utf-8")
    print(f"geschreven: {path}")


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def build_home(stats):
    body = f"""
<section class="hero container">
  <svg class="hero-crest" viewBox="0 0 100 120" aria-hidden="true">
    <path d="M50 4 L92 16 V56 C92 90 72 108 50 116 C28 108 8 90 8 56 V16 Z"
          fill="#fffdf6" stroke="#b8862f" stroke-width="3"/>
    <path d="M50 4 L92 16 V56 C92 90 72 108 50 116 C28 108 8 90 8 56 V16 Z"
          fill="none" stroke="#7a1f22" stroke-width="1.2" transform="scale(0.93)" transform-origin="50 60"/>
    <text x="50" y="68" text-anchor="middle" font-family="Playfair Display, serif" font-size="30" fill="#7a1f22">H</text>
  </svg>
  <p class="kicker">Sinds 1380 · Roermond en verder</p>
  <h1>Familie Hillen</h1>
  <p class="lede">Een digitaal familiearchief: {stats['individuals']} voorouders in de stamboom, verhalen over
  vier familiebedrijven van boterfabriek tot sigarenfabriek, en een kaart van de plaatsen waar de Hillens
  hebben geleefd en gewerkt.</p>
</section>

<section class="section container">
  <div class="teaser-grid">
    <a class="teaser-card" href="stamboom.html">
      <span class="icon">🌳</span>
      <h3>Stamboom</h3>
      <p>Verken de familielijn vanaf stamvader Diederik Hillen (ca. 1380) tot vandaag, met een doorzoekbare,
      interactieve boom.</p>
      <span class="go">Bekijk de stamboom →</span>
    </a>
    <a class="teaser-card" href="wapen.html">
      <span class="icon">🛡️</span>
      <h3>Familiewapen</h3>
      <p>Nog te bevestigen: is er een officieel Hillen-wapen? Deze plek staat gereserveerd voor zodra het
      gevonden is.</p>
      <span class="go">Meer informatie →</span>
    </a>
    <a class="teaser-card" href="artikelen.html">
      <span class="icon">📜</span>
      <h3>Artikelen</h3>
      <p>Vier familiebedrijven uitgelicht: een boterfabriek, een ijzergieterij, een pijpenfabriek en de oudste
      sigarenfabriek van Nederland.</p>
      <span class="go">Lees de verhalen →</span>
    </a>
    <a class="teaser-card" href="kaart.html">
      <span class="icon">🗺️</span>
      <h3>Kaart</h3>
      <p>Een kaart van {stats['places']} plaatsen in Nederland, België en daarbuiten waar de familie Hillen
      woonde, werkte of trouwde.</p>
      <span class="go">Open de kaart →</span>
    </a>
  </div>
</section>

<section class="section alt">
  <div class="container narrow" style="text-align:center;">
    <h2>Over dit archief</h2>
    <p>Deze website is samengesteld uit een GEDCOM-stamboombestand ({stats['individuals']} personen,
    {stats['families']} gezinnen) en vier onderzochte familiedossiers over Hillen-ondernemingen door de eeuwen
    heen. Alle genealogische gegevens en historische feiten komen rechtstreeks uit die bronnen — zie de
    verantwoording onderaan elk artikel.</p>
  </div>
</section>
"""
    write("index.html", base_page(
        title="Home",
        description="Digitaal familiearchief van de familie Hillen: stamboom, familiewapen, artikelen en kaart.",
        active_nav="index.html",
        body_html=body,
    ))


# ---------------------------------------------------------------------------
# Familiewapen
# ---------------------------------------------------------------------------

def build_wapen():
    body = """
<section class="section container">
  <div class="section-head">
    <p class="kicker">Nog te bevestigen</p>
    <h1>Het familiewapen</h1>
  </div>
  <div class="wapen-shell">
    <svg class="shield-placeholder" viewBox="0 0 200 240" role="img" aria-label="Lege wapenschild-omtrek">
      <path d="M100 8 L184 32 V112 C184 176 144 216 100 232 C56 216 16 176 16 112 V32 Z"
            fill="#fffdf6" stroke="#b8862f" stroke-width="4" stroke-dasharray="10 8"/>
      <line x1="100" y1="40" x2="100" y2="190" stroke="#d8c7a0" stroke-width="1.5"/>
      <line x1="45" y1="80" x2="155" y2="80" stroke="#d8c7a0" stroke-width="1.5"/>
      <text x="100" y="130" text-anchor="middle" font-family="Playfair Display, serif" font-size="20"
            fill="#b8862f">?</text>
    </svg>
    <p class="narrow">
      In het familiedossier en de stamboomgegevens is tot nu toe <strong>geen bevestigd heraldisch wapen</strong>
      van de familie Hillen teruggevonden — alleen bedrijfsemblemen zoals het beeldmerk "Het Roode Anker" van de
      Delftse sigarenfabriek, die bij de bedrijfsgeschiedenis in het artikel over die fabriek horen en niet als
      familiewapen gelden.
    </p>
    <p class="narrow">
      Deze pagina is bewust gereserveerd zodat het wapen later eenvoudig toegevoegd kan worden, bijvoorbeeld na
      onderzoek bij de Hoge Raad van Adel, het Centraal Bureau voor Genealogie, of een regionaal
      heraldisch register.
    </p>
    <div class="howto-box">
      <h3>Hoe voeg je het wapen later toe?</h3>
      <ol>
        <li>Plaats de afbeelding (bij voorkeur SVG of een hoge-resolutie PNG) in
          <code>assets/images/wapen/hillen-wapen.png</code>.</li>
        <li>Open <code>wapen.html</code> en vervang de <code>&lt;svg class="shield-placeholder"&gt;</code>-blok
          door <code>&lt;img src="assets/images/wapen/hillen-wapen.png" alt="Wapen familie Hillen"&gt;</code>.</li>
        <li>Voeg eronder een korte bronvermelding toe (wie heeft het wapen geregistreerd, en wanneer).</li>
      </ol>
    </div>
  </div>
</section>
"""
    write("wapen.html", base_page(
        title="Familiewapen",
        description="Het Hillen-familiewapen: nog niet bevestigd. Deze pagina is gereserveerd voor zodra het gevonden is.",
        active_nav="wapen.html",
        body_html=body,
    ))


def build_stamboom(stats):
    body = f"""
<section class="section container">
  <div class="section-head">
    <p class="kicker">{stats['individuals']} personen · {stats['families']} gezinnen</p>
    <h1>De stamboom</h1>
    <p class="narrow" style="margin:0 auto;">Klik op een naam voor details, zoek op naam, of scrol/sleep om de
    boom te verkennen. Stamvader is Diederik (Hendrik/Dederik) Hillen, geboren rond 1380 in Roermond.</p>
  </div>

  <div class="view-toggle">
    <button id="view-tree-btn" class="active" type="button">Boomweergave</button>
    <button id="view-list-btn" type="button">Alfabetische lijst</button>
  </div>

  <div id="tree-view">
    <div class="tree-toolbar">
      <input type="search" id="person-search" placeholder="Zoek een naam, bijv. &quot;Alexander Hillen&quot;…" autocomplete="off">
      <div id="search-results"></div>
      <button id="reset-view-btn" type="button">Reset weergave</button>
      <button id="expand-all-btn" type="button" class="secondary">Alles uitklappen</button>
    </div>
    <div id="tree-wrap">
      <svg id="tree-svg"></svg>
    </div>
  </div>

  <div id="list-view">
    <div id="alpha-list" class="alpha-list"></div>
  </div>

  <div id="detail-panel"></div>
</section>
"""
    extra_scripts = (
        '<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>\n'
        '<script src="js/stamboom.js"></script>'
    )
    write("stamboom.html", base_page(
        title="Stamboom",
        description="Interactieve stamboom van de familie Hillen, vanaf stamvader Diederik Hillen (ca. 1380).",
        active_nav="stamboom.html",
        body_html=body,
        extra_scripts=extra_scripts,
    ))


def build_kaart():
    body = """
<section class="section container">
  <div class="section-head">
    <p class="kicker">Waar de familie Hillen leefde</p>
    <h1>De kaart</h1>
    <p class="narrow" style="margin:0 auto;">Elke marker is een plaats uit de stamboomgegevens — geboorte,
    overlijden of woonplaats. Klik op een marker voor de bijbehorende familieleden.</p>
  </div>
  <div id="map"></div>
  <p class="map-legend">Plaatsen zijn automatisch gegeocodeerd op basis van de plaatsnaam in de stamboom;
  bij twijfelgevallen (bijv. verouderde plaatsnamen) kan de marker bij benadering staan. Eén plaats
  ("Koestein") kon niet betrouwbaar worden gelokaliseerd en ontbreekt daarom op de kaart.</p>
</section>
"""
    extra_head = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css">'
    extra_scripts = (
        '<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>\n'
        '<script src="js/kaart.js"></script>'
    )
    write("kaart.html", base_page(
        title="Kaart",
        description="Interactieve kaart van plaatsen waar de familie Hillen woonde, werkte of trouwde.",
        active_nav="kaart.html",
        body_html=body,
        extra_head=extra_head,
        extra_scripts=extra_scripts,
    ))


def main():
    stamboom = json.loads((ROOT / "data" / "stamboom.json").read_text(encoding="utf-8"))
    stats = stamboom["stats"]
    build_home(stats)
    build_wapen()
    build_stamboom(stats)
    build_kaart()


if __name__ == "__main__":
    main()
