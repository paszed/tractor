from bs4 import BeautifulSoup


def get_selector(el):
    parts = []
    current = el

    while current and current.name != "html":
        part = current.name

        if current.get("class"):
            part += "." + ".".join(current.get("class")[:2])
        elif current.get("id"):
            part += f"#{current.get('id')}"

        parts.insert(0, part)

        if current.get("class") or current.get("id"):
            break

        current = current.parent

    return " ".join(parts)


def score_selector(soup, selector):
    try:
        matches = soup.select(selector)
        count = len(matches)
    except Exception:
        return 0, "invalid selector ❌"

    if count == 0:
        return count, "no matches ❌"
    elif count == 1:
        return count, "too specific ⚠️"
    elif count < 5:
        return count, "maybe OK ⚠️"
    elif count < 100:
        return count, "good ✅"
    else:
        return count, "too broad ❌"


def interactive_mode(url, html):
    soup = BeautifulSoup(html, "html.parser")

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

    count, rating = score_selector(soup, selector)

    print("\nSuggested selector:")
    print(selector)

    print(f"\nMatches: {count} → {rating}")
