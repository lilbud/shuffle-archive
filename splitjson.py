import json
from pathlib import Path


def split_json(base_dir: Path) -> None:
    """Split category pages into separate post json files."""
    for folder in base_dir.iterdir():
        for file in folder.iterdir():
            data = [dict(item) for item in json.loads(file.read_text())]
            for item in data:
                id = item["id"]

                with Path(f"./posts/{id}.json").open("w", encoding="utf-8") as f:
                    json.dump(item, f)
