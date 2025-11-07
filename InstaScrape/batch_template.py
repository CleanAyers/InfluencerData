#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch scrape template for InstaScrape.

Edit the REEL_IDENTIFIERS list with either reel URLs or just the shortcodes
(e.g., DQag0vAD5na), adjust the requests-per-second (RPS) value, then run:

    source venv/bin/activate
    python3 batch_template.py

The script reuses cookie.json via the standard login flow, sequentially
scrapes each reel, and stores outputs with shortcode-based filenames.
"""

import asyncio
from datetime import datetime
from typing import List, Optional
import time
import re

from main import (
    extract_shortcode,
    fetch_all_pages,
    load_or_login_get_cookies_interactive,
    write_outputs,
    ScrapeError,
    LoginError,
)

# ---------------------------------------------------------------------------
# EDIT THESE VALUES
# ---------------------------------------------------------------------------

REEL_IDENTIFIERS: List[str] = [
    "DNt_4e4Xlmw", #1
    "DMgFYzwyGtz", #2
    "DDfIkCOShLr", #3
    "DBPNgMNpx2s", #4
    "C8sGi0PSLvK", #5

    "CeXDv26jJnq", #6
    "CeM9VyMJFsS", #7
]

# Default base URL used when only a shortcode is provided.
BASE_REEL_URL = "https://www.instagram.com/reel/{shortcode}/"

# Maximum requests per second when hitting Instagram GraphQL.
MAX_RPS: float = 3.0

# Optional prefix to help group files per creator/run.
OUTPUT_PREFIX: str = "batch"

# Sleep in seconds between reels to stay friendly to rate limits.
DELAY_BETWEEN_REELS: float = 5.0

# ---------------------------------------------------------------------------


async def scrape_reel(shortcode: str, session_tuple, rps: float) -> None:
    comments_flat, comments_struct = await fetch_all_pages(shortcode, session_tuple, rps)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{OUTPUT_PREFIX}_{shortcode}_{timestamp}"
    write_outputs(base_name, comments_flat, comments_struct)


def normalize_to_shortcode(identifier: str) -> Optional[str]:
    identifier = identifier.strip()
    if not identifier:
        return None
    if "instagram.com" in identifier:
        return extract_shortcode(identifier)
    if re.fullmatch(r"[A-Za-z0-9_-]+", identifier):
        return identifier
    return None


async def run_batch(urls: List[str]) -> None:
    if not urls:
        print("No reel identifiers configured.")
        return

    session_tuple = load_or_login_get_cookies_interactive()
    for raw_identifier in urls:
        shortcode = normalize_to_shortcode(raw_identifier)
        if not shortcode:
            print(f"[skip] Invalid reel identifier: {raw_identifier}")
            continue
        print(f"\n=== Scraping reel {shortcode} ===")
        try:
            await scrape_reel(shortcode, session_tuple, MAX_RPS)
        except (ScrapeError, LoginError) as exc:
            print(f"[error] Failed to scrape {shortcode}: {exc}")
            break
        if DELAY_BETWEEN_REELS > 0:
            time.sleep(DELAY_BETWEEN_REELS)


def main() -> None:
    try:
        asyncio.run(run_batch(REEL_IDENTIFIERS))
    except KeyboardInterrupt:
        print("Aborted by user.")


if __name__ == "__main__":
    main()
