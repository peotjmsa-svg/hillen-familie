# Hillen stamboom — werkwijze

Statische site (GitHub Pages vanaf `main`). Antwoord de gebruiker in het Nederlands. Commit en push na elke afgeronde ronde.

## Data
- `data/stamboom.json`: `people` (id `@P0001@`, name, sex, birth_year, death_year, occupation, note, place, place_events[{place,role,year}], sources[], children[]), `families` (`@F…@`: husb, wife, chil, marr_date "24 MAY 1856", marr_place), `places`, `stats`.
- Nieuw kind: toevoegen aan `families[..].chil` én aan `children` van beide ouders. Nieuwe id = hoogste nummer + 1.
- Schrijven: `json.dumps(d, ensure_ascii=False, indent=1)`, `open(..., "w", encoding="utf-8", newline="\r\n")`. Werk `stats` bij, en de tellingen in `index.html` en `stamboom.html`.
- Nieuwe plaats in `place_events`: geocode via Nominatim (1 req/s) naar `data/plaatsen.json`, anders ontbreekt hij op de kaart.
- In notities staan exacte data ("Geboren Grave 30-9-1856") en de bron in `sources`.

## Zoekgereedschap (`scripts/`)
- `python scripts/oa_zoek.py "Naam Hillen"`: Open Archieven zoeken; geeft record-id's (`rhl:…`, `bhi:…`).
- `bash scripts/oa_akte.sh <id> …`: volledige akte (ouders, partner, leeftijd, beroep).
- `python scripts/oa_gezin.py "Hillen & Achternaamvrouw"`: alle akten van een echtpaar.
- `archivsuche_nrw.py`, `archief_screenshot.py`: Duitse archieven (archive.nrw.de). `ddb_zoek.py`: Deutsche Digitale Bibliothek API.
- `commons_zoek.py` / `commons_info.py`: vrije foto's op Wikimedia Commons (licentie in bijschrift).
- `lees_open_tabblad.py`: leest tabbladen die de gebruiker zelf open heeft in Chrome (debugpoort 9223). Alleen lezen, nooit navigeren.
  Uitzondering: in dat debugvenster mag Claude op elke site vrij bladeren en navigeren zolang de gebruiker daar is ingelogd (inloggen doet de gebruiker). Menselijk tempo, geen bulkdownloads, nooit anti-botbescherming omzeilen; bij captcha, loginscherm of fout stoppen en vragen.
- Gebruik curl in plaats van Python-urllib (SSL-fout). Test de site via `python -m http.server 8765`, niet via file://.

## Regels
- Alleen zekere koppelingen toevoegen: ouders of partner in de akte moeten overeenkomen. Tegenstrijdigheden noteren, niet stil aanpassen.

## Open punten
- Gezin Joannes Hillen × Helena Vorstermans: geen akten online.
- Caspar Hillen: sterfjaar 1789 botst met de akte van 1818.
- Ongeveer 90 personen van vóór 1780 zonder jaren (doopboeken, bv. FamilySearch via de browser van de gebruiker).
