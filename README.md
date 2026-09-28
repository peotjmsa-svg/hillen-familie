# Familie Hillen

Een statische, digitale familiewebsite voor de familie Hillen: een interactieve stamboom, vier historische
familiebedrijf-artikelen, een kaart van plaatsen waar de familie leefde, en een gereserveerde plek voor het
familiewapen zodra dat gevonden is.

Live: zie de GitHub Pages-link in de repository "About"-sectie.

## Inhoud

- `index.html`, `stamboom.html`, `wapen.html`, `artikelen.html`, `kaart.html` — de vijf hoofdpagina's.
- `artikelen/*.html` — de vier familiebedrijf-artikelen (boterfabriek Roermond, ijzergieterij Blerick,
  pijpenfabriek Bree, sigarenfabriek Delft).
- `css/style.css` — gedeelde stijl.
- `js/stamboom.js` — D3.js-stamboomvisualisatie (laadt `data/stamboom.json`).
- `js/kaart.js` — Leaflet/OpenStreetMap-kaart (laadt `data/stamboom.json` en `data/plaatsen.json`).
- `data/stamboom.json` — voorverwerkte stamboomgegevens (personen, gezinnen, plaatsen), gegenereerd uit het
  GEDCOM-bestand door `scripts/parse_gedcom.py`.
- `data/plaatsen.json` — gecachte geocoderesultaten (Nominatim/OpenStreetMap) per plaatsnaam, gegenereerd door
  `scripts/geocode_places.py`.
- `assets/images/artikelen/` — voor het web verkleinde/gecomprimeerde artikelfoto's.

De site is volledig statisch: geen backend, geen database, geen build-stap nodig om te *serveren* — GitHub
Pages kan de repository direct als root serveren.

## Techniekkeuzes

- **Geen framework/bundler.** Losse HTML/CSS/vanilla-JS-bestanden, met D3.js en Leaflet.js via CDN
  (jsdelivr). Dit hield de deploy simpel: GitHub Pages serveert de `main`-branch direct, zonder
  Actions-buildstap.
- **Python-voorbewerkingsscripts** (`scripts/`) zijn eenmalig uitgevoerd en hun output (`data/*.json`,
  `assets/images/artikelen/*`) is gecommit. De live site draait dus nooit zelf GEDCOM-parsing of geocoding.
- **Geocoding via Nominatim** (OpenStreetMap), met een beschrijvende User-Agent en max. 1 request/seconde,
  eenmalig uitgevoerd en gecached in `data/plaatsen.json`.

## Site opnieuw genereren

Nodig: de originele bronmap `raw/` (GEDCOM-export + artikel-PDF's, niet meegecommit — zie `.gitignore`),
Python 3 met `Pillow`.

```bash
python scripts/parse_gedcom.py      # -> data/stamboom.json
python scripts/geocode_places.py    # -> data/plaatsen.json (roept Nominatim aan, ~1 req/sec)
python scripts/build_site.py        # -> index.html, stamboom.html, wapen.html, kaart.html
python scripts/build_articles.py    # -> artikelen.html, artikelen/*.html
```

De artikelfoto's in `assets/images/artikelen/` zijn handmatig verkleind/gecomprimeerd (max ~1600px,
JPEG-kwaliteit ~82) uit de originele PDF-scans in `raw/articles/`; er is geen apart her-uitvoerbaar script
voor omdat het eenmalig werk was.

## Het familiewapen

Er is (nog) geen bevestigd heraldisch wapen van de familie Hillen gevonden — alleen bedrijfsemblemen zoals
"Het Roode Anker" van de Delftse sigarenfabriek, die bij dat artikel horen en niet als familiewapen gelden.
`wapen.html` is een bewuste, duidelijk gelabelde placeholder. Om het echte wapen later toe te voegen:

1. Zet de afbeelding in `assets/images/wapen/hillen-wapen.png` (SVG of hoge-resolutie PNG heeft de voorkeur).
2. Vervang in `wapen.html` het `<svg class="shield-placeholder">`-blok door
   `<img src="assets/images/wapen/hillen-wapen.png" alt="Wapen familie Hillen">`.
3. Voeg een korte bronvermelding toe (wie heeft het wapen geregistreerd/bevestigd, en wanneer).

## Genealogische brongegevens

Alle namen, data en familierelaties komen rechtstreeks uit `raw/gedcom/stamboom-hillen.ged.txt`
(GEDCOM 5.5.1, 271 personen, 80 gezinnen). Alle historische feiten in de artikelen komen uit de vier
onderzochte familiedossiers in `raw/articles/`; zie de bronnenlijst onderaan elk artikel voor de
oorspronkelijke bronnen.

## Duitse archieven doorzoeken (archive.nrw.de)

Het portaal archive.nrw.de laadt zijn zoekresultaten via JavaScript uit een JSON-dienst. `scripts/archivsuche_nrw.py`
roept die dienst rechtstreeks aan, zodat je zonder de Duitse website kunt zoeken:

```bash
python scripts/archivsuche_nrw.py "Hillen Sülz"
python scripts/archivsuche_nrw.py "Hyllen" --pages 3 --out raw/archivsuche_hyllen.json
```

Per treffer toont het script de datering, het archief, de signatuur, een directe link en de volledige (Duitse)
beschrijving. Zoek ook op spellingsvarianten: Hillen, Hyllen, Hijllen, "Rillen" (OCR-fout). Laat de uitvoer
vertalen door Claude, of open de link in Chrome en kies rechtsklik → "Vertalen naar het Nederlands". De website zelf
heeft ook een Nederlandse interface (taalkeuze rechtsboven), maar de archiefbeschrijvingen blijven Duits.

Screenshots van een archiefbeschrijving (voor de site) maak je met `scripts/archief_screenshot.py`
(vereist `pip install playwright` en een lokale Chrome):

```bash
python scripts/archief_screenshot.py assets/images/archief "att1645|Attendorn|https://www.archive.nrw.de/ms/search?link=..."
```
