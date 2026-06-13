import datetime
import json
import re
from pathlib import Path

import html_to_markdown

from cleanup import initial_cleanup


def extra_fixes(content: str) -> str:
    """Apply a few fixes to resulting markdown."""
    for line in content.split("\n"):
        # missing ending bold tag
        if line.startswith("**") and not line.endswith("**") and ":**" not in line:
            content = content.replace(line, f"{line}**")

        # missing starting bold tag
        if not line.startswith("**") and ":**" in line:
            content = content.replace(line, f"**{line}")

        # add blockquote marker to italic lines
        if (
            line.startswith("*")
            and line.endswith("*")
            and ":*" not in line
            and "![]" not in line
        ):
            content = content.replace(line, f"> {line}")

    return content


def save_to_archive(post: dict, save_path: Path) -> None:
    """Save post to archive folder as MD and JSON."""
    content = initial_cleanup(post["content"]["rendered"])
    content = html_to_markdown.convert(content)

    content = extra_fixes(content)

    if not save_path.exists():
        print(save_path.name)
        save_path.mkdir(exist_ok=True)
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


if __name__ == "__main__":
    for file in Path("./posts_json/").glob("*.json"):
        with file.open("r", encoding="utf-8") as f:
            post = json.load(f)

            date = datetime.datetime.strptime(
                post["modified_gmt"],
                "%Y-%m-%dT%H:%M:%S",
            )

            save_path = Path(f"./archive/posts/{date.date()}_{post['slug']}")

            # only save post if it doesn't already exist and title isn't a number
            # post with a numerical title are image pages and are new, but have no content
            if not save_path.exists() and not re.search(
                r"^\d+$",
                post["slug"],
            ):
                save_to_archive(post, save_path)
                print(save_path)
