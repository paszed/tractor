from bs4 import BeautifulSoup
from urllib.parse import urlparse


def generate_config(url, html):
    soup = BeautifulSoup(html, "html.parser")

    domain = urlparse(url).netloc.replace("www.", "").split(".")[0]

    # ------------------------
    # Detect repeated elements
    # ------------------------
    candidates = [
        "article",
        "li",
        "div.card",
        "div.item",
        "a"
    ]

    best_selector = None
    max_count = 0

    for selector in candidates:
        items = soup.select(selector)
        if len(items) > max_count:
            max_count = len(items)
            best_selector = selector

    # ------------------------
    # If we found a list → structured
    # ------------------------
    if best_selector and max_count >= 3:
        fields = {}

        # try to detect title/text
        if soup.select(f"{best_selector} h1, {best_selector} h2, {best_selector} h3"):
            fields["title"] = "h2"
        else:
            fields["text"] = best_selector

        # detect links
        if soup.select(f"{best_selector} a"):
            fields["link"] = "a@href"

        return {
            "name": domain,
            "url": url,
            "item": best_selector,
            "fields": fields
        }

    # ------------------------
    # fallback → simple mode
    # ------------------------
    if soup.select("h1"):
        selector = "h1"
    elif soup.select("h2"):
        selector = "h2"
    elif soup.select("a"):
        selector = "a"
    else:
        selector = "p"

    return {
        "name": domain,
        "url": url,
        "selector": selector,
        "attr": "text"
    }

