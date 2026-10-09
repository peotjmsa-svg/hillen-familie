#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the Artikelen overview page and the four article detail pages.

Content below is reformatted (headings/paragraphs/captions split out) from
raw/articles/<slug>/article.txt — no facts added or changed, only laid out.
Run after build_site.py: python scripts/build_articles.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import ROOT, base_page, write  # noqa: E402

IMG = "assets/images/artikelen"

ARTICLES = [
    {
        "slug": "boterfabriek-roermond",
        "img_dir": "boterfabriek_roermond",
        "title": "De Boterfabriek Hillen-Verbruggen",
        "era": "Roermond · 1879 – 1896",
        "sub": "Van mislukte suikerfabriek tot de derde zuivelfabriek van Nederland",
        "teaser": "Een geveilde suikerfabriek, een Blerickse familie die de sprong waagt, en een pand dat via "
                  "Moutfabriek Limburgia tot op de dag van vandaag overeind staat.",
        "hero": f"{IMG}/boterfabriek_roermond/boterfabriek_roermond_p1_1.jpg",
        "hero_caption": "“Boterfabriek ‘Hillen’ geeft geheimen prijs!” — het pand "
                        "gefotografeerd in 1989, met de karakteristieke schoorsteen en trapgevel. "
                        "(bron: Ruud Lamboo-Louwarts, historieroermond.nl)",
        "facts": [
            ("Gekocht", "12 december 1879, voor 4.500 gulden (notaris Laurens Linssen)"),
            ("Locatie", "Huidige Maria Theresialaan, Roermond — pand staat er nog altijd, nu Moutfabriek Limburgia"),
            ("Compagnon", "Guillaume Hubert Verbruggen, uit Luik"),
            ("Betekenis", "3e zuivelfabriek van Nederland (na Winschoten en Edam)"),
            ("Verkocht", "1896, aan handelsreiziger Louis Beltjens → werd Moutfabriek Limburgia"),
        ],
        "sections": [
            {
                "h": "Een mislukte suikerfabriek als vertrekpunt",
                "p": [
                    "Het pand waar dit verhaal zich afspeelt, begon niet als zuivelfabriek. Rond 1877-1878 "
                    "vestigden Leon Hermans (afkomstig van kasteel Heel) en zijn compagnon Mathis Niessen er "
                    "een suiker- en glucosefabriek. Het werd een financieel debacle: binnen ongeveer een jaar "
                    "ging de onderneming failliet, en de fabriek werd inclusief machines geveild.",
                    "Op de veiling van 23 december 1879 kocht een zekere ‘Alexander Hillen’ een "
                    "kiezelzeef voor 1 gulden — een klein bedrag, maar de bron noemt hem expliciet "
                    "“een latere eigenaar van de fabriek”. Enkele dagen eerder, op 12 december 1879, "
                    "was het pand voor 4.500 gulden overgedragen aan ‘leden van de familie Hillen te "
                    "Grave’, via notaris Laurens Linssen te Roermond.",
                ],
            },
            {
                "h": "Van kunstboter tot moderne zuivelfabriek",
                "img": f"{IMG}/boterfabriek_roermond/boterfabriek_roermond_p2_2.jpg",
                "img_caption": "Origineel briefhoofd: ‘Margarine Boterfabriek Hillen &amp; "
                               "Verbruggen’, telegramadres ‘Hillen Roermond’.",
                "p": [
                    "De nieuwe eigenaars richtten er aanvankelijk geen mouterij op, maar de ‘Margarine- en "
                    "Kunstboterfabriek Hillen-Verbruggen’. Alexander Hillen bleef als vennoot en eigenaar "
                    "nauw bij de onderneming betrokken; zijn compagnon was Guillaume Hubert Verbruggen, "
                    "afkomstig uit Luik.",
                    "Omdat de zaken voorspoedig verliepen, werd op 28 augustus 1883 de eerste steen gelegd voor "
                    "een grootschalige uitbreiding: een hypermoderne stoom-zuivelfabriek onder de firmanaam "
                    "Hillen-Verbruggen. Daarmee werd het de derde zuivelfabriek van heel Nederland, na die van "
                    "Winschoten en Edam — destijds een van de meest winstgevende en modernste sectoren van "
                    "het land, met een sterk groeiende export van Nederlandse boter naar onder meer Engeland en "
                    "Duitsland.",
                    "Een bijzonder detail dat de familie in een veel bredere, internationale zakenwereld "
                    "plaatst: de dochter van compagnon Verbruggen trouwde later met Anton Jurgens — de "
                    "latere margarine-magnaat wiens bedrijf via een fusie mede aan de basis stond van wat "
                    "vandaag Unilever is.",
                ],
            },
            {
                "h": "Verkoop en tweede leven als mouterij",
                "img": f"{IMG}/boterfabriek_roermond/boterfabriek_roermond_p2_3.jpg",
                "img_caption": "Het met klimop begroeide pand als ‘Moutfabriek Limburgia’, met de "
                               "naam nog leesbaar in de gevel.",
                "p": [
                    "In 1896 verkochten de eigenaars de fabriek aan Louis Beltjens, een 38-jarige "
                    "handelsreiziger. Pas onder zijn leiding werd het complex daadwerkelijk omgebouwd tot "
                    "mouterij: de ‘Moutfabriek Limburgia’.",
                    "Tijdens de Tweede Wereldoorlog bezetten de Duitsers de fabriek en gebruikten het complex "
                    "als opslagplaats voor etenswaren en wijn die via de ‘IJzeren Rijn’ vanuit "
                    "Frankrijk naar Mönchengladbach werden vervoerd. In 1945 brandde de houten eesttoren "
                    "af; in 1947 verrees op diezelfde plek de huidige, kenmerkende bakstenen toren. In 1953 "
                    "werd de fabriek nog uitgebreid met een opslagruimte en productieloods.",
                    "In 1974 verhuisde de familie Beltjens en werd de moutfabriek verkocht. Het pand kwam leeg "
                    "te staan en raakte ernstig in verval — ruim dertig jaar lang, pal aan het spoor in "
                    "een Roermondse woonwijk.",
                ],
            },
            {
                "h": "Restauratie tot rijksmonument",
                "img": f"{IMG}/boterfabriek_roermond/boterfabriek_roermond_p3_4.jpg",
                "img_caption": "De vervallen Moutfabriek, met de bakstenen eesttoren uit 1947, vlak vóór "
                               "de restauratie.",
                "p": [
                    "In 2005 kocht Henk Wolters het vervallen complex van de gemeente Roermond. Kern "
                    "Architecten restaureerde het pand met respect voor de geschiedenis tot een duurzame "
                    "werkplek — vandaag de dag hun eigen kantoor, en een gerestaureerd rijksmonument aan "
                    "de Maria Theresialaan.",
                ],
            },
            {
                "h": "Hoe zeker weten we dit? — een woord over bewijsvoering",
                "p": [
                    "De naam ‘Alexander Hillen’ komt in de Roermondse bronnen letterlijk voor, maar "
                    "geen enkele bron zegt met zoveel woorden dat dit dezelfde Alexander Hillen (1821–1898) "
                    "is als de Blerickse voorvader in onze stamboom. We hebben dit stap voor stap onderzocht en "
                    "zijn tot de volgende, onderbouwde inschatting gekomen — waarschijnlijk, maar niet "
                    "100% sluitend bewezen:",
                ],
                "list": [
                    "Geen andere kandidaat gevonden. Er is in Roermond of omstreken geen tweede ‘Alexander "
                    "Hillen’ opgedoken die de rol beter zou verklaren (o.a. gecheckt via een lokale "
                    "begraafplaats-index).",
                    "De tweelingbroer had het al druk elders. Alexanders tweelingbroer Johan runde in exact "
                    "dezelfde jaren (1877–1884) de ijzergieterij in Blerick — dus niet hij, maar "
                    "mogelijk Alexander had de vrije ruimte voor een tweede onderneming in Roermond.",
                    "De ‘familie Hillen te Grave’ is te verklaren. Alexanders broer Jacobus Hillen "
                    "trouwde in 1856 in Herpen (bij Grave) en vestigde zich daar; zijn zoon werd zelfs in Grave "
                    "geboren (1856). Dat verklaart de vermelding in de notariële akte.",
                    "Een blijvende band met Roermond. Een kleinzoon van diezelfde Jacobus werd in 1890 in "
                    "Roermond zelf geboren — een aanwijzing dat deze familietak generaties lang aan de "
                    "stad verbonden bleef.",
                ],
                "p_after": [
                    "Voor volledige zekerheid zou je het originele bevolkingsregister van Roermond "
                    "(1875–1895) of de notariële akte van 12 december 1879 zelf moeten inzien bij het "
                    "Historisch Centrum Limburg — dat is archiefwerk dat niet online te doen is. Tot die "
                    "tijd behandelen we deze koppeling als aannemelijk, en vermelden we expliciet waar het "
                    "bewijs indirect blijft.",
                ],
            },
        ],
        "sources": [
            "HistorieRoermond.nl, ‘Suikerfabriek’ en ‘Boterfabriek “Hillen”’ (foto: Ruud Lamboo-Louwarts)",
            "Kernarchitecten.com, ‘Het HUIS van Kernarchitecten’ (geschiedenis en restauratie Moutfabriek)",
            "Stichting Ruimte Roermond, ‘Monumenten, architectuur, stedenbouw in Limburg’",
            "Genealogie Limburg Wiki, ‘Hermans (Heel)’",
            "Diverse historische krantenberichten via Delpher.nl",
        ],
    },
    {
        "slug": "ijzergieterij-blerick",
        "img_dir": "ijzergieterij_blerick",
        "title": "De IJzergieterij van Johan Hillen",
        "era": "Blerick · 1877 – 1916",
        "sub": "Van kleine machinefabriek tot een van de grootste werkgevers van Blerick",
        "teaser": "Stoommachines, landbouwwerktuigen en een verschoven Maasbrug — het verhaal van een "
                  "fabriek die generaties lang van vader op zonen ging.",
        "hero": f"{IMG}/ijzergieterij_blerick/ijzergieterij_hillen_1_p1_1.jpg",
        "hero_caption": "De Pontanusstraat in Blerick, met de fabriekslocaties met Romeinse cijfers gemarkeerd "
                        "— Hillen begon op de plek waar tegenwoordig winkelcentrum La Plaza staat. "
                        "(bron: Heuijerjans.net)",
        "facts": [
            ("Opgericht", "1877, door Johan (Joannes) Hillen"),
            ("Locatie", "Achter de Pontanusstraat, Blerick — nu de plek van winkelcentrum La Plaza"),
            ("Groei", "24 werknemers (1877) → ca. 100 werknemers (1884)"),
            ("Producten", "Landbouwwerktuigen, stoommachines, schroefbouten, bruggen, boekenrekken"),
            ("Einde", "Faillissement 1910 · verkocht aan familie Holthuis (1916) → werd Geho-pompen"),
        ],
        "sections": [
            {
                "h": "Oprichting: een fabriek voor stoommachines en landbouwwerktuigen",
                "p": [
                    "Op 6 september 1877 richtten Johan Hillen en zijn compagnon Penning aan de overkant van "
                    "de Maas, in Blerick, een kleine machinefabriek op. De Kamer van Koophandel van Venlo "
                    "noteerde in dat jaar dat het bedrijf werkte met een machine van 15 paardenkracht en zich "
                    "toelegde op het vervaardigen van nieuwe en het repareren van oude stoommachines en "
                    "landbouwwerktuigen, en op het maken van schroefbouten en klinknagels. Johan Hillen was op "
                    "dat moment 56 jaar oud — een tweelingbroer van Alexander Hillen, en zelf zoon van de "
                    "Blerickse hoefsmid Alardus Hillen.",
                    "Het bedrijf veranderde in de decennia die volgden meermaals van naam — Hillen & "
                    "Penning, J. Hillen & Zonen, Joh. Hillen & Co. — wat suggereert dat de zonen van "
                    "Johan al vroeg meewerkten in de zaak. In 1884 nam de firma bovendien de allereerste "
                    "ijzergieterij van Blerick over: die van de families Van Boom en Joiris, die dat jaar "
                    "ophield te bestaan omdat er geen opvolger meer was.",
                ],
            },
            {
                "h": "Groei tot grootste werkgever van Blerick",
                "img": f"{IMG}/ijzergieterij_blerick/ijzergieterij_hillen_1_p2_2.jpg",
                "img_caption": "“Poseren in de vorige eeuw voor ‘t fabriek.” Personeel en "
                               "bedrijfsleider van ijzergieterij Hillen, 1895. Productie: ketels en motoren. "
                               "(met dank aan Ruud Merkx, via Heuijerjans.net)",
                "p": [
                    "Binnen zeven jaar groeide het personeelsbestand van 24 naar ongeveer 100 man — een "
                    "verviervoudiging die de fabriek tot een van de grootste werkgevers van Blerick maakte. "
                    "Het assortiment breidde zich sterk uit: van landbouwwerktuigen tot complete bruggen, van "
                    "scheeps- en ketelwerk tot boekenrekken. Vanaf 1884 konden scheeps-, ketel- en "
                    "bruggenmakers er direct aan de slag.",
                    "Een bijzonder detail: rond de eeuwwisseling beschikte Blerick nog niet over elektriciteit. "
                    "Hillen wekte voor de eigen productie zelf stroom op met een generator — en leverde "
                    "daarmee zelfs elektriciteit aan de nabijgelegen pastorie, lang voordat het dorp een "
                    "elektriciteitsnet kreeg.",
                    "In 1886 kreeg “de Blerickse aannemer Joh. Hillen” een prestigieuze opdracht: het "
                    "verschuiven van de bestaande Maasbrug op haar pijlers, zodat er een tweede, parallelle "
                    "brug bij kon komen. De oorspronkelijke brug (1865) was gebouwd voor het "
                    "spoorwegverkeer; na de verschuiving diende hij nog uitsluitend als verkeersbrug voor "
                    "voetgangers en fietsers.",
                ],
            },
            {
                "h": "Een fabriek met een eigen karakter",
                "p": [
                    "De lokale kranten uit die jaren geven een levendig beeld van het dagelijkse reilen en "
                    "zeilen bij Hillen. In 1892 sloegen op een huwelijksfeest in de buurt de vreugdeschoten de "
                    "paarden op hol die een 8.000 kilo wegende, bij Hillen vervaardigde ijzeren brug moesten "
                    "vervoeren — het gevaarte kwam tegen een woonhuis tot stilstand en liet een deel van "
                    "de gevel instorten. In 1910 ging de firma failliet en werd het complete bedrijf publiek "
                    "geveild door de Blerickse notaris Vissers, inclusief het aangrenzende herenhuis, zes "
                    "burgerhuizen, een landbouwerswoning en ruim drie hectare bouw- en weiland. Drie jaar "
                    "later, op 19 november 1913, brandden de gieterij en smelterij bovendien volledig af, "
                    "waardoor vijftig man tijdelijk zonder werk kwamen te zitten.",
                ],
                "img": f"{IMG}/ijzergieterij_blerick/ijzergieterij_hillen_1_p3_3.jpg",
                "img_caption": "Advertentie voor ‘Hillen’s Gas-, Petroleum- en Benzine Motoren’ "
                               "en de IJzer- en Kopergieterij, firma Johan Hillen, Blerick.",
                "p_after": [
                    "In 1906 verscheen zelfs een reclamefolder van 40 pagina's voor de ‘Hillen-motor’ "
                    "— een teken van hoe breed het bedrijf inmiddels adverteerde.",
                ],
            },
            {
                "h": "Van vader op zonen, tot het faillissement",
                "p": [
                    "Toen Johan Hillen op 11 mei 1895 overleed, zetten zijn zonen Henri (Henri Hubert Hillen, "
                    "1852–1914) en Piet de zaak voort. Henri werd directeur en bleef dat tot zijn dood op "
                    "23 oktober 1914 — hij overleed dus nog geen jaar na de verwoestende brand van 1913.",
                    "Na het faillissement van 1910 werd de zaak nog kort voortgezet als naamloze vennootschap, "
                    "maar in 1916 kocht de familie Th. Holthuis uit Veendam ‘Joh. Hillen’s "
                    "IJzergieterij en Machinefabriek’ voor 10.000 gulden.",
                ],
            },
        ],
        "sources": [
            "Heuijerjans.net (Andreas Heuijerjans), ‘Blerick: De IJzergieterijen Van Boom/Joiris, Hillen en "
            "Van den Bergh’ — heuijerjans.blogspot.com/2014/09/blerick-de-ijzergieterijen-van.html",
            "Nederlands IJzermuseum, ‘Overzicht ijzergieterijen in Nederland 1689–2012’ (Dik Nas)",
            "Diverse historische krantenberichten via Delpher.nl",
            "Kamer van Koophandel Limburg, ‘Twee Eeuwen Handel & Nijverheid 1804–2014’",
        ],
    },
    {
        "slug": "pijpenfabriek-bree",
        "img_dir": "pijpenfabriek_bree",
        "title": "De Pijpenfabriek van Bree: Knoedgen → Hillen → Hilson",
        "era": "Bree, België · 1846 – 1980",
        "sub": "Van een Duitse pijpenmakersfamilie tot het merk Hilson (‘Hillen and Sons’)",
        "teaser": "Via een huwelijk kwam een van de laatste twee heidepijpenfabrikanten van de Benelux in "
                  "handen van de familie Hillen — met een politicus als bijvangst.",
        "hero": f"{IMG}/pijpenfabriek_bree/pijpenfabriek_bree_2_p2_1.jpg",
        "hero_caption": "Amerikaanse verkoopadvertentie (Wally Frank) voor de ‘Hilson Fantasia’ — "
                        "“The Modern Hilson... Made in Belgium” — een teken van hoe ver de "
                        "export van het Breese familiebedrijf reikte.",
        "facts": [
            ("Oorsprong", "1846, Maastricht, door Jean Jacques Knödgen — verplaatst naar Bree in 1853"),
            ("In Hillen-handen", "Na WOI, via Jean (Jan) Hillen — kleinzoon van de oprichter"),
            ("Merk", "Hilson (‘Hillen and Sons’), bedacht door zoon Albert na WOII"),
            ("Positie", "Één van slechts twee heidepijpen-fabrikanten van de Benelux (met Gubbels/Big Ben, Roermond)"),
            ("Einde", "1979/80, financiële problemen → overgenomen door Kon. Pijpenfabriek Gubbels"),
        ],
        "sections": [
            {
                "h": "Een Duitse pijpenmaker in Belgisch Limburg — of tóch een Hillen?",
                "p": [
                    "Over wie de fabriek in 1846 precies stichtte, spreken de bronnen elkaar tegen. De "
                    "gespecialiseerde kleipijpen-site Claypipes.nl vertelt een gedetailleerd verhaal over een "
                    "familie Duitse pijpenmakers uit de Westerwald: de broers Jean Jacques en Jacques "
                    "Knödgen, die in 1839 vanuit Chokier naar Luik vertrokken om daar een eigen "
                    "pijpenmakerij te beginnen. In 1846 verliet Jean Jacques Luik voor Maastricht, en "
                    "verhuisde in 1853 naar Bree — de geboorteplaats van zijn vrouw. Pas na de Eerste "
                    "Wereldoorlog zou de fabriek dan, via een huwelijk, in handen van de familie Hillen zijn "
                    "gekomen.",
                    "Pipedia — de belangrijkste internationale referentiesite voor pijpengeschiedenis "
                    "— vertelt het anders: daar staat dat de fabriek in 1846 rechtstreeks werd opgericht "
                    "door ‘Jean-Claude Hillen (andere bronnen: Jean-Paul)’ als handelsonderneming, "
                    "die zich al snel toelegde op pijpen en aanverwante tabaksartikelen. Zelfs Pipedia twijfelt "
                    "dus over de exacte voornaam. We kunnen deze twee versies niet met zekerheid met elkaar "
                    "verzoenen — mogelijk gaat het om twee generaties die door latere bronnen door elkaar "
                    "zijn gehaald, of was er al vóór het huwelijk met de Knödgens al een Hillen "
                    "bij de handel betrokken. Wat zeker is: de fabriek maakte aanvankelijk aarden "
                    "(klei-)pijpen — een assortiment van 187 verschillende modellen, gemerkt met de "
                    "letters ‘JK’ in de hiel.",
                ],
            },
            {
                "h": "Via huwelijk in Hillen-handen",
                "p": [
                    "Door een reeks huwelijken kwam de fabriek na de Eerste Wereldoorlog in handen van Jan "
                    "(Jean) Hillen — een kleinzoon van de oprichter. Jans vader, Albertus Theodorus "
                    "Hubertus (Albert) Hillen (Blerick 1856–1916), was in 1883 in Bree "
                    "getrouwd met Maria Knödgen, dochter of kleindochter van de pijpenfabrikant. Jan zelf, "
                    "geboren op 8 november 1889 in Bree, breidde de fabriek onder zijn leiding verder uit met "
                    "de productie van asbestos- en bruyèrepijpen (heidehouten pijpen) — een "
                    "belangrijke koerswijziging ten opzichte van de traditionele kleipijp.",
                    "Jan Hillen was behalve fabrikant ook een man van aanzien in Bree: hij was schepen van de "
                    "stad, voorzitter van het Rode Kruis afdeling Bree en voorzitter van de commissie van "
                    "onderlinge bijstand. Hij trouwde in 1918 met Josephina Antonetta ‘Maria’ Smets, "
                    "en overleed in 1988 in Bree op de gezegende leeftijd van 99 jaar.",
                ],
            },
            {
                "h": "De zonen: van Hillen naar Hilson",
                "p": [
                    "Na de Tweede Wereldoorlog namen Jans zonen het roer over: Jos nam de verkoop voor zijn "
                    "rekening, Albert de productie. Albert was tijdens de oorlog tolk geweest bij het Britse "
                    "leger, wat hem na de bevrijding een uitgebreid internationaal netwerk opleverde — "
                    "precies wat nodig was om de export op gang te brengen. Voor de merknaam koos hij iets "
                    "simpels dat het bedrijf perfect samenvatte: Hilson, een samentrekking van ‘Hillen "
                    "and Sons’.",
                    "Onder de naam ‘Broers Hillen B.V.’ groeide Hilson in de jaren zestig en zeventig "
                    "uit tot een succesvol merk in machinaal vervaardigde bruyèrepijpen, met name op de "
                    "Duitse markt — waar het beter verkocht dan het eigen ‘Big Ben’-merk van "
                    "branchegenoot Gubbels. De zeldzame, handgemaakte ‘freehand’-pijpen van het "
                    "bedrijf gingen onder een aparte naam de deur uit: Mastro, gesigneerd met ‘A.M. "
                    "Sanoul’. Tegen het einde van de jaren zeventig waren Hillen (Bree) en Gubbels "
                    "(Roermond) de laatst overgebleven twee heidepijpen-fabrikanten van de hele Benelux.",
                    "In 1980 kreeg de firma financiële problemen. De Koninklijke Pijpenfabriek Elbert "
                    "Gubbels uit Roermond nam het bedrijf over, inclusief het merk Hilson — dat destijds "
                    "zelfs beter verkocht dan Gubbels’ eigen Big Ben. Sindsdien worden Hilson-pijpen in "
                    "Roermond gemaakt.",
                ],
            },
            {
                "h": "Een politicus in de familie",
                "p": [
                    "Jan Hillen had ook een broer die een heel andere weg insloeg: Albert Theodore Constant "
                    "Marie Hillen (Bree, 14 februari 1892 – Antwerpen, 13 november 1933) werd advocaat en, "
                    "via de Katholieke Partij, lid van de Belgische Kamer van Volksvertegenwoordigers. Zijn "
                    "rouwprentje omschrijft hem als een man die zijn talenten “van zijn collegejaren af, "
                    "in Studentenbond en Jonge Wacht, met jeugdige geestdrift” ten dienste stelde van de "
                    "Katholieke en Vlaamse zaak. Hij overleed op 41-jarige leeftijd, drie jeugdige kinderen "
                    "achterlatend.",
                ],
            },
            {
                "h": "Hoe zeker weten we dit?",
                "p": [
                    "Dit verhaal steunt op ongewoon stevige grond, met meerdere onafhankelijke bronnen die "
                    "elkaar bevestigen — op de precieze oprichter van 1846 na, waar Claypipes.nl en "
                    "Pipedia elkaar tegenspreken (zie hierboven):",
                ],
                "list": [
                    "De herkomst van het merk ‘Hilson’ (= Hillen and Sons) en de rolverdeling tussen "
                    "Jos en Albert staan woordelijk hetzelfde beschreven op minstens vier onafhankelijke "
                    "pijpenverzamelaars-sites (Pipedia, Rebornpipes, Dutch Pipe Smoker, Al Pascià).",
                    "Het Kamerlidmaatschap van Albert Theodore Constant Marie Hillen is apart bevestigd via de "
                    "officieel gepubliceerde ‘Lijst van Belgische volksvertegenwoordigers "
                    "1831–2002’, met exact dezelfde geboorte- en sterftedata als in het "
                    "familie-rouwprentje.",
                    "De genealogische gegevens (data, huwelijken) komen uit LimMemoriam.be, een "
                    "rouwprentjesverzameling met concrete akte-nummers — het meest betrouwbare soort bron "
                    "die we in dit hele onderzoek zijn tegengekomen.",
                ],
            },
        ],
        "sources": [
            "Pipedia.org, ‘Hilson’ en ‘Gubbels’",
            "Rebornpipes.com, ‘History of the Gubbels Pipe Business’ (Arno van Goor)",
            "DutchPipeSmoker.com, diverse artikelen over Gubbels/Hilson/Big Ben",
            "Al Pascià, ‘Gubbels Factory — Big Ben and Hilson pipes’",
            "Claypipes.nl, ‘Knoedgen (Bree)’ en ‘Bodemvondsten Knoedgen’",
            "LimMemoriam.be, parenteel Albert Theodoor Hubert Hillen (rouwprentjesverzameling Heemkundekring Bree)",
            "Wikipedia / Unionpedia, ‘Lijst van Belgische volksvertegenwoordigers 1831–2002’",
        ],
    },
    {
        "slug": "sigarenfabriek-delft",
        "img_dir": "sigarenfabriek_delft",
        "title": "A. Hillen’s Sigaren- en Tabaksfabrieken",
        "era": "Delft · 1770 – 1937/38",
        "sub": "De oudste sigarenfabriek van Nederland",
        "teaser": "Van een pand ‘het Rode Anker’ aan de Oude Delft tot bijna 700 werknemers en een "
                  "winkelketen van meer dan 120 filialen door heel Nederland.",
        "hero": f"{IMG}/sigarenfabriek_delft/sigarenfabriek_delft_p1_1.jpg",
        "hero_caption": "Omslag van de ‘Pryscourant’ (prijslijst) van Sigarenfabriek A. Hillen, met "
                        "het beeldmerk ‘Het Roode Anker’ — de naam van het pand aan de Oude "
                        "Delft waar alles begon.",
        "facts": [
            ("Opgericht", "1770, door Gerrit (Gerardus) Hillen, Oude Delft / hoek Pepersteeg"),
            ("Merken", "Het Rode Anker · Delftsche Post"),
            ("Piek", "Rond 1920: bijna 700 werknemers · franchiseketen ‘Van Andel’, 120+ winkels"),
            ("Betekenis", "Oudste sigarenfabriek van Nederland · rond 1890 grootste werkgever van Delft"),
            ("Einde", "Februari 1937/38, 300 werknemers — pand verkocht aan firma Braat"),
        ],
        "sections": [
            {
                "h": "De eerste sigarenfabriek van Nederland",
                "p": [
                    "Waar de meeste van de circa 2.500 Nederlandse sigarenfabrieken uit de 19e en 20e eeuw in "
                    "Noord-Brabant stonden, begon de allereerste in Delft. Gerrit Hillen — in onze "
                    "stamboom Gerardus Hillen (1743–1805), een telg uit de Blerickse tak van de familie "
                    "— vestigde zich in 1770 op de hoek van de Oude Delft en de Pepersteeg, in het pand "
                    "‘het Rode Anker’. Hij fabriceerde er aanvankelijk tabak, en later ook sigaren. "
                    "Op 22 februari 1772 kreeg hij van de Schepenen van Delft officieel consent om zijn "
                    "producten te verkopen.",
                    "Het was zijn zoon Albertus Hillen (1774–1834) die de zaak echt tot bloei bracht en "
                    "fors uitbreidde, onder meer met de aankoop van panden aan de Pepersteeg. Na zijn dood "
                    "zette zijn vrouw Anna Maria van Spreeuwenburg de zaak nog vier jaar voort. Bij de "
                    "boedelscheiding van 1835 bleken de bezittingen opvallend breed: naast het woonhuis en "
                    "pakhuis ‘het Rode Anker’ (Oude Delft nr. 63, en aan de Pepersteeg) zou er volgens "
                    "een latere samenvatting zelfs een aardewerkfabriek ‘de Bloempot’ bij hebben gehoord, "
                    "geërfd van vader Gerrit. Dat is twijfelachtig: in het kadaster van 1832 bezat Albertus "
                    "alleen huizen en pakhuizen, geen plateelbakkerij. Hoogstens ging het om een aandeel in "
                    "plateelbakkerij De Vergulde Blompot aan de Molslaan, die in de jaren 1790 in 36 delen "
                    "werd verkocht.",
                ],
            },
            {
                "h": "Van familiebedrijf naar de familie Hioolen",
                "img": f"{IMG}/sigarenfabriek_delft/sigarenfabriek_delft_p2_2.jpg",
                "img_caption": "‘A. Hillen’s Sigarenfabriek Delft, langs de spoorlijn, nabij het "
                               "station.’ De fabriek breidde in de loop der jaren uit tot een langgerekt "
                               "complex.",
                "p": [
                    "Op een fraaie gedenkschotel, gemaakt ter gelegenheid van het 150-jarig bestaan van de "
                    "fabriek, staat een portret van Albertus Hillen afgebeeld — met het opschrift "
                    "‘Albertus Hillen — Fundator Est’ en de jaartallen 1762 en 1922 (een kleine "
                    "onnauwkeurigheid ten opzichte van het officieel gehanteerde oprichtingsjaar 1770, zoals "
                    "wel vaker voorkomt op dit soort jubileumstukken).",
                    "Ergens vóór 1861 kwam de dagelijkse leiding in handen van Albertus Gerardus de Lange "
                    "(geboren 4 mei 1825 te Delft), die op het Oude Delft 63 kwam wonen en directeur van de firma "
                    "Hillen werd. Hij droeg niet de naam Hillen, maar was wel familie: zijn moeder was "
                    "Sara Jacoba Elizabeth Hillen, een dochter van Albertus Hillen (bron: burgerlijke stand "
                    "Delft, via Open Archieven). In 1861 nam Martinus Hioolen "
                    "(1834–1905) de zaak definitief over, mogelijk gemaakt door financiële steun van "
                    "zijn oom Willem Hioolen. De Hioolens kwamen uit een zeer oud geslacht (rond 1490!) en "
                    "waren al generaties eigenaar van de snuifmolens ‘De Lelie’ en ‘De "
                    "Ster’ aan de Kralingse Zoom in Rotterdam — molens die er vandaag de dag nog "
                    "steeds staan, nu als museum.",
                ],
                "img2": f"{IMG}/sigarenfabriek_delft/sigarenfabriek_delft_p2_3.jpg",
                "img2_caption": "Delfts-blauwe gedenkschotel voor het 150-jarig jubileum, met portret van "
                                "Albertus Hillen — ‘Fundator Est’.",
            },
            {
                "h": "Op zijn hoogtepunt: bijna 700 man personeel",
                "img": f"{IMG}/sigarenfabriek_delft/sigarenfabriek_delft_p3_4.jpg",
                "img_caption": "Luchtfoto van het complex langs de spoorlijn, met het grote reclamebord "
                               "‘A. HILLEN DELFT’ pal naast de rails — goed zichtbaar voor elke "
                               "voorbijrijdende trein.",
                "p": [
                    "Martinus bracht een revolutionair idee mee uit de familiehandel: in een tijd van "
                    "stagnerende welvaart bedacht hij een landelijk netwerk van eigen winkelfilialen, om zo "
                    "een vast afzetgebied voor zijn sigaren te garanderen — in plaats van afhankelijk te "
                    "zijn van zelfstandige sigarenwinkeliers die overal hun inkoop deden. Onder de naam Van "
                    "Andel groeide dit uit tot een keten van meer dan 120 sigarenwinkels verspreid over heel "
                    "Nederland, met zelfs een eigen verkoopkantoor in Batavia (Nederlands-Indië).",
                    "Rond 1890 was de tabaksbranche de grootste werkgever van Delft geworden, en rond 1920 "
                    "telde A. Hillen alleen al bijna 700 werknemers. Het bedrijf behoorde tot de drie "
                    "sigarenfabrieken van Nederland die hun personeel het best betaalden, en had al vroeg een "
                    "omvangrijke export naar diverse werelddelen. Tijdens de Eerste Wereldoorlog kocht de "
                    "fabriek zelfs een stuk grond aan, zodat het personeel in tijden van schaarste eigen "
                    "groenten kon verbouwen. Directeur C.N.J. Hioolen was tussen de twee wereldoorlogen actief "
                    "lid van de landelijke commissie die de werking van de merkenwet onderzocht.",
                    "De belangrijkste merken — Het Rode Anker en Delftsche Post — gingen door heel "
                    "Nederland over de toonbank. Tussen 1880 en 1940 waren in Delft zo’n 850 "
                    "sigarenmakers actief, wat de stad terecht de bijnaam ‘sigarenstad’ opleverde.",
                ],
            },
            {
                "h": "Het einde, en wat er restte",
                "img": f"{IMG}/sigarenfabriek_delft/sigarenfabriek_delft_p4_5.jpg",
                "img_caption": "Een Hillen-winkelpand ‘Havana Sigaren’ op een druk stadshoekje.",
                "img2": f"{IMG}/sigarenfabriek_delft/sigarenfabriek_delft_p4_7.jpg",
                "img2_caption": "Reclameborden voor Hillen-sigaren op de Prinsenstraat in Den Haag — het "
                                "bewijs dat de winkelketen zich ver buiten Delft verspreidde.",
                "p": [
                    "In februari 1937 (sommige bronnen noemen 1938) moest de fabriek, dan nog altijd 300 "
                    "werknemers tellend, definitief de deuren sluiten. Het pand werd gekocht door de firma "
                    "Braat. Van de mensen die er werkten, is één persoonlijk verhaal goed "
                    "gedocumenteerd: Leen Dijkshoorn werkte van 1935 tot 1938 op de inpakafdeling, waar de "
                    "sigaren in blik werden verpakt — hij maakte dus zelf de sluiting van de fabriek nog "
                    "mee.",
                    "De herinnering aan het bedrijf leeft op meerdere plekken voort: de Hillenlaan in de "
                    "Delftse wijk Delftzicht is naar de fabriek vernoemd (1994), en het Tabakshistorisch "
                    "Museum Delft — gevestigd in een oude sigarenwinkel — wijdt een vaste plek aan "
                    "‘de oudste sigarenfabriek van Nederland’. De volledige geschiedenis is in 2000 "
                    "vastgelegd door Louis Bracco Gartner in het boek ‘De geschiedenis van de Delftse "
                    "tabaksnijverheid en die van A. Hillen, de oudste sigarenfabriek van Nederland’ (126 "
                    "pagina’s, met foto’s van aandelen, firmabrieven en sigarenbandjes).",
                ],
                "img3": f"{IMG}/sigarenfabriek_delft/sigarenfabriek_delft_p4_6.jpg",
                "img3_caption": "Originele factuur van ‘A. Hillen, Delft Holland’, gedateerd 31 "
                                "december 1902, gericht aan ‘Het Gasthuis, Delft’ — met een "
                                "tekening van het fabriekscomplex in de briefhoofd en handgeschreven regels "
                                "voor sigaren als ‘Rosa Bella’ en ‘Murias Puritanos’.",
            },
        ],
        "sources": [
            "GeschiedenisVanZuidHolland.nl, ‘De geschiedenis van de Zuid-Hollandse tabaksnijverheid’",
            "VerhalenWiki.nl, ‘De historie van A. Hillen en de latere N.V. A. Hillen’s Sigaren- en "
            "Tabaksfabriek’",
            "Tabakshistorie.nl (Stichting Nederlandse Tabakshistorie), ‘Tijdlijn’",
            "Tabaksmuseum.nl, ‘Delftse Tabaksnijverheid’",
            "Stichting Haags Industrieel Erfgoed (SHIE), ‘Hillen, A. (1770–1937)’",
            "Delftsaardewerk.nl, gedenkschotel 150 jaar bestaan A. Hillen’s Sigaren- en Tabaksfabrieken",
            "stratenvandelft.nl (R. & P. van der Krogt), ‘Hillenlaan’",
            "Delftkijkt.nl, ‘Sigarenwinkels van Delft’",
            "L. Bracco Gartner, ‘De geschiedenis van de Delftse tabaksnijverheid en die van A. Hillen, de "
            "oudste sigarenfabriek van Nederland’ (2000)",
        ],
    },
]

