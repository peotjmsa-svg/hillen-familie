#!/usr/bin/env python3
"""Save a screenshot of an archive.nrw.de record description (for the website).

archive.nrw.de is protected by a proof-of-work bot check and renders records with JavaScript, so a real
browser is needed. This uses Playwright with the locally installed Chrome (pip install playwright).

Usage:
    python scripts/archief_screenshot.py OUTDIR "name|needle|URL" ["name|needle|URL" ...]

`needle` is a word from the record title; the script waits until it is visible, then crops from the
record heading down to the Laufzeit (date) row and saves OUTDIR/name.png.
"""
import os
import sys
import time

from PIL import Image
from playwright.sync_api import sync_playwright

SCALE = 1.5


def main():
    outdir = sys.argv[1]
    jobs = [arg.split("|", 2) for arg in sys.argv[2:]]
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 1000}, locale="de-DE",
                                  device_scale_factor=SCALE)
        page = ctx.new_page()
        for name, needle, url in jobs:
            page.goto(url, timeout=120000)
            try:
                page.get_by_text(needle, exact=False).first.wait_for(state="visible", timeout=150000)
            except Exception as exc:
                print("not found:", name, exc)
                continue
            page.add_style_tag(content="#sliding-popup, .eu-cookie-compliance-banner {display:none!important}")
            time.sleep(3)
            head = page.locator("h1, h2, h3, h4").filter(has_text=needle).first.bounding_box()
            date_row = page.get_by_text("Laufzeit", exact=True).first.bounding_box()
            scroll = page.evaluate("window.scrollY")
            full = os.path.join(outdir, f"{name}_full.png")
            page.screenshot(path=full, full_page=True)
            top = max(0, (head["y"] + scroll - 40) * SCALE)
            bottom = (date_row["y"] + scroll + 45) * SCALE
            with Image.open(full) as im:
                im.crop((int(455 * SCALE), int(top), im.width, int(bottom))).save(os.path.join(outdir, f"{name}.png"))
            os.remove(full)
            print("saved", name)
        browser.close()


if __name__ == "__main__":
    main()
