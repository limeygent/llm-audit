"""
Filename: push_geo_blocks.py
Purpose: Push geo content blocks to llp_geo_paragraph ACF field across city-service pages.
Created: 2026-03-29

Reads geo_blocks.json, matches suburbs to page IDs from pages.json,
swaps service placeholders, and updates via WP REST API.

Usage:
    python3 push_geo_blocks.py --service dental_implants [--limit 3] [--yes]
    python3 push_geo_blocks.py --service all                          # all 4 services
    python3 push_geo_blocks.py --service dental_implants --suburb Westminster  # single page
"""

import json
import os
import re
import asyncio
import aiohttp
import base64
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.expanduser("~")
SITES_FILE = os.path.join(HOME_DIR, "Desktop", "codeprojects", "PMSI-website-editor", "sites.json")
PAGES_FILE = os.path.join(HOME_DIR, "Desktop", "codeprojects", "PMSI-website-editor", "odin-dental", "pages.json")
GEO_BLOCKS_FILE = os.path.join(BASE_DIR, "suburb_data", "geo_blocks.json")
CONCURRENCY = 5

SERVICE_PREFIXES = {
    "dental_implants": "Dental Implants",
    "all_on_four": "All On Four Implants",
    "cosmetic_dentist": "Cosmetic Dentist",
    "dentist_in": "Dentist In"
}

# SAFETY: Only process city-service pages (ID >= 16891)
MIN_PAGE_ID = 16891

# Pages to skip (duplicates, Treatment Considerations)
SKIP_PAGE_IDS = {17270, 17279, 17288, 17301, 17305, 17980}


def extract_suburb(title, prefix):
    """Extract suburb name from page title given a service prefix."""
    pattern = rf'^{re.escape(prefix)}\s+([\w\s]+),\s*WA$'
    match = re.match(pattern, title, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def build_html(heading, geo_block, placeholders):
    """Convert geo block text to HTML with placeholder substitution."""
    text = geo_block
    for key, value in placeholders.items():
        text = text.replace("{{" + key + "}}", value)

    paragraphs = text.strip().split("\n\n")
    html = f"<h2>{heading}</h2>\n"
    for p in paragraphs:
        html += f"<p>{p.strip()}</p>\n"
    return html.strip()


async def update_page(session, auth_header, base_url, page_id, suburb, html, semaphore):
    """Update a single page's llp_geo_paragraph field."""
    async with semaphore:
        try:
            payload = {
                "acf": {
                    "llp_geo_paragraph": html
                }
            }

            url = f"{base_url}wp-json/wp/v2/pages/{page_id}"
            headers = {"Authorization": auth_header, "Content-Type": "application/json"}

            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    print(f"  ok  {page_id} | {suburb}")
                    return page_id, True, "updated"
                else:
                    text = await resp.text()
                    return page_id, False, f"HTTP {resp.status}: {text[:100]}"

        except Exception as e:
            return page_id, False, f"ERROR: {e}"


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--service", required=True, help="Service key (dental_implants, all_on_four, cosmetic_dentist, dentist_in, or 'all')")
    parser.add_argument("--suburb", default=None, help="Process only this suburb")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    if args.service == "all":
        services = list(SERVICE_PREFIXES.keys())
    else:
        if args.service not in SERVICE_PREFIXES:
            print(f"ERROR: Unknown service '{args.service}'. Options: {', '.join(SERVICE_PREFIXES.keys())}, all")
            return
        services = [args.service]

    with open(SITES_FILE) as f:
        sites = json.load(f)
    site = next(s for s in sites if s["name"] == "Odin House Dental Surgery")

    with open(PAGES_FILE) as f:
        pages = json.load(f)

    with open(GEO_BLOCKS_FILE) as f:
        geo_data = json.load(f)

    blocks_by_suburb = {b["suburb"]: b for b in geo_data["blocks"]}
    placeholders = geo_data["placeholders"]

    targets = []
    for service_key in services:
        prefix = SERVICE_PREFIXES[service_key]
        service_placeholders = placeholders[service_key]

        for page in pages:
            if page["id"] < MIN_PAGE_ID:
                continue
            if page["id"] in SKIP_PAGE_IDS:
                continue

            suburb = extract_suburb(page["title"], prefix)
            if not suburb:
                continue

            if args.suburb and suburb.lower() != args.suburb.lower():
                continue

            if suburb not in blocks_by_suburb:
                print(f"  WARNING: No geo block for '{suburb}', skipping page {page['id']}")
                continue

            block = blocks_by_suburb[suburb]
            html = build_html(block["heading"], block["geo_block"], service_placeholders)
            targets.append((page["id"], suburb, service_key, html))

    if args.limit:
        targets = targets[:args.limit]

    if not targets:
        print("No pages matched. Check --service and --suburb values.")
        return

    print(f"Pushing geo blocks to {len(targets)} pages")
    print(f"Services: {', '.join(services)}")
    print(f"Field: llp_geo_paragraph")
    print()

    for page_id, suburb, svc, _ in targets[:5]:
        print(f"  {page_id} | {SERVICE_PREFIXES[svc]} {suburb}")
    if len(targets) > 5:
        print(f"  ... and {len(targets) - 5} more")
    print()

    if not args.yes:
        answer = input("Proceed? (yes/no): ")
        if answer.lower() != "yes":
            print("Aborted.")
            return

    creds = base64.b64encode(
        f"{site['wp_user']}:{site['app_password']}".encode()
    ).decode()
    auth_header = f"Basic {creds}"
    semaphore = asyncio.Semaphore(CONCURRENCY)

    success = 0
    failed = 0
    fail_log = []

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            update_page(session, auth_header, site["url"], page_id, suburb, html, semaphore)
            for page_id, suburb, _, html in targets
        ]
        for coro in asyncio.as_completed(tasks):
            page_id, ok, detail = await coro
            if ok:
                success += 1
            else:
                failed += 1
                fail_log.append((page_id, detail))

    print(f"\n{'='*50}")
    print(f"COMPLETE: {success} updated, {failed} failed")
    print(f"{'='*50}")

    if fail_log:
        print(f"\nFailed pages:")
        for page_id, detail in fail_log:
            print(f"  {page_id}: {detail}")


if __name__ == "__main__":
    asyncio.run(main())
