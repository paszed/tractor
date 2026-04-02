from bs4 import BeautifulSoup


def get_selector(el):
    parts = []
    current = el

    while current and current.name != "html":
        part = current.name

        # prefer class
        if current.get("class"):
            part += "." + ".".join(current.get("class")[:2])

        # fallback to id
        elif current.get("id"):
            part += f"#{current.get('id')}"

        parts.insert(0, part)

        # stop early if meaningful anchor found
        if current.get("class") or current.get("id"):
            break

        current = current.parent

    return " ".join(parts)


def interactive_mode(url, html):
    soup = BeautifulSoup(html, "html.parser")

    # focus on meaningful content areas first
    elements = soup.select("article h3, article a, article p, h1, h2")[:20]

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
    except (ValueError, IndexError):
        print("Invalid choice")
        return

    selector = get_selector(el)

    print("\nSuggested selector:")
    print(selector)

