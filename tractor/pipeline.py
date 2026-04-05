import sys

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from tractor.fetch import fetch_html
from tractor.extract import extract_fields


def get_next_page(html, config, base_url):
    pagination = config.get("pagination")
    if not pagination:
        return None

    expr = pagination.get("next")
    if not expr:
        return None

    # parse "selector@attr"
    if "@" in expr:
        selector, attr = expr.split("@", 1)
    else:
        selector, attr = expr, "href"

    soup = BeautifulSoup(html, "html.parser")
    el = soup.select_one(selector)

    if not el:
        return None

    href = el.get(attr)
    if not href:
        return None

    return urljoin(base_url, href)


def run_pipeline(config):
    url = config["url"]
    all_data = []

    while url:
        
        print(f"→ Crawling {url}", file=sys.stderr)

        html = fetch_html(url)

        # extract structured data
        if "item" in config and "fields" in config:
            field_defs = [f"{k}={v}" for k, v in config["fields"].items()]
            data = extract_fields(html, config["item"], field_defs, url)
        else:
            data = []

        all_data.extend(data)

        # pagination
        next_url = get_next_page(html, config, url)

        if not next_url:
            break

        url = next_url

    return all_data


def run_generate(url):
    from tractor.generate import generate_config

    html = fetch_html(url)
    return generate_config(url, html)


def run_pipeline_stream(config):
    url = config["url"]

    while url:
        print(f"→ Crawling {url}", file=sys.stderr)

        html = fetch_html(url)

        # extract structured data
        if "item" in config and "fields" in config:
            field_defs = [f"{k}={v}" for k, v in config["fields"].items()]
            data = extract_fields(html, config["item"], field_defs, url)
        else:
            data = []

        for item in data:
            yield item

        # pagination
        next_url = get_next_page(html, config, url)
        if not next_url:
            break

        url = next_url
