from bs4 import BeautifulSoup
from typing import List


def select_items(soup: BeautifulSoup, selector: str) -> List:
    """
    Select item elements from the page using a CSS selector.

    Args:
        soup: BeautifulSoup object
        selector: CSS selector string

    Returns:
        List of matching elements
    """
    if not selector:
        return []

    return soup.select(selector)
