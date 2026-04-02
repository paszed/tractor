from bs4 import BeautifulSoup
from urllib.parse import urlparse


def generate_config(url, html):
    soup = BeautifulSoup(html, "html.parser")

    # simple heuristics
    if soup.select("h1"):
        selector = "h1"
    elif soup.select("h2"):
        selector = "h2"
    elif soup.select("a"):
        selector = "a"
    else:
        selector = "p"

    # name from domain
    domain = urlparse(url).netloc.replace("www.", "").split(".")[0]

    return {
        "name": domain,
        "url": url,
        "selector": selector,
        "attr": "text"
    }