PEOPLE = json.loads((ROOT / "data" / "stamboom.json").read_text(encoding="utf-8"))["people"]


def person_link(pid, text):
    name = PEOPLE["@" + pid + "@"]["name"]
    return f'<a href="../stamboom.html?persoon={pid}" title="{name} in de stamboom">{text}</a>'


# Person links in the generated articles: (person id, text to find, name inside it to link).
# Each text must occur exactly once in the rendered article, so a changed sentence fails loudly.
PERSON_LINKS = {
    "boterfabriek-roermond": [
        ("P0005", "Alexander Hillen bleef", "Alexander Hillen"),
        ("P0115", "Alexanders tweelingbroer Johan runde", "Johan"),
        ("P0117", "Alexanders broer Jacobus Hillen trouwde", "Jacobus Hillen"),
        ("P0120", "zijn zoon werd zelfs in Grave geboren", "zijn zoon"),
        ("P0127", "Een kleinzoon van diezelfde Jacobus", "kleinzoon"),
        ("P0005", "Alexander Hillen (1821–1898)", "Alexander Hillen"),
    ],
    "ijzergieterij-blerick": [
        ("P0115", "Johan (Joannes) Hillen", "Johan (Joannes) Hillen"),
        ("P0115", "Johan Hillen en zijn compagnon", "Johan Hillen"),
        ("P0005", "tweelingbroer van Alexander Hillen", "Alexander Hillen"),
        ("P0004", "hoefsmid Alardus Hillen", "Alardus Hillen"),
        ("P0119", "Henri (Henri Hubert Hillen, 1852–1914)", "Henri"),
        ("P0288", "en Piet de zaak voort", "Piet"),
    ],
    "pijpenfabriek-bree": [
        ("P0129", "Jean (Jan) Hillen", "Jean (Jan) Hillen"),
        ("P0135", "bedacht door zoon Albert", "Albert"),
        ("P0129", "Jan (Jean) Hillen", "Jan (Jean) Hillen"),
        ("P0122", "Albertus Theodorus Hubertus (Albert) Hillen", "Albertus Theodorus Hubertus (Albert) Hillen"),
        ("P0123", "Maria Knödgen", "Maria Knödgen"),
        ("P0130", "Josephina Antonetta ‘Maria’ Smets", "Josephina Antonetta ‘Maria’ Smets"),
        ("P0137", "Jos nam de verkoop", "Jos"),
        ("P0135", "rekening, Albert de productie", "Albert"),
        ("P0131", "Albert Theodore Constant Marie Hillen (Bree", "Albert Theodore Constant Marie Hillen"),
    ],
    "sigarenfabriek-delft": [
        ("P0107", "Gerrit (Gerardus) Hillen", "Gerrit (Gerardus) Hillen"),
        ("P0107", "Gerardus Hillen (1743–1805)", "Gerardus Hillen"),
        ("P0111", "Albertus Hillen (1774–1834)", "Albertus Hillen"),
        ("P0112", "Anna Maria van Spreeuwenburg", "Anna Maria van Spreeuwenburg"),
        ("P0304", "Sara Jacoba Elizabeth Hillen", "Sara Jacoba Elizabeth Hillen"),
    ],
}


