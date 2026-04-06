from tractor.config import load_config
from tractor.pipeline.runner import run_pipeline
from tractor.output.writer import write


def run_command(config_path: str, format: str = "jsonl") -> None:
    config = load_config(config_path)

    data = run_pipeline(config)

    write(data, format=format)
