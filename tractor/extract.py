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
