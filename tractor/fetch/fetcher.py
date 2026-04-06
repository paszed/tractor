import requests


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Tractor/1.0)"
}


def fetch_html(url: str, timeout: int = 10) -> str:
    """
    Fetch raw HTML from a URL.

    Returns:
        str: HTML content

    Raises:
        requests.HTTPError
        requests.RequestException
    """
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text
