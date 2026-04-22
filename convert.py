import re
from pathlib import Path

post_folder = Path("./archive/posts/")

for post in post_folder.iterdir():
    print(post.name)
    if post.is_dir():
        post_path = Path(post, "post.md")

        post_text = post_path.read_text(encoding="utf-8")

        bold_fixed = re.sub(
            r"^\*{2}([^*]+?)\s*$",
            r"**\1**",
            post_text,
            flags=re.MULTILINE,
        )
        trimmed = re.sub(r"\s+$", r"", bold_fixed)

        with Path(post, "post.md").open("w", encoding="utf-8") as f:
            f.write(trimmed)
