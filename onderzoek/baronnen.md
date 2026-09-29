# Onderzoeksnotities: de laatste baronnen van de Helden-tak

Stand na de sessie van 29-9-2026. Alles wat hier als "gevonden" staat, is gelezen in de bron. Wat "vermoeden" heet, is dat ook.
Wat al op de site staat: `plekken.html` (kaart `#chatelet`, `#kinderen`) en de persoonsnotities in `data/stamboom.json`
(P0084–P0088, P0298–P0302).

## 1. Ludwig Augustin, de laatste baron (P0298)

### Gevonden en verwerkt
- **Doopregister Châtelet 1704–1721** (AGATHA, register `524_0697_001_03057_000`, 170 beelden) volledig doorgelezen:
  - beeld 75: doop Louis (Ludovicus Augustinus Maria), **13-9-1711** (niet 1712);
  - beeld 94: doop Maria Catharina, **25-4-1713**, peetouders Joannes Baptista en Catharina le Clercq;
  - beeld 115: doop Maria Anna Carola, **14-2-1715**, peetouders Nicolas Goblet en Oda Puissant "namens de barones De Kleisten".
    Zij is de "D. Maria Carola Anna d'Hilem, innupta" die op 22-7-1737 sterft;
  - beeld 78: 21-12-1711 Ludwig Augustin peter van Ludovicus Joseph, kind van Augustinus Bonhomme en Catharina Leclercq;
  - beeld 89: 20-11-1712 "dno barone de Hillen" peter van Ludovicus Augustinus Histon.
- **Beierse context**: in Châtelet lag 1702–1714 een garnizoen van het Beierse leger van Max Emanuel (regimenten d'Arco en De Kleist).
  In het register: graaf d'Arco (18-12-1711), kapitein Joannes Petrus Denis (19-12-1711), "Joannes Balduinus de Thier, maior regimenti
  d'Arco" (beeld 90, 5-12-1712), baron Ewald de Kleist × Maria Anna de Manteuffel (januari 1714), soldaten "in regimento d'Arco"
  (beelden 169–170). Ludwig Augustin was vrijwel zeker officier in Beierse of Keulse dienst; rang en regiment niet gevonden.
- **Habets, Geschiedenis van het bisdom Roermond III (1892), blz. 127** (Google Books id `fvr2QOAkH_oC`): in 1781 benoemden
  "Jan Nicolaas Goblet en Joseph Leclercq, als erfgenamen van Lambertina Leclercq, weduwe van Ludovicus Augustinus baron de Hillen"
  een kandidaat-cantor voor de domkerk van Roermond. Dat recht hoorde bij de afstammelingen van Reiner van Hillen te Helden
  (P0061, regeling met het kapittel 3-6-1600). Afgewezen; de barons von Bolland (afstammelingen van Anna Hillen, P0086) wonnen.
  Gevolg: bewijs dat Ludwig Augustin van de Helden-tak afstamt; aanwijzing (geen bewijs) dat Louis zonder nakomelingen stierf.

### Doorzocht zonder resultaat
- Oostenrijks Staatsarchief (archivinformationssystem.at): geen Hyllen/Hilen; alleen niet-verwante Hillens.
- Hofkriegsrat-index 1710 (Hungaricana, `KA_HKR_462_1710E`, "Hi" op blz. 151–153): geen Hillen.
- Oostenrijkse officierskaartenbak 1740–1820 (FamilySearch catalogus 106245, film 7683657 "Hess"): geen Hillen tussen Hillebrandt en Hiller.
- Deutsche Digitale Bibliothek, Gallica (exacte zoekopdrachten), Google Books: niets over zijn legerdienst.
- Staudinger, Geschichte des kurbayerischen Heeres: alleen deel 1 (1651–1679) online, niet het deel 1680–1726.

### Open
- Beierse officierslijsten (Bayerisches Hauptstaatsarchiv Abt. IV Kriegsarchiv) staan niet online. Gebruiker wil geen brief.
- Louis: huwelijksregister Châtelet 1730–1764 en doopregister 1738–1794 nog niet systematisch doorzocht.
- ANNO (Wiener Zeitung) heeft treffers "Hillen" 28-2-1733, 20-11-1771 en "Hyllen" 3-9-1746; niet gelezen (Cloudflare-check).

## 2. Andere Hillens (familieband onbewezen)
Zie `onderzoek/andere-hillens.md`: de Tiroolse jagermeester Jan Hillen "Kniepis", de Van Hilles van Megen en Groesbeek,
de heren van Louverval en andere naamgenoten.

## Werkwijze die werkte (debugvenster, poort 9223)
- AGATHA-scans rechtstreeks via IIIF: `https://i3f.arch.be/iiif/524/524_0697_001/524_0697_001_{register}_000/524_0697_001_{register}_000_0_{nnnn}.jp2/full/{breedte},/0/default.jpg`
  (ophalen via de browsersessie, `ctx.request.get`). Drie pagina's naast elkaar in één afbeelding lezen gaat snel.
- Hungaricana (Hofkriegsrat-boeken): beeld zit in `canvas.page-canvas`, uitlezen met `toDataURL`.
- Regesta Imperii: zoekveld `#searchstring`, knop `#submit`; detailpagina's hebben de volledige tekst en voetnoten.
- Google Books: `books?id=ID&pg=PA127&output=text` geeft tekst bij volledige weergave; `books?id=ID&q=term` toont fragmenten.
- Geblokkeerd (niet omzeilen): Gallica soms robotcheck, Geneanet/ANNO Cloudflare (gebruiker klikt zelf), Tessmann 403,
  Mémoire des hommes in onderhoud.