def add_person_links(slug, html):
    for pid, ctx, name in PERSON_LINKS.get(slug, []):
        n = html.count(ctx)
        if n != 1:
            raise ValueError(f"{slug}: '{ctx}' komt {n}x voor; pas PERSON_LINKS aan")
        html = html.replace(ctx, ctx.replace(name, person_link(pid, name), 1))
    return html


# Hand-written articles (not generated here) that still need a card on the overview page.
EXTRA_CARDS = [
    {"slug": "dokters-hillen-vught", "hero": "assets/images/fotos/vught_taalstraat181.jpg",
     "alt": "Taalstraat 181 in Vught", "era": "Vught · 1889 – 1971", "title": "De dokters Hillen van Vught",
     "teaser": "Vader en zoon, samen 82 jaar huisarts: een ziekenhuis, kenteken N-33, artsenverzet rond Kamp Vught en een straat naar hen genoemd."},
    {"slug": "louis-hillen-blerick", "hero": "assets/images/fotos/brandweerlouishillen.jpg",
     "alt": "De vrijwillige brandweer van Blerick, 1901–1921", "era": "Blerick · 1869 – 1952",
     "title": "Louis Hillen, de man van Blerick",
     "teaser": "Pijpenimporteur, twintig jaar brandweerman, veertig jaar kerkbestuur en wethouder: een vrijgezel die overal bij was."},
]


