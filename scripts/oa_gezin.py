import json, subprocess, urllib.parse, sys, re, time
sys.stdout.reconfigure(encoding="utf-8")


def get(url):
    out = subprocess.run(["curl", "-s", "-A", "hillen research", url], capture_output=True).stdout
    time.sleep(0.3)
    try:
        return json.loads(out.decode("utf-8", "replace"))
    except Exception:
        return {}


def search(q):
    d = get("https://api.openarch.nl/1.0/records/search.json?" + urllib.parse.urlencode({"name": q, "lang": "nl", "number_show": 100}))
    return (d.get("response") or {}).get("docs") or []


def show(ident):
    a, i = ident.split(":", 1)
    t = subprocess.run(["curl", "-s", f"https://api.openarch.nl/1.0/records/show.json?archive={a}&identifier={i}&lang=nl"], capture_output=True).stdout.decode("utf-8", "replace")
    time.sleep(0.3)
    t = t.replace("a2a_", "")
    vals = re.findall(r'"(FirstName|PrefixLastName|LastName|RelationType|PersonAgeLiteral|PersonAgeYears|Profession|Place|Year|Month|Day|EventType)":"([^"]*)"', t)
    return vals


def summarize(vals):
    # rebuild persons in order: names come first, then event, then relation types in same order
    names, cur, ages = [], [], {}
    rels = [v for k, v in vals if k == "RelationType"]
    people = []
    buf = {}
    for k, v in vals:
        if k == "FirstName":
            if buf:
                people.append(buf)
            buf = {"n": v}
        elif k in ("PrefixLastName", "LastName") and buf is not None and "n" in buf and "event" not in buf:
            buf["n"] += " " + v
        elif k in ("PersonAgeLiteral", "PersonAgeYears", "Profession") and buf:
            buf[k] = v
        elif k == "EventType":
            if buf:
                people.append(buf)
            buf = {}
            break
    ev = dict((k, v) for k, v in vals if k in ("EventType",))
    date = [v for k, v in vals if k in ("Year", "Month", "Day")]
    places = [v for k, v in vals if k == "Place"]
    out = []
    for p, r in zip(people, rels):
        extra = " ".join(f"{k}={v}" for k, v in p.items() if k != "n")
        out.append(f"{r}: {p['n']} {extra}".strip())
    return ev.get("EventType"), date, places, out


for q in sys.argv[1:]:
    docs = search(q)
    print(f"\n##### {q}: {len(docs)}")
    seen = set()
    for d in sorted(docs, key=lambda x: str((x.get("eventdate") or {}).get("year"))):
        ident = d.get("url", "").rstrip("/").split("/")[-1]
        if ident in seen or d.get("eventtype") == "Registratie":
            continue
        seen.add(ident)
        et, date, places, ppl = summarize(show(ident))
        print(f"  {'-'.join(date[:3])} {et} {places[:1]} {ident}")
        for x in ppl:
            print("     ", x)
