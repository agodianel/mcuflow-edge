import json
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict, indent: int = 2) -> None:
    path.write_text(json.dumps(data, indent=indent) + "\n")