def render_body(article):
    facts_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in article["facts"])
    sections_html = []
    for sec in article["sections"]:
        parts = [f"<h2>{sec['h']}</h2>"]
        for p in sec.get("p", []):
            parts.append(f"<p>{p}</p>")
        for key in ("img", "img2", "img3"):
            if sec.get(key):
                cap_key = f"{key}_caption"
                cap = sec.get(cap_key, "")
                parts.append(
                    f'<figure><img src="../{sec[key]}" alt="{cap[:120]}" loading="lazy">'
                    f'<figcaption>{cap}</figcaption></figure>'
                )
        if sec.get("list"):
            items = "".join(f"<li>{li}</li>" for li in sec["list"])
            parts.append(f"<ul>{items}</ul>")
        for p in sec.get("p_after", []):
            parts.append(f"<p>{p}</p>")
        sections_html.append("".join(parts))

    sources_html = "".join(f"<li>{s}</li>" for s in article["sources"])

    return f"""
<div class="article-hero">
  <img src="../{article['hero']}" alt="{article['title']}">
  <div class="caption container">{article['hero_caption']}</div>
</div>
<div class="article-head container">
  <p class="era">{article['era']}</p>
  <h1>{article['title']}</h1>
  <p class="sub">{article['sub']}</p>
</div>
<div class="article-layout container">
  <aside class="facts-box">
    <dl>{facts_html}</dl>
  </aside>
  <article class="article-body">
    {''.join(sections_html)}
    <div class="sources">
      <h4>Bronnen</h4>
      <ul>{sources_html}</ul>
    </div>
  </article>
</div>
"""


