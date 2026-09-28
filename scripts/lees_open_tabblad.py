#!/usr/bin/env python3
"""Read the text of the tabs the user has open in a Chrome window started with --remote-debugging-port.

This script never navigates or clicks: the user browses (and passes any login or bot check) themselves,
and this only reads what is on screen, so the content can be translated and added to the family tree.

Usage:
    python scripts/lees_open_tabblad.py [PORT] [--out FILE]
"""
import sys

from playwright.sync_api import sync_playwright


def main():
    port = 9223
    out = None
    args = sys.argv[1:]
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        args = args[:i] + args[i + 2:]
    if args:
        port = int(args[0])
    sys.stdout.reconfigure(encoding="utf-8")
    chunks = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        for ctx in browser.contexts:
            for page in ctx.pages:
                if page.url.startswith(("chrome://", "devtools://", "about:")):
                    continue
                chunks.append(f"===== {page.title()}\n{page.url}\n\n{page.inner_text('body')}\n")
        # detach without closing the user's browser
    text = "\n".join(chunks)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
