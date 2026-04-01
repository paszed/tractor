import argparse

from tractor.fetch import fetch_html
from tractor.extract import extract
from tractor.output import output


def run():
    parser = argparse.ArgumentParser(description="Tractor - simple web scraper")

    parser.add_argument("url")
    parser.add_argument("--selector", required=True)
    parser.add_argument("--attr", default="text")
    parser.add_argument("--format", default="text", choices=["text","json"])

    args = parser.parse_args()

    html = fetch_html(args.url)
    data = extract(html, args.selector, args.attr)

    output(data, args.format)
