import argparse
import os
import json
import sys
import signal

from tractor.fetch import fetch_html
from tractor.extract import extract, extract_fields
from tractor.output import output
from tractor.config import load_config
from tractor.generate import generate_config
from tractor.interactive import interactive_mode
from tractor.pipeline import run_pipeline


def safe_print(data):
    try:
        print(json.dumps(data, indent=2))
    except BrokenPipeError:
        pass


def run():
    # fix broken pipe (important for piping to head/jq/etc)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser(description="tractor - simple web extraction tool")
    subparsers = parser.add_subparsers(dest="command")

    # =========================
    # SCRAPE
    # =========================
    scrape = subparsers.add_parser("scrape")
    scrape.add_argument("config")
    scrape.add_argument("--output")

    # =========================
    # EXTRACT
    # =========================
    extract_cmd = subparsers.add_parser("extract")
    extract_cmd.add_argument("url")
    extract_cmd.add_argument("--selector")
    extract_cmd.add_argument("--attr")
    extract_cmd.add_argument("--item")
    extract_cmd.add_argument("--field", action="append")
    extract_cmd.add_argument("--format", default="json")
    extract_cmd.add_argument("--output")

    # =========================
    # GENERATE
    # =========================
    generate = subparsers.add_parser("generate")
    generate.add_argument("url")
    generate.add_argument("--save")

    # =========================
    # PREVIEW
    # =========================
    preview = subparsers.add_parser("preview")
    preview.add_argument("url")
    preview.add_argument("--selector")
    preview.add_argument("--attr")
    preview.add_argument("--item")
    preview.add_argument("--field", action="append")

    # =========================
    # INTERACTIVE
    # =========================
    interactive = subparsers.add_parser("interactive")
    interactive.add_argument("url")

    args = parser.parse_args()

    # =========================
    # SCRAPE MODE
    # =========================
    if args.command == "scrape":
        path = args.config

        # folder mode
        if os.path.isdir(path):
            files = [f for f in os.listdir(path) if f.endswith(".json")]

            for file in files:
                print(f"→ Running {file}", file=sys.stderr)

                config_path = os.path.join(path, file)
                config = load_config(config_path)

                data = run_pipeline(config)

                if args.output:
                    output(data, "json", args.output)
                else:
                    safe_print(data)

            return

        # single config
        config = load_config(path)
        data = run_pipeline(config)

        if args.output:
            output(data, "json", args.output)
        else:
            safe_print(data)

    # =========================
    # EXTRACT MODE
    # =========================
    elif args.command == "extract":
        if not args.item and not args.selector:
            parser.error("provide either --selector OR --item with --field")

        html = fetch_html(args.url)

        if args.item and args.field:
            data = extract_fields(html, args.item, args.field, args.url)
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

            print(f"✓ saved to {args.save}", file=sys.stderr)
        else:
            safe_print(config)

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

        preview_data = data[:5] if isinstance(data, list) else data
        safe_print(preview_data)

    # =========================
    # INTERACTIVE MODE
    # =========================
    elif args.command == "interactive":
        html = fetch_html(args.url)
        interactive_mode(args.url, html)

    else:
        parser.print_help()

  
   
