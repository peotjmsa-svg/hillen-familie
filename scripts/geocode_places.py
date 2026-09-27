#!/usr/bin/env python3
"""Geocode every place name found in the parsed GEDCOM data via Nominatim.

Run once, after parse_gedcom.py: python scripts/geocode_places.py
Writes: data/plaatsen.json (cached, so the live site never calls the geocoder).
Respects Nominatim usage policy: descriptive User-Agent, max 1 request/second.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAMBOOM_PATH = ROOT / "data" / "stamboom.json"
OUT_PATH = ROOT / "data" / "plaatsen.json"

USER_AGENT = "hillen-familie-stamboom-website/1.0 (persoonlijk familieproject; contact: peotjmsa@gmail.com)"

# Manual overrides for place names that are ambiguous, historical, or need a
# country hint to geocode correctly.
QUERY_OVERRIDES = {
    "'s-Gravenhage": "Den Haag, Nederland",
    "België (Bree)": "Bree, België",
    "Bree (B)": "Bree, België",
    "Neerpelt (B)": "Neerpelt, België",
    "Edinburgh (Schotland)": "Edinburgh, Scotland, United Kingdom",
    "Duitsland (Rijnland)": "Rheinland, Duitsland",
    "Parijs": "Paris, France",
    "Den Bosch": "'s-Hertogenbosch, Nederland",
    "Antwerpen": "Antwerpen, België",
    "Heythuizen": "Heythuysen, Nederland",
}


def geocode(query):
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": 1})
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not data:
        return None
    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
        "display_name": data[0]["display_name"],
    }


def main():
    stamboom = json.loads(STAMBOOM_PATH.read_text(encoding="utf-8"))
    places = stamboom["places"]

    cache = {}
    if OUT_PATH.exists():
        cache = json.loads(OUT_PATH.read_text(encoding="utf-8"))

    changed = False
    for place in places:
        if place in cache and cache[place].get("lat") is not None:
            continue
        query = QUERY_OVERRIDES.get(place, f"{place}, Nederland")
        result = None
        try:
            result = geocode(query)
        except Exception as e:
            print(f"FOUT bij geocoderen van {place!r} ({query!r}): {e}")
        if result is None and place in QUERY_OVERRIDES:
            pass
        elif result is None:
            # Retry without the ", Nederland" suffix in case it's not Dutch.
            try:
                result = geocode(place)
            except Exception as e:
                print(f"FOUT bij herhaalde poging {place!r}: {e}")
        if result:
            cache[place] = {"query": query, **result}
            print(f"OK   {place!r:35s} -> {result['lat']:.4f},{result['lon']:.4f}  ({result['display_name']})")
        else:
            cache[place] = {"query": query, "lat": None, "lon": None, "display_name": None}
            print(f"MISS {place!r:35s} -> geen resultaat voor query {query!r}")
        changed = True
        time.sleep(1.1)

    if changed:
        OUT_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")

    n_ok = sum(1 for v in cache.values() if v.get("lat") is not None)
    print(f"\nTotaal {len(cache)} plaatsen, {n_ok} succesvol gegeocodeerd.")


if __name__ == "__main__":
    main()
