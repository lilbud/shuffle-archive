import datetime
import json
import re
from pathlib import Path

import html_to_markdown

from cleanup import initial_cleanup


def extra_fixes(content: str) -> str:
    """Apply a few fixes for missing bolded tags."""
    for line in content.split("\n"):
        # missing ending bold tag
        if line.startswith("**") and not line.endswith("**") and ":**" not in line:
            content = content.replace(line, f"{line}**")

        # missing starting bold tag
        if not line.startswith("**") and ":**" in line:
            content = content.replace(line, f"**{line}")

        # add blockquote marker to italic lines
        if line.startswith("*") and line.endswith("*") and ":*" not in line:
            content = content.replace(line, f"> {line}")

    return content


def save_to_archive(post: dict) -> None:
    """Save post to archive folder as MD and JSON."""
    date = datetime.datetime.strptime(
        post["modified_gmt"],
        "%Y-%m-%dT%H:%M:%S",
    )

    content = initial_cleanup(post["content"]["rendered"])
    content = html_to_markdown.convert(content)

    content = extra_fixes(content)

    save_path = Path(f"./archive/posts/{date.date()}_{post['slug']}")

    # print(save_path)
    save_path.mkdir(exist_ok=True)

    if not save_path.exists():
        print(save_path.name)
    else:
        print(f"{save_path.name}: already exists")

    if not Path(save_path, "meta.json").exists():
        with Path(save_path, "meta.json").open("w", encoding="utf-8") as f:
            json.dump(post, f)

        print(f"{save_path.name}: created json")

    # convert post to markdown and save
    if not Path(save_path, "post.md").exists():
        with Path(save_path, "post.md").open("w", encoding="utf-8") as f:
            f.write(content)

        print(f"{save_path.name}: created md")


# for file in Path("./posts_json/").glob("*.json"):
#     with file.open("r", encoding="utf-8") as f:
#         post = json.load(f)
#         save_to_archive(post)
