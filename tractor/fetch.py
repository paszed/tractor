import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")
