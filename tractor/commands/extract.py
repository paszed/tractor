from tractor.fetch.fetcher import fetch_html
from tractor.parse.parser import parse_html


def run_command(url: str, selector: str) -> None:
    html = fetch_html(url)
    soup = parse_html(html)

    elements = soup.select(selector)

    for el in elements[:10]:
        print(el.get_text(strip=True))
