from bs4 import BeautifulSoup
from typing import Dict, List, Any
from urllib.parse import urljoin


def extract_items(items: List, fields: Dict[str, str], base_url: str) -> List[Dict[str, Any]]:
    """
    Extract structured data from a list of item elements.

    Args:
        items: list of BeautifulSoup elements
        fields: dict of field_name -> selector
        base_url: used to resolve relative URLs

    Returns:
        List of dictionaries
    """
    results = []

    for item in items:
        data = {}

        for field_name, selector in fields.items():
            value = extract_field(item, selector, base_url)
            data[field_name] = value

        results.append(data)

    return results


def extract_field(item, selector: str, base_url: str):
    """
    Extract a single field from an item using selector.

    Supports:
        "a@href"
        "img@src"
        ".price"
    """
    if "@" in selector:
        css, attr = selector.split("@", 1)
        el = item.select_one(css)
        if not el:
            return None

        val = el.get(attr)
        if val and attr in ["href", "src"]:
            return urljoin(base_url, val)
        return val

    el = item.select_one(selector)
    if not el:
        return None

    return el.get_text(strip=True)
