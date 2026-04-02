from bs4 import BeautifulSoup


def get_selector(el):
    """Generate simple CSS selector"""
    if el.get("id"):
        return f"#{el.get('id')}"

    if el.get("class"):
        return f"{el.name}.{el.get('class')[0]}"

    return el.name


def interactive_mode(url, html):
    soup = BeautifulSoup(html, "html.parser")

    # pick interesting elements
    elements = soup.select("h1, h2, h3, a, li, article")[:20]

    if not elements:
        print("No elements found")
        return

    print("\nSelect an element:\n")

    for i, el in enumerate(elements):
        text = el.get_text(strip=True)[:80]
        print(f"[{i}] <{el.name}> {text}")

    choice = input("\nEnter number: ")

    try:
        el = elements[int(choice)]
    except:
        print("Invalid choice")
        return

    selector = get_selector(el)

    print("\nSuggested selector:")
    print(selector)
