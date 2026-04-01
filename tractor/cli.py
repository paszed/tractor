import argparse

from tractor.fetch import fetch_html
from tractor.extract import extract, extract_fields
from tractor.output import output


def run():
    parser = argparse.ArgumentParser(description="Tractor - simple web scraper")

    parser.add_argument("url", help="URL to scrape")

    # simple mode
    parser.add_argument("--selector", help="CSS selector")
    parser.add_argument("--attr", default="text", help="Attribute to extract")

    # structured mode
    parser.add_argument("--item", help="Selector for repeating items")
    parser.add_argument(
        "--field",
        action="append",
        help='Field mapping: name=selector or name=selector@attr'
    )

    # output
    parser.add_argument("--format", default="text", choices=["text", "json"])

    args = parser.parse_args()

    # validation
    if not args.item and not args.selector:
        parser.error("provide either --selector OR --item with --field")

    html = fetch_html(args.url)

    # choose mode
    if args.item and args.field:
        data = extract_fields(html, args.item, args.field)
    else:
        data = extract(html, args.selector, args.attr)

    output(data, args.format)
