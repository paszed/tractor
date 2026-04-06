from bs4 import BeautifulSoup


def parse_html(html: str) -> BeautifulSoup:
    """
    Convert raw HTML string into a BeautifulSoup object.
    """
    return BeautifulSoup(html, "html.parser")
