from urllib.parse import urljoin

def get_next_page(html, config, base_url):
    if "pagination" not in config:
        return None

    selector = config["pagination"].get("next")
    if not selector:
        return None

    el = html.select_one(selector)
    if not el:
        return None

    href = el.get("href")
    if not href:
        return None

    return urljoin(base_url, href)
