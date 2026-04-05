from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def clean_text(text):
    if not text:
        return None
    return text.encode("utf-8", "ignore").decode("utf-8").strip()


def parse_price(text):
    if not text:
        return None
    # extract number like 51.77
    match = re.search(r"(\d+\.\d+)", text)
    return float(match.group(1)) if match else None


def extract(html, selector, attr="text"):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)

    results = []

    for el in elements:
        if attr == "text":
            value = el.get_text(strip=True)
            value = clean_text(value)
        else:
            value = el.get(attr)

        results.append(value)

    return results


def extract_fields(html, item_selector, field_defs, base_url=None):
    soup = html
    items = soup.select(item_selector)

    results = []

    for item in items:
        obj = {}

        for field in field_defs:
            # "name=selector@attr"
            name, expr = field.split("=", 1)

            if "@" in expr:
                selector, attr = expr.split("@", 1)
            else:
                selector, attr = expr, "text"

            el = item.select_one(selector)

            if el:
                if attr == "text":
                    value = el.get_text(strip=True)
                    value = clean_text(value)
                else:
                    value = el.get(attr)
            else:
                value = None

            # normalize URLs
            if name in ["link", "image"] and value and base_url:
                value = urljoin(base_url, value)

            # normalize price
            if name == "price":

                value = parse_price(value)

            obj[name] = value

        results.append(obj)

    return results