def build_article_pages():
    for article in ARTICLES:
        body = add_person_links(article["slug"], render_body(article))
        write(f"artikelen/{article['slug']}.html", base_page(
            title=article["title"],
            description=article["teaser"],
            active_nav="artikelen.html",
            body_html=body,
            depth=1,
        ))


def build_overview():
    cards = []
    for a in ARTICLES + EXTRA_CARDS:
        cards.append(f"""
    <a class="article-card" href="artikelen/{a['slug']}.html">
      <div class="thumb"><img src="{a['hero']}" alt="{a.get('alt', a['title'])}" loading="lazy"></div>
      <div class="body">
        <span class="era">{a['era']}</span>
        <h3>{a['title']}</h3>
        <p>{a['teaser']}</p>
        <span class="go">Lees het verhaal &rarr;</span>
      </div>
    </a>""")
    body = f"""
<section class="section container">
  <div class="section-head">
    <p class="kicker">Familiedossier</p>
    <h1>Artikelen</h1>
    <p class="narrow" style="margin:0 auto;">Vier ondernemingen die de familie Hillen door de eeuwen heen
    dreef — van een 18e-eeuwse sigarenfabriek tot een 19e-eeuwse ijzergieterij — en portretten van de
    dokters Hillen in Vught en van een Hillen die in Blerick overal een hand in had.</p>
  </div>
  <div class="card-grid">
    {''.join(cards)}
  </div>
</section>
"""
    write("artikelen.html", base_page(
        title="Artikelen",
        description="Vier historische familiebedrijven van de familie Hillen: boterfabriek, ijzergieterij, pijpenfabriek en sigarenfabriek.",
        active_nav="artikelen.html",
        body_html=body,
    ))


if __name__ == "__main__":
    build_article_pages()
    build_overview()
