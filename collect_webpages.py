#!/usr/bin/env python3
import argparse
import random
import sys
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup


def normalize_url(base_url: str, href: str) -> str | None:
    if not href:
        return None
    href = href.strip()

    # Ignore non-web links
    if href.startswith(("mailto:", "javascript:", "tel:")):
        return None

    # Make absolute
    abs_url = urljoin(base_url, href)

    # Remove fragment (#...)
    abs_url, _frag = urldefrag(abs_url)

    # Only http/https
    p = urlparse(abs_url)
    if p.scheme not in ("http", "https"):
        return None

    return abs_url


def fetch_html_links(url: str, timeout: float) -> set[str]:
    """GET a page and extract all <a href> links."""
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "CS432/532"})
    except requests.RequestException:
        return set()

    ctype = r.headers.get("Content-Type", "")
    if "text/html" not in ctype:
        return set()

    soup = BeautifulSoup(r.text, "lxml")
    out: set[str] = set()
    for a in soup.find_all("a"):
        href = a.get("href")
        n = normalize_url(r.url, href)  # uses final URL as base
        if n:
            out.add(n)
    return out


def is_big_html(url: str, timeout: float) -> tuple[bool, str]:
    """
    Return (accepted?, final_url_after_redirects)
    Accept if HTML and >1000 bytes.
    """
    headers = {"User-Agent": "CS432/532"}

    try:
        h = requests.head(url, timeout=timeout, allow_redirects=True, headers=headers)
        final_url = h.url
        ctype = h.headers.get("Content-Type", "")
        clen = h.headers.get("Content-Length", None)

        if "text/html" not in ctype:
            return False, final_url

        if clen is not None:
            try:
                if int(clen) > 1000:
                    return True, final_url
                return False, final_url
            except ValueError:
                pass  # fall back to GET
    except requests.RequestException:
        # fallback to GET
        final_url = url

    # GET fallback
    try:
        g = requests.get(url, timeout=timeout, allow_redirects=True, headers=headers)
        final_url = g.url
        ctype = g.headers.get("Content-Type", "")
        if "text/html" not in ctype:
            return False, final_url

        clen = g.headers.get("Content-Length", None)
        if clen is not None:
            try:
                return (int(clen) > 1000), final_url
            except ValueError:
                pass

        # If no Content-Length header, estimate from body length
        return (len(g.content) > 1000), final_url

    except requests.RequestException:
        return False, final_url


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("seed_url", help="Seed webpage URL (ex: https://weiglemc.github.io/)")
    ap.add_argument("-n", "--target", type=int, default=500, help="How many unique URIs to collect (default 500)")
    ap.add_argument("-t", "--timeout", type=float, default=5.0, help="Timeout seconds for HTTP requests (default 5)")
    ap.add_argument("-o", "--out", default="uris.txt", help="Output file (default uris.txt)")
    ap.add_argument("--max-pages", type=int, default=5000, help="Safety cap on pages to process (default 5000)")
    args = ap.parse_args()

    target = args.target
    timeout = args.timeout

    good: set[str] = set()
    seen: set[str] = set()

    frontier = deque([args.seed_url])
    pages_processed = 0

    while len(good) < target and pages_processed < args.max_pages:
        if not frontier:
            # If it runs out of frontier, pick a random collected URL as new seed
            if not good:
                print("Frontier empty and no URLs collected. Try a different seed.", file=sys.stderr)
                break
            new_seed = random.choice(list(good))
            print(f"random seed: {new_seed}")
            frontier.append(new_seed)

        url = frontier.popleft()
        if url in seen:
            continue
        seen.add(url)
        pages_processed += 1

        # Check if this URL itself qualifies
        ok, final_url = is_big_html(url, timeout=timeout)
        if ok and final_url not in good:
            good.add(final_url)
            print(final_url)

        # Expand frontier using links from this page
        links = fetch_html_links(url, timeout=timeout)
        for link in links:
            if link not in seen:
                frontier.append(link)

        if pages_processed % 50 == 0:
            remaining = target - len(good)
            print(f"Need to collect {remaining} more URIs...")

    # Saving the results
    with open(args.out, "w", encoding="utf-8") as f:
        for u in sorted(good):
            f.write(u + "\n")

    print(f"\nCollected {len(good)} unique URIs")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
