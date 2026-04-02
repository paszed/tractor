from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


def generate_config(url, html):
    soup = BeautifulSoup(html, "html.parser")

    domain = urlparse(url).netloc.replace("www.", "").split(".")[0]

    # ------------------------
    # Detect repeated elements (IMPROVED)
    # ------------------------
    candidates = [
        "article",
        "li",
        "div.card",
        "div.item",
        "div.product",
        "div.product_pod"
    ]

    best_selector = None
    best_score = 0

    for selector in candidates:
        items = soup.select(selector)

        # ignore weak matches
        if len(items) < 3:
            continue

        # score = count * structure richness
        structure_score = len(items[0].find_all())
        score = len(items) * structure_score

        if score > best_score:
            best_score = score
            best_selector = selector

    # ------------------------
    # Structured mode (fields++)
    # ------------------------
    if best_selector:

        fields = {}

        items = soup.select(best_selector)
        first = items[0]

        # ------------------------
        # TITLE detection
        # ------------------------
        title_tag = first.find(["h1", "h2", "h3"])
        if title_tag:
            fields["title"] = title_tag.name

        # ------------------------
        # LINK detection
        # ------------------------
        link_tag = first.find("a", href=True)
        if link_tag:
            fields["link"] = "a@href"

        # ------------------------
        # IMAGE detection
        # ------------------------
        img_tag = first.find("img", src=True)
        if img_tag:
            fields["image"] = "img@src"

        # ------------------------
        # PRICE detection
        # ------------------------
        text = first.get_text(" ", strip=True)
        price_match = re.search(r"[$€£]\s?\d+", text)

        if price_match:
            price_elem = first.find(string=re.compile(r"[$€£]"))
            if price_elem and price_elem.parent:
                cls = price_elem.parent.get("class")
                if cls:
                    fields["price"] = "." + cls[0]

        # ------------------------
        # fallback
        # ------------------------
        if not fields:
            fields["text"] = best_selector

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
