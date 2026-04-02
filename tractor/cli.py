import argparse
import os

from tractor.fetch import fetch_html
from tractor.extract import extract, extract_fields
from tractor.output import output
from tractor.config import load_config


def run():
    parser = argparse.ArgumentParser(description="Tractor - simple web scraper")

    subparsers = parser.add_subparsers(dest="command")

    # --- scrape command (config mode) ---
    scrape_parser = subparsers.add_parser("scrape")
    scrape_parser.add_argument("config", help="Path to config file or folder")

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

    # =========================
    # CONFIG MODE (scrape)
    # =========================
    if args.command == "scrape":
        path = args.config

        # --- folder mode ---
        if os.path.isdir(path):
            files = [f for f in os.listdir(path) if f.endswith(".json")]

            for file in files:
                config_path = os.path.join(path, file)
                print(f"→ Running {file}")

                config = load_config(config_path)
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

                name = config.get("name", file.replace(".json", ""))
                output_file = os.path.join("outputs", f"{name}.{args.format}")
                output(data, args.format, output_file)

            return

        # --- single file mode ---
        config = load_config(path)
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

    # =========================
    # CLI MODE (manual args)
    # =========================
    if not args.item and not args.selector:
        parser.error("provide either --selector OR --item with --field")

    html = fetch_html(args.url)

    if args.item and args.field:
        data = extract_fields(html, args.item, args.field)
    else:
        data = extract(html, args.selector, args.attr)

    output(data, args.format, args.output)

