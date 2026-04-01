import json


def output(data, format="text", file=None):
    if format == "json":
        content = json.dumps(data, indent=2)
    else:
        content = "\n".join(str(item) for item in data)
        
    if file:
        with open(file, "w") as f:
            f.write(content)
    else:
        print(content)
