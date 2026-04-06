import json
from tractor.utils.errors import ConfigError


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    required = ["url", "item", "fields"]

    for key in required:
        if key not in config:
            raise ConfigError(f"Missing field: {key}")
