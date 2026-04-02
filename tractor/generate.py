from bs4 import BeautifulSoup
from urllib.parse import urlparse


def score(soup, selector):
    try:
        return len(soup.select(selector))
    except:
        return 0


def pick_best(candidates, soup):
    best = None
    best_score = -1
    best_count = float("inf")

    for sel in candidates:
        count = score(soup, sel)

        if 5 <= count <= 100:
            s = 3
        elif 2 <= count < 5:
            s = 2
        elif count == 1:
            s = 1
        else:
            s = 0

        if s > best_score or (s == best_score and count < best_count):
            best = sel
            best_score = s
            best_count = count

    return best


def detect_item(soup):
    candidates = {}

    elements = soup.find_all(["article", "li", "div"])

    for el in elements[:200]:
        classes = el.get("class", [])

        # must have class → structure signal
        if not classes:
            continue

        # build selector
        cls = ".".join(classes[:2])
        selector = f"{el.name}.{cls}"

        count = len(soup.select(selector))

        # ignore too rare or too broad
        if count < 3 or count > 50:
            continue

        score = 0

        # base score = repetition
        score += count * 2

        # strong boost: has multiple children (structure)
        if len(el.find_all(recursive=False)) >= 2:
            score += 20

        # strong boost: contains title-like
        if el.select_one("h1, h2, h3"):
            score += 30

        # boost: contains link
        if el.select_one("a[href]"):
            score += 10

        # boost semantic tags
        if el.name == "article":
            score += 20

        candidates[selector] = score

    if not candidates:
        return "body"

    return max(candidates, key=candidates.get)



def detect_fields(container):
    fields = {}

    # --- TITLE ---
    title = container.select_one("h1, h2, h3")
    if title:
        fields["title"] = title.name

    # --- LINK (scoped to title if possible) ---
    if title:
        link = title.select_one("a[href]")
        if link:
            fields["link"] = f"{title.name} a@href"
    else:
        link = container.select_one("a[href]")
        if link:
            fields["link"] = "a@href"

    # --- IMAGE ---
    img = container.select_one("img")
    if img:
        fields["image"] = "img@src"

    # --- PRICE ---
    price = container.select_one(".price, .price_color, .amount")
    if price:
        classes = price.get("class", [])
        if classes:
            fields["price"] = "." + classes[0]

    return fields

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
        "fields": fields
    }


