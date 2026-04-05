from bs4 import BeautifulSoup
import re


# -------------------------
# HELPERS
# -------------------------

def clean_text(text):
    if not text:
        return ""

    return (
        text.strip()
        .encode("latin1", errors="ignore")
        .decode("utf-8", errors="ignore")
    )


def parse_price(text):
    text = clean_text(text)

    match = re.search(r"[\d]+(?:\.\d+)?", text)
    if match:
        return float(match.group())

    return text


# -------------------------
# SIMPLE EXTRACT
# -------------------------

def extract(html, selector, attr="text"):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)

    results = []

    for el in elements:
        if attr == "text":
            value = clean_text(el.get_text(strip=True))
        else:
            value = el.get(attr)

        results.append(value)

    return results


# -------------------------
# STRUCTURED EXTRACT
# -------------------------

def extract_fields(html, item_selector, field_defs):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(item_selector)

    results = []

    for item in items:
        obj = {}

        for field in field_defs:
            # parse "name=selector@attr"
            name, expr = field.split("=", 1)

            if "@" in expr:
                selector, attr = expr.split("@", 1)
            else:
                selector, attr = expr, "text"

            el = item.select_one(selector.strip())

            if el:
                if attr == "text":
                    value = clean_text(el.get_text(strip=True))
                else:
                    value = el.get(attr)
            else:
                value = None

            # 🔥 SPECIAL HANDLING: price
            if name == "price" and value:
                value = parse_price(value)

            obj[name] = value

        results.append(obj)

    return results
