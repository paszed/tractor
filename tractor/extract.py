from bs4 import BeautifulSoup


def extract(html, selector, attr="text"):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)

    results = []

    for el in elements:
        if attr == "text":
            results.append(el.get_text(strip=True))
        else:
            results.append(el.get(attr))

    return results


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

            el = item.select_one(selector)

            if el:
                if attr == "text":
                    value = el.get_text(strip=True)
                else:
                    value = el.get(attr)
            else:
                value = None

            obj[name] = value

        results.append(obj)

    return results
