#!/usr/bin/env python3
"""Find candidate archive records (Open Archieven) for family members whose birth or death is still unknown.

For every person in data/stamboom.json without a birth or death year, this searches openarch.nl for
"<first name> Hillen" (or the person's own surname), downloads each hit, and keeps only records in which
the parents (or the spouse) match what the family tree already says. Output is a review list; nothing is
changed in the data. Every match must still be checked by a human before it goes into the tree.

Usage:
    python scripts/zoek_ontbrekende_data.py [--from 1780] [--to 1935] [--out raw/kandidaten.json]
"""
import argparse
import json
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse

API = "https://api.openarch.nl/1.0/records"


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", " ", s)


def get(url):
    out = subprocess.run(["curl", "-s", "-A", "hillen-familie genealogy research", url], capture_output=True)
    time.sleep(0.4)
    return json.loads(out.stdout.decode("utf-8", "replace") or "{}")


def search(q, rows=100):
    url = f"{API}/search.json?" + urllib.parse.urlencode({"name": q, "lang": "nl", "number_show": rows})
    return (get(url).get("response") or {}).get("docs") or []


def unwrap(o):
    while isinstance(o, dict) and len(o) == 1 and not isinstance(next(iter(o.values())), list):
        o = next(iter(o.values()))
    return o


def record(identifier):
    arch, ident = identifier.split(":", 1)
    d = get(f"{API}/show.json?" + urllib.parse.urlencode({"archive": arch, "identifier": ident, "lang": "nl"}))
    r = d[0] if isinstance(d, list) and d else d
    a2a = r.get("a2a_A2A", r) if isinstance(r, dict) else {}
    persons = a2a.get("a2a_Person") or []
    persons = persons if isinstance(persons, list) else [persons]
    names = {}
    for p in persons:
        pn = p.get("a2a_PersonName", {})
        first = unwrap(pn.get("a2a_PersonNameFirstName", {}))
        prefix = unwrap(pn.get("a2a_PersonNamePrefixLastName", {}))
        last = unwrap(pn.get("a2a_PersonNameLastName", {}))
        parts = [x for x in (first, prefix, last) if isinstance(x, str)]
        extra = {}
        for key in ("a2a_BirthDate", "a2a_Age", "a2a_BirthPlace", "a2a_Profession"):
            if key in p:
                extra[key[4:]] = json.dumps(p[key], ensure_ascii=False)
        names[p.get("pid")] = (" ".join(parts), extra)
    rels = a2a.get("a2a_RelationEP") or []
    rels = rels if isinstance(rels, list) else [rels]
    out = []
    for rel in rels:
        pid = unwrap(rel.get("a2a_PersonKeyRef", {}))
        rtype = unwrap(rel.get("a2a_RelationType", {}))
        if pid in names:
            out.append((rtype, names[pid][0], names[pid][1]))
    ev = a2a.get("a2a_Event") or {}
    ev = ev[0] if isinstance(ev, list) else ev
    date = ev.get("a2a_EventDate", {})
    date = {k[4:]: unwrap(v) for k, v in date.items()} if isinstance(date, dict) else {}
    etype = unwrap(ev.get("a2a_EventType", {}))
    place = unwrap((ev.get("a2a_EventPlace") or {}).get("a2a_Place", {})) if isinstance(ev.get("a2a_EventPlace"), dict) else None
    return {"id": identifier, "type": etype, "date": date, "place": place, "people": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="y0", type=int, default=1780)
    ap.add_argument("--to", dest="y1", type=int, default=1935)
    ap.add_argument("--out", default="raw/kandidaten.json")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    data = json.load(open("data/stamboom.json", encoding="utf-8"))
    people, fams = data["people"], data["families"]
    parents, spouses = {}, {}
    for f in fams.values():
        for c in f["chil"]:
            parents[c] = (f["husb"], f["wife"])
        if f["husb"] and f["wife"]:
            spouses.setdefault(f["husb"], []).append(f["wife"])
            spouses.setdefault(f["wife"], []).append(f["husb"])

    results = {}
    for pid, p in people.items():
        if p["birth_year"] and p["death_year"]:
            continue
        era = p["birth_year"] or p["death_year"]
        if not era or not (args.y0 <= era <= args.y1):
            continue
        first = p["name"].split("(")[0].split()[0]
        surname = p["name"].split()[-1]
        father, mother = parents.get(pid, (None, None))
        checks = []
        if father:
            checks.append(norm(people[father]["name"]).split()[0])
        if mother:
            checks.append(norm(people[mother]["name"]).split()[-1])
        for s in spouses.get(pid, []):
            checks.append(norm(people[s]["name"]).split()[-1])
        if not checks:
            continue
        hits = []
        for doc in search(f"{first} {surname}"):
            rec_id = doc.get("url", "").rstrip("/").split("/")[-1]
            if ":" not in rec_id:
                continue
            ev_year = (doc.get("eventdate") or {}).get("year")
            if ev_year and p["birth_year"] and int(ev_year) < p["birth_year"] - 1:
                continue
            rec = record(rec_id)
            blob = norm(" ".join(n for _, n, _ in rec["people"]))
            score = sum(1 for c in checks if c and c in blob)
            if score >= min(2, len(checks)):
                hits.append(rec)
        if hits:
            results[pid] = {"name": p["name"], "birth_year": p["birth_year"], "death_year": p["death_year"],
                            "checks": checks, "records": hits}
            print(f"\n## {pid} {p['name']} ({p['birth_year']}–{p['death_year']})  checks={checks}")
            for r in hits:
                d = r["date"]
                print(f"   {d.get('Year')}-{d.get('Month')}-{d.get('Day')} {r['type']} {r['place']} {r['id']}")
                for rt, n, x in r["people"]:
                    print(f"      {rt}: {n} {x if x else ''}")
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
