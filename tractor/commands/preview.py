from tractor.config import load_config
from tractor.pipeline.runner import run_pipeline


def run_command(config_path: str, limit: int = 5) -> None:
    config = load_config(config_path)

    for i, item in enumerate(run_pipeline(config)):
        print(item)
        if i + 1 >= limit:
            break
