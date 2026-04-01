import json


def output(data, format="text"):
    if format == "json":
        print(json.dumps(data, indent=2))
    else:
        for item in data:
            print(item)
