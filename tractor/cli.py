import argparse

from tractor.fetch import fetch_html
from tractor.extract import extract, extract_fields
from tractor.output import output
from tractor.config import load_config


def run():
    parser = argparse.ArgumentParser(description="Tractor - simple web scraper")

    subparsers = parser.add_subparsers(dest="command")

    # --- scrape command (config mode) ---
    scrape_parser = subparsers.add_parser("scrape")
    scrape_parser.add_argument("config", help="Path to config file")

    # --- default CLI args ---
    parser.add_argument("url", nargs="?", help="URL to scrape")

    parser.add_argument("--selector", help="CSS selector")
    parser.add_argument("--attr", default="text", help="Attribute to extract")

    parser.add_argument("--item", help="Selector for repeating items")
    parser.add_argument(
        "--field",
        action="append",
        help='Field mapping: name=selector or name=selector@attr'
    )

    parser.add_argument("--format", default="text", choices=["text", "json"])
    parser.add_argument("--output", help="Output file")

    args = parser.parse_args()

    # --- CONFIG MODE ---
    if args.command == "scrape":
        config = load_config(args.config)

        html = fetch_html(config["url"])

        if "item" in config and "fields" in config:
            field_defs = [
                f"{k}={v}" for k, v in config["fields"].items()
            ]
            data = extract_fields(html, config["item"], field_defs)
        else:
            data = extract(
                html,
                config["selector"],
                config.get("attr", "text")
            )

        output(data, args.format, args.output)
        return

    # --- CLI MODE ---
    if not args.item and not args.selector:
        parser.error("provide either --selector OR --item with --field")

    html = fetch_html(args.url)

    if args.item and args.field:
        data = extract_fields(html, args.item, args.field)
    else:
        data = extract(html, args.selector, args.attr)

    output(data, args.format, args.output)

