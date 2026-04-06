import argparse
import sys

from tractor.commands.scrape import run_command as scrape_command
from tractor.commands.preview import run_command as preview_command
from tractor.commands.extract import run_command as extract_command
from tractor.commands.interactive import run_command as interactive_command

from tractor.utils.errors import TractorError


def main():
    parser = argparse.ArgumentParser(prog="tractor")
    subparsers = parser.add_subparsers(dest="command")

    # scrape
    s = subparsers.add_parser("scrape")
    s.add_argument("config")
    s.add_argument(
        "--format",
        choices=["json", "jsonl"],
        default="jsonl"
    )

    # preview
    p = subparsers.add_parser("preview")
    p.add_argument("config")

    # extract
    e = subparsers.add_parser("extract")
    e.add_argument("url")
    e.add_argument("selector")

    # interactive
    i = subparsers.add_parser("interactive")
    i.add_argument("url")

    args = parser.parse_args()

    try:
        if args.command == "scrape":
            scrape_command(args.config, format=args.format)

        elif args.command == "preview":
            preview_command(args.config)

        elif args.command == "extract":
            extract_command(args.url, args.selector)

        elif args.command == "interactive":
            interactive_command(args.url)

        else:
            parser.print_help()
            sys.exit(1)

    except TractorError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
