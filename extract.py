#!/usr/bin/env python3
"""
LLM Audit Page Extractor
Fetches clean page content via Jina Reader API for use with the LLM readability audit.

Usage:
    python extract.py <url>
    python extract.py <url> --output /path/to/output.md
    python extract.py <url> --json
"""

import argparse
import json
import subprocess
import sys


def extract_page(url):
    """Fetch page content via Jina Reader API using curl. Returns markdown string."""
    jina_url = f"https://r.jina.ai/{url}"

    result = subprocess.run(
        [
            "curl", "-s",
            jina_url,
            "-H", "X-Retain-Images: none",
            "-H", "X-Return-Format: markdown",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )

    if result.returncode != 0:
        print(f"curl failed with code {result.returncode}: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    if not result.stdout.strip():
        print(f"Empty response from Jina for {url}", file=sys.stderr)
        sys.exit(1)

    return result.stdout


def compute_stats(content):
    """Compute basic page stats for the audit."""
    lines = content.strip().split("\n")
    words = content.split()
    chars = len(content)

    headings = [l for l in lines if l.startswith("#")]
    # Count markdown table separator rows (handles both |---|and | --- | formats)
    tables = sum(1 for l in lines if l.strip().startswith("|") and "---" in l and l.strip().endswith("|"))
    lists = sum(1 for l in lines if l.strip().startswith(("- ", "* ", "1. ", "2. ", "3. ")))

    # Coverage estimate based on Petrovic/DEJAN research
    if chars < 5000:
        coverage = "~66%"
    elif chars < 10000:
        coverage = "~42%"
    elif chars < 20000:
        coverage = "~25%"
    else:
        coverage = "~12%"

    return {
        "chars": chars,
        "words": len(words),
        "headings": len(headings),
        "tables": tables,
        "list_items": lists,
        "estimated_grounding_coverage": coverage,
        "grounding_ratio": f"{380 / max(len(words), 1):.1%}",
    }


def main():
    parser = argparse.ArgumentParser(description="Extract page content for LLM audit")
    parser.add_argument("url", help="URL to extract")
    parser.add_argument("--output", "-o", help="Save to file (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output as JSON with stats")
    args = parser.parse_args()

    content = extract_page(args.url)
    stats = compute_stats(content)

    if args.json:
        result = {
            "url": args.url,
            "stats": stats,
            "content": content,
        }
        output = json.dumps(result, indent=2)
    else:
        header = (
            f"# Extracted: {args.url}\n"
            f"# Words: {stats['words']} | Chars: {stats['chars']} | "
            f"Grounding coverage: {stats['estimated_grounding_coverage']} | "
            f"Grounding ratio: {stats['grounding_ratio']}\n"
            f"# Headings: {stats['headings']} | Tables: {stats['tables']} | "
            f"List items: {stats['list_items']}\n"
            f"---\n\n"
        )
        output = header + content

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
