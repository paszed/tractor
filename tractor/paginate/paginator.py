from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_next_url(soup: BeautifulSoup, selector: str, base_url: str) -> str | None:
    """
    Find the next page URL using a CSS selector.

    Args:
        soup: BeautifulSoup object
        selector: e.g. "li.next a@href"
        base_url: current page URL

    Returns:
        Absolute URL or None
    """
    if not selector:
        return None

    if "@" not in selector:
        return None

    css, attr = selector.split("@", 1)

    el = soup.select_one(css)
    if not el:
        return None

    val = el.get(attr)
    if not val:
        return None

    return urljoin(base_url, val)
