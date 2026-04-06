from tractor.fetch.fetcher import fetch_html
from tractor.parse.parser import parse_html


def run_command(url: str) -> None:
    html = fetch_html(url)
    soup = parse_html(html)

    print(f"Loaded {url}")
    print("Type a CSS selector to test (or 'q' to quit)\n")

    while True:
        selector = input("> ").strip()

        if selector in ("q", "quit", "exit"):
            break

        elements = soup.select(selector)

        print(f"Found {len(elements)} elements")

        for el in elements[:3]:
            print("-", el.get_text(strip=True))

        print()
