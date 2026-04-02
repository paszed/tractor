from bs4 import BeautifulSoup


def score_selector(soup, selector):
    try:
        matches = soup.select(selector)
        count = len(matches)
    except Exception:
        return 0, "invalid ❌"

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


def generate_candidates(el):
    candidates = []

    # base element
    candidates.append(el.name)

    parent = el.parent

    if parent:
        # parent + element
        candidates.append(f"{parent.name} {el.name}")

        # parent.class + element
        if parent.get("class"):
            cls = ".".join(parent.get("class")[:2])
            candidates.append(f"{parent.name}.{cls} {el.name}")

        # parent id
        if parent.get("id"):
            candidates.append(f"#{parent.get('id')} {el.name}")

    return list(dict.fromkeys(candidates))  # remove duplicates


def pick_best_selector(soup, candidates):
    best = None
    best_score = -1
    best_count = float("inf")

    print("\nTrying selectors:\n")

    for sel in candidates:
        count, rating = score_selector(soup, sel)
        print(f"{sel} → {count} ({rating})")

        # scoring tiers
        if 5 <= count <= 100:
            score = 3
        elif 2 <= count < 5:
            score = 2
        elif count == 1:
            score = 1
        else:
            score = 0

        # 🔥 key improvement:
        # prefer higher score AND lower count
        if score > best_score or (score == best_score and count < best_count):
            best_score = score
            best_count = count
            best = sel

    return best



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

    candidates = generate_candidates(el)
    best = pick_best_selector(soup, candidates)

    print("\nBest selector:")
    print(best)
