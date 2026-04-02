import json
import csv
import sys


def output(data, format="text", file=None):
    # JSON output
    if format == "json":
        content = json.dumps(data, indent=2)

        if file:
            with open(file, "w") as f:
                f.write(content)
        else:
            print(content)

    # CSV output
    elif format == "csv":
        if not data:
            return

        # ensure list of dicts
        if not isinstance(data[0], dict):
            data = [{"value": item} for item in data]

        keys = data[0].keys()

        if file:
            with open(file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    # text output (default)

    else:
        content = "\n".join(str(item) for item in data)

        if file:
            with open(file, "w") as f:
                f.write(content)
        else:
            print(content)
