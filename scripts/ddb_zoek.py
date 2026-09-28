#!/usr/bin/env python3
"""Search the Deutsche Digitale Bibliothek / Archivportal-D through its public API (v2 search index).

The DDB offers an official API at api.deutsche-digitale-bibliothek.de; its v2 search index can be queried
without an API key. This covers the German archives that are also shown on archivportal-d.de.

Usage:
    python scripts/ddb_zoek.py "Hyllen" [--rows 50] [--archive]

Query syntax is Solr: use quotes for phrases ("Ludwig Augustin") and AND/OR between terms.
--archive limits results to archive records (Archivportal-D).
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://api.deutsche-digitale-bibliothek.de/2/search/index/search/select"
UA = "hillen-familie genealogy research"


def search(query, rows=50, start=0, archive_only=False):
    params = [("q", query), ("rows", rows), ("start", start),
              ("fl", "id,title,label,begin_time,end_time,provider,dataset_label,apd_reference_number,apd_context")]
    if archive_only:
        params.append(("fq", 'sector_fct:"sec_01"'))
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))["response"]


def first(v):
    return v[0] if isinstance(v, list) and v else v


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--rows", type=int, default=50)
    ap.add_argument("--archive", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    res = search(args.query, args.rows, archive_only=args.archive)
    print(f"# {args.query}: {res['numFound']} hits")
    for d in res["docs"]:
        # begin_time/end_time are day counts since year 0
        years = "–".join(str(int(int(first(d.get(k))) / 365.2425)) for k in ("begin_time", "end_time") if d.get(k))
        print(f"\n## {years or '?'} | {first(d.get('provider'))} | {first(d.get('apd_reference_number')) or ''}")
        print(f"https://www.archivportal-d.de/item/{d['id']}")
        print(first(d.get("title")) or first(d.get("label")))
        ctx = d.get("apd_context")
        if ctx:
            print("   context:", " > ".join(str(c) for c in (ctx if isinstance(ctx, list) else [ctx]))[:300])


if __name__ == "__main__":
    main()
