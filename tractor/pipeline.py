import sys
from urllib.parse import urljoin

from tractor.fetch import fetch_html
from tractor.extract import extract_fields
from tractor.pagination import get_next_page


def resolve_url(base_url, el, attr):
    href = el.get(attr)
    if not href:
        return None
    return urljoin(base_url, href)


def run_pipeline(config):
    url = config["url"]
    all_data = []
    visited = set()

    while url:
        # 🔴 STOP if already visited (prevents duplicates)
        if url in visited:
            break

        visited.add(url)

        print(f"→ Crawling {url}", file=sys.stderr)

        html = fetch_html(url)

        # 👉 Get next page EARLY (important for control flow)
        next_url = get_next_page(html, config, url)

        # 👉 Extract data
        if "item" in config and "fields" in config:
            field_defs = [f"{k}={v}" for k, v in config["fields"].items()]
            data = extract_fields(html, config["item"], field_defs, url)
        else:
            data = []

        all_data.extend(data)

        # 🔴 Stop if no next page
        if not next_url:
            break

        # 🔴 Prevent loop if next already visited
        if next_url in visited:
            break

        url = next_url

    return all_data


def run_pipeline_stream(config):
    url = config["url"]
    visited = set()

    while url:
        # 🔴 STOP duplicates early
        if url in visited:
            break

        visited.add(url)

        print(f"→ Crawling {url}", file=sys.stderr)

        html = fetch_html(url)

        # 👉 Get next page early
        next_url = get_next_page(html, config, url)

        # 👉 Extract and yield
        if "item" in config and "fields" in config:
            field_defs = [f"{k}={v}" for k, v in config["fields"].items()]
            data = extract_fields(html, config["item"], field_defs, url)
        else:
            data = []

        for item in data:
            yield item

        # 🔴 Stop if no next
        if not next_url:
            break

        # 🔴 Prevent loops
        if next_url in visited:
            break

        url = next_url


def run_generate(url):
    from tractor.generate import generate_config

    html = fetch_html(url)
    return generate_config(url, html)
