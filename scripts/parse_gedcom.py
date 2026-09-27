#!/usr/bin/env python3
"""Parse the Hillen family GEDCOM export into a compact JSON tree for the website.

Run once: python scripts/parse_gedcom.py
Writes: data/stamboom.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEDCOM_PATH = ROOT / "raw" / "gedcom" / "stamboom-hillen.ged.txt"
OUT_PATH = ROOT / "data" / "stamboom.json"

WOONPLAATS_RE = re.compile(r"Woonplaats volgens de piramide:\s*([^.]+)\.")


NAME_RE = re.compile(r"^(.*)/([^/]*)/\s*$")


def parse_name(raw):
    """'Diederik (Hendrik/Dederik) /Hillen/' -> given, surname, display.

    The surname is always the LAST /slash-delimited/ token on the line;
    a parenthetical alternate-name can itself contain a stray '/'. Anchoring
    the regex greedily from the start (and matching to end-of-string) means
    Python's backtracking naturally picks the LAST pair of slashes as the
    surname delimiters, leaving any earlier stray slash inside group 1.
    """
    m = NAME_RE.match(raw.strip())
    if m:
        given = m.group(1).strip()
        surname = m.group(2).strip()
    else:
        given, surname = raw.strip(), ""
    display = f"{given} {surname}".strip()
    return given, surname, display


def parse_gedcom_lines(path):
    records = []  # list of (level, tag, value)
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.strip().split(" ", 2)
            level = int(parts[0])
            if len(parts) >= 2 and parts[1].startswith("@") and parts[1].endswith("@"):
                # level 0 record start: "0 @P0001@ INDI"
                xref = parts[1]
                tag = parts[2] if len(parts) > 2 else ""
                records.append((level, tag, xref))
            else:
                tag = parts[1] if len(parts) > 1 else ""
                value = parts[2] if len(parts) > 2 else ""
                records.append((level, tag, value))
    return records


def build_individuals_and_families(records):
    individuals = {}
    families = {}

    i = 0
    n = len(records)
    while i < n:
        level, tag, value = records[i]
        if level == 0 and tag == "INDI":
            xref = value
            indi = {
                "id": xref,
                "given": "",
                "surname": "",
                "name": "",
                "nick": None,
                "sex": None,
                "birth_year": None,
                "birth_date": None,
                "birth_place": None,
                "death_year": None,
                "death_date": None,
                "death_place": None,
                "occupation": None,
                "note": None,
                "woonplaats": None,
                "sources": [],
                "famc": None,  # family as child
                "fams": [],    # families as spouse
            }
            i += 1
            context = None  # 'BIRT' or 'DEAT'
            while i < n and records[i][0] > 0:
                lvl, t, v = records[i]
                if lvl == 1:
                    context = t
                    if t == "NAME":
                        given, surname, display = parse_name(v)
                        indi["given"] = given
                        indi["surname"] = surname
                        indi["name"] = display
                    elif t == "SEX":
                        indi["sex"] = v
                    elif t == "NICK":
                        indi["nick"] = v
                    elif t == "OCCU":
                        indi["occupation"] = v
                    elif t == "NOTE":
                        indi["note"] = v
                        m = WOONPLAATS_RE.search(v)
                        if m:
                            indi["woonplaats"] = m.group(1).strip()
                    elif t == "SOUR":
                        indi["sources"].append(v)
                    elif t == "FAMC":
                        indi["famc"] = v
                    elif t == "FAMS":
                        indi["fams"].append(v)
                elif lvl == 2:
                    if context == "BIRT" and t == "DATE":
                        indi["birth_date"] = v
                        ym = re.search(r"(\d{3,4})", v)
                        if ym:
                            indi["birth_year"] = int(ym.group(1))
                    elif context == "BIRT" and t == "PLAC":
                        indi["birth_place"] = v
                    elif context == "DEAT" and t == "DATE":
                        indi["death_date"] = v
                        ym = re.search(r"(\d{3,4})", v)
                        if ym:
                            indi["death_year"] = int(ym.group(1))
                    elif context == "DEAT" and t == "PLAC":
                        indi["death_place"] = v
                i += 1
            individuals[xref] = indi
            continue
        elif level == 0 and tag == "FAM":
            xref = value
            fam = {"id": xref, "husb": None, "wife": None, "chil": [], "marr_date": None, "marr_place": None}
            i += 1
            context = None
            while i < n and records[i][0] > 0:
                lvl, t, v = records[i]
                if lvl == 1:
                    context = t
                    if t == "HUSB":
                        fam["husb"] = v
                    elif t == "WIFE":
                        fam["wife"] = v
                    elif t == "CHIL":
                        fam["chil"].append(v)
                elif lvl == 2:
                    if context == "MARR" and t == "DATE":
                        fam["marr_date"] = v
                    elif context == "MARR" and t == "PLAC":
                        fam["marr_place"] = v
                i += 1
            families[xref] = fam
            continue
        else:
            i += 1

    return individuals, families


def derive_place(indi):
    return indi["birth_place"] or indi["woonplaats"] or indi["death_place"]


def main():
    records = parse_gedcom_lines(GEDCOM_PATH)
    individuals, families = build_individuals_and_families(records)

    # Attach children list to each individual for tree building.
    for fam in families.values():
        for child_id in fam["chil"]:
            child = individuals.get(child_id)
            if child:
                child["_famc_obj"] = fam

    # Build parent -> children edges via FAMS (families where this person is a parent).
    children_of = {xref: [] for xref in individuals}
    for fam in families.values():
        parents = [p for p in (fam["husb"], fam["wife"]) if p]
        for child_id in fam["chil"]:
            for p in parents:
                if p in children_of:
                    children_of[p].append(child_id)

    def person_place_events(p):
        events = []
        if p["birth_place"]:
            events.append({"place": p["birth_place"].strip(), "role": "geboren", "year": p["birth_year"]})
        if p["death_place"]:
            events.append({"place": p["death_place"].strip(), "role": "overleden", "year": p["death_year"]})
        if p["woonplaats"] and p["woonplaats"].strip() not in {e["place"] for e in events}:
            events.append({"place": p["woonplaats"].strip(), "role": "woonachtig", "year": p["birth_year"]})
        return events

    def person_summary(xref):
        p = individuals[xref]
        return {
            "id": p["id"],
            "name": p["name"],
            "sex": p["sex"],
            "birth_year": p["birth_year"],
            "death_year": p["death_year"],
            "occupation": p["occupation"],
            "note": p["note"],
            "place": derive_place(p),
            "place_events": person_place_events(p),
            "sources": p["sources"],
            "children": sorted(set(children_of.get(xref, []))),
        }

    people_out = {xref: person_summary(xref) for xref in individuals}

    # Root ancestor: the individual with no FAMC (no parents recorded) and earliest birth year,
    # falling back to the known root @P0001@.
    roots = [xref for xref, p in individuals.items() if not p["famc"]]
    root_id = "@P0001@" if "@P0001@" in individuals else (roots[0] if roots else None)

    # Unique places (for the map step) -- gather every place mention, not just
    # the first one used for a person's primary "place" field.
    places = set()
    for p in individuals.values():
        for place in (p["birth_place"], p["death_place"], p["woonplaats"]):
            if place:
                places.add(place.strip())
    for fam in families.values():
        if fam["marr_place"]:
            places.add(fam["marr_place"].strip())

    out = {
        "root_id": root_id,
        "people": people_out,
        "families": families,
        "places": sorted(places),
        "stats": {
            "individuals": len(individuals),
            "families": len(families),
            "places": len(places),
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"Individuals: {len(individuals)}  Families: {len(families)}  Places: {len(places)}")
    print(f"Root: {root_id} -> {individuals[root_id]['name'] if root_id else None}")
    # Spot check: name with a slash inside the alt-name parenthetical.
    p1 = individuals.get("@P0001@")
    if p1:
        print(f"Spot check @P0001@: given={p1['given']!r} surname={p1['surname']!r} name={p1['name']!r}")


if __name__ == "__main__":
    main()
