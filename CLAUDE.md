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

## Onderzoeksnotities
- `onderzoek/`: per onderwerp wat gevonden is, wat doorzocht is zonder resultaat, en wat nog open staat. Lees het relevante
  bestand voordat je verder zoekt, en werk het bij aan het eind van elke onderzoekssessie.
  - `onderzoek/baronnen.md`: Ludwig Augustin en Louis (Châtelet, Beierse officieren, Roermond 1781).
  - `onderzoek/op-te-vragen.md`: lijst van scans, akten en boeken om op te vragen, per instantie (afvinken wat binnen is).
  - `onderzoek/andere-hillens.md`: naamgenoten waarvan niet bewezen is dat ze familie zijn (Tiroolse jagermeester Jan Hillen
    "Kniepis" en de Van Hilles van Megen, heren van Louverval, overige). Niet in de stamboom zetten zonder bewijs.

## Open punten
- Gezin Joannes Hillen × Helena Vorstermans: geen akten online.
- ~~Caspar Hillen: sterfjaar 1789 botst met de akte van 1818.~~ Opgelost 9-10-2026: Caspar overleed 4-6-1789; zijn weduwe
  Theodora Sanders hertrouwde 1790 met Joannes Wilhelmus Linches en stierf 1818 (Land van Kessel).
- Aansluiting Johannes Hillen (Sevenum, P0063) op burgemeester Johan (P0041) rust alleen op de piramide; de parenteel begint bij
  Johannes zonder ouders. Ook het tweede huwelijk van Joannes (P0082) met Elisabeth Lemmen is niet bewezen (Land van Kessel: "mogelijk").
- Ongeveer 90 personen van vóór 1780 zonder jaren (doopboeken, bv. FamilySearch via de browser van de gebruiker).
