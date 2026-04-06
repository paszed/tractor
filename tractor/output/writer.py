import json
from typing import Iterable, Dict, Any


def write(data: Iterable[Dict[str, Any]], format: str = "jsonl") -> None:
    if format == "jsonl":
        for item in data:
            print(json.dumps(item, ensure_ascii=False))

    elif format == "json":
        print(json.dumps(list(data), indent=2, ensure_ascii=False))

    else:
        raise ValueError("Invalid format")
