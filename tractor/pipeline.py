def run_generate(url):
    from tractor.fetch import fetch_html
    from tractor.generate import generate_config

    html = fetch_html(url)
    config = generate_config(html, url)

    return config


def run_scrape(config):
    from tractor.fetch import fetch_html
    from tractor.extract import extract_data

    html = fetch_html(config["url"])
    data = extract_data(html, config)

    return data
