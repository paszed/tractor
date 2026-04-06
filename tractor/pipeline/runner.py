from typing import Generator, Dict, Any, Set

from tractor.fetch.fetcher import fetch_html
from tractor.parse.parser import parse_html
from tractor.select.selector import select_items
from tractor.extract.extractor import extract_items
from tractor.paginate.paginator import get_next_url


def run_pipeline(config: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    url = config.get("url")
    item_selector = config.get("item")
    fields = config.get("fields", {})
    pagination_selector = config.get("pagination", {}).get("next")

    visited: Set[str] = set()

    while url:
        if url in visited:
            break
        visited.add(url)

        html = fetch_html(url)
        soup = parse_html(html)

        items = select_items(soup, item_selector)
        results = extract_items(items, fields, url)

        for item in results:
            yield item

        next_url = get_next_url(soup, pagination_selector, url)

        if not next_url or next_url in visited:
            break

        url = next_url
        url = next_url
