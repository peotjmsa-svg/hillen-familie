#!/usr/bin/env python3
"""Search the NRW archive portal (archive.nrw.de) from the command line.

archive.nrw.de loads its search results with JavaScript from a JSON service. This script calls that
service directly, so results can be read, saved and translated without using the German website.

Usage:
    python scripts/archivsuche_nrw.py "Hillen Sülz"
    python scripts/archivsuche_nrw.py "Hyllen" --pages 3 --out raw/archivsuche_hyllen.json

Each hit prints its date range (Laufzeit), archive, a link to the record, and the full German
description. The JSON output keeps the raw records for later translation.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://www.archive.nrw.de/sufservice/api/search"
UA = "Mozilla/5.0 (hillen-familie genealogy research)"


def search(keyword, page=0, size=50):
    qs = urllib.parse.urlencode({"keyword": keyword, "size": size, "page": page})
    req = urllib.request.Request(f"{API}?{qs}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_marks(text):
    return (text or "").replace("<mark>", "").replace("</mark>", "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keyword")
    ap.add_argument("--pages", type=int, default=1)
    ap.add_argument("--size", type=int, default=50)
    ap.add_argument("--out")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    records = []
    for page in range(args.pages):
        data = search(args.keyword, page, args.size)
        if page == 0:
            print(f"# {args.keyword}: {data['hits']} hits")
        batch = data.get("searchResult") or []
        if not batch:
            break
        records.extend(batch)

    for r in records:
        oid = r.get("objectId")
        print(f"\n## {r.get('laufzeit') or '?'}  |  {r.get('archivName') or r.get('archiv') or ''}")
        print(f"https://www.archive.nrw.de/ms/search?link=VERZEICHNUNGSEINHEIT-{oid}")
        print(strip_marks(r.get("title")))
        for a in r.get("textAbstract") or []:
            print("  ", strip_marks(a))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(records, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
