import json
from pathlib import Path

if __name__ == "__main__":
    file = Path(
        r"..\bookshelf_collection\cover-me-2\pixxibook.com_Archive [26-01-28 23-12-54].har",
    )

    data = json.load(
        file.open(),
    )

    images = []
    for item in data["log"]["entries"]:
        image_url = item["request"]["url"]
        print(image_url)
        images.append(image_url)

    with Path(file.parent, "list.txt").open("w") as f:
        for img in images:
            f.write(f"{img}\n")
