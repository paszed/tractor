from bs4 import BeautifulSoup
from urllib.parse import urlparse


# -------------------------
# HELPERS
# -------------------------

def score_selector(soup, selector):
    try:
        return len(soup.select(selector))
    except Exception:
        return 0


def normalize_classes(classes):
    return ".".join([c for c in classes if c][:2])


# -------------------------
# ITEM DETECTION
# -------------------------

def detect_item(soup):
    candidates = {}

    elements = soup.find_all(["article", "li", "div"])

    for el in elements[:200]:
        classes = el.get("class", [])

        # require class → structure signal
        if not classes:
            continue

        cls = normalize_classes(classes)
        if not cls:
            continue

        selector = f"{el.name}.{cls}"

        count = score_selector(soup, selector)

        # ignore useless selectors
        if count < 3 or count > 100:
            continue

        score = 0

        # repetition = strong signal
        score += count * 2

        # structure: multiple children
        if len(el.find_all(recursive=False)) >= 2:
            score += 20

        # semantic: title-like
        if el.select_one("h1, h2, h3"):
            score += 30

        # semantic: link
        if el.select_one("a[href]"):
            score += 10

        # semantic: article tag
        if el.name == "article":
            score += 20

        candidates[selector] = score

    if not candidates:
        return "body"

    return max(candidates, key=candidates.get)


# -------------------------
# FIELD DETECTION
# -------------------------

def detect_fields(container):
    fields = {}

    # --- TITLE ---
    title_el = container.select_one("h1, h2, h3")
    if title_el:
        fields["title"] = title_el.name

    # --- LINK ---
    link_el = None

    if title_el:
        link_el = title_el.select_one("a[href]")
        if link_el:
            fields["link"] = f"{title_el.name} a@href"

    if not link_el:
        link_el = container.select_one("a[href]")
        if link_el:
            fields["link"] = "a@href"

    # --- IMAGE ---
    img_el = container.select_one("img")
    if img_el:
        fields["image"] = "img@src"

    # --- PRICE ---
    price_el = container.select_one(".price, .price_color, .amount")

    if price_el:
        classes = price_el.get("class", [])
        if classes:
            fields["price"] = f".{classes[0]}"

    return fields


# -------------------------
# MAIN GENERATOR
# -------------------------

def generate_config(url, html):
    soup = BeautifulSoup(html, "html.parser")

    item = detect_item(soup)

    container = soup.select_one(item)
    fields = detect_fields(container) if container else {}

    name = urlparse(url).netloc.split(".")[0]

    return {
        "name": name,
        "url": url,
        "item": item,
        "fields": fields,
    }

