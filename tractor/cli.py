import argparse
import os
import json

from tractor.fetch import fetch_html
from tractor.extract import extract, extract_fields
from tractor.output import output
from tractor.config import load_config
from tractor.generate import generate_config
from tractor.interactive import interactive_mode



def run():
    parser = argparse.ArgumentParser(description="Tractor - simple web scraper")

    subparsers = parser.add_subparsers(dest="command")

    # =========================
    # SCRAPE (config mode)
    # =========================
    scrape_parser = subparsers.add_parser("scrape")
    scrape_parser.add_argument("config", help="Path to config file or folder")

    # =========================
    # EXTRACT (manual mode)
    # =========================
    extract_parser = subparsers.add_parser("extract")

    extract_parser.add_argument("url", help="URL to scrape")

    extract_parser.add_argument("--selector", help="CSS selector")
    extract_parser.add_argument("--attr", default="text", help="Attribute to extract")

    extract_parser.add_argument("--item", help="Selector for repeating items")
    extract_parser.add_argument(
        "--field",
        action="append",
        help="Field mapping: name=selector or name=selector@attr"
    )

    extract_parser.add_argument("--format", default="text", choices=["text", "json", "csv"])
    extract_parser.add_argument("--output", help="Output file")

    # =========================
    # GENERATE (auto config)
    # =========================
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("url", help="URL to analyze")
    generate_parser.add_argument("--save", help="Save config to file")

    # =========================
    # PREVIEW (test selectors)
    # =========================
    preview_parser = subparsers.add_parser("preview")

    preview_parser.add_argument("url", help="URL to preview")
    preview_parser.add_argument("--selector", help="CSS selector")
    preview_parser.add_argument("--attr", default="text")

    preview_parser.add_argument("--item", help="Selector for repeating items")
    preview_parser.add_argument(
        "--field",
        action="append",
        help="Field mapping"
    )

    # =========================
    # INTERACTIVE (selector picker)
    # =========================
    interactive_parser = subparsers.add_parser("interactive")
    interactive_parser.add_argument("url", help="URL to inspect")


    args = parser.parse_args()

    # =========================
    # SCRAPE MODE
    # =========================
    if args.command == "scrape":
        path = args.config

        if os.path.isdir(path):
            files = [f for f in os.listdir(path) if f.endswith(".json")]

            for file in files:
                print(f"→ Running {file}")

                config_path = os.path.join(path, file)
                config = load_config(config_path)

                html = fetch_html(config["url"])

                if "item" in config and "fields" in config:
                    field_defs = [f"{k}={v}" for k, v in config["fields"].items()]
                    data = extract_fields(html, config["item"], field_defs)
                else:
                    data = extract(
                        html,
                        config["selector"],
                        config.get("attr", "text")
                    )

                name = config.get("name", file.replace(".json", ""))
                output_file = os.path.join("outputs", f"{name}.json")

                output(data, "json", output_file)

            return

        # single config
        config = load_config(path)
        html = fetch_html(config["url"])

        if "item" in config and "fields" in config:
            field_defs = [f"{k}={v}" for k, v in config["fields"].items()]
            data = extract_fields(html, config["item"], field_defs)
        else:
            data = extract(
                html,
                config["selector"],
                config.get("attr", "text")
            )

        name = config.get("name", "output")
        output_file = os.path.join("outputs", f"{name}.json")

        output(data, "json", output_file)

    # =========================
    # EXTRACT MODE
    # =========================
    elif args.command == "extract":
        if not args.item and not args.selector:
            parser.error("provide either --selector OR --item with --field")

        html = fetch_html(args.url)

        if args.item and args.field:
            data = extract_fields(html, args.item, args.field)
        else:
            data = extract(html, args.selector, args.attr)

        output(data, args.format, args.output)

    # =========================
    # GENERATE MODE
    # =========================
    elif args.command == "generate":
        html = fetch_html(args.url)
        config = generate_config(args.url, html)

        if args.save:
            dir_path = os.path.dirname(args.save)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(args.save, "w") as f:
                json.dump(config, f, indent=2)

            print(f"✓ saved to {args.save}")
        else:
            print(json.dumps(config, indent=2))

    # =========================
    # PREVIEW MODE
    # =========================
    elif args.command == "preview":
        html = fetch_html(args.url)

        if args.item and args.field:
            data = extract_fields(html, args.item, args.field)
        else:
            if not args.selector:
                parser.error("provide --selector or --item")
            data = extract(html, args.selector, args.attr)

        preview = data[:5] if isinstance(data, list) else data

        print(json.dumps(preview, indent=2))

    # =========================
    # INTERACTIVE MODE
    # =========================
    elif args.command == "interactive":
        html = fetch_html(args.url)
        interactive_mode(args.url, html)

    else:
        parser.print_help()
