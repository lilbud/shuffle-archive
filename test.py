import datetime
import json
from pathlib import Path

import html_to_markdown

from cleanup import initial_cleanup

posts = Path(r".\archive\posts")
json_posts = Path(r".\posts_json")

tags = []


if __name__ == "__main__":
    for file in json_posts.iterdir():
        post = json.loads(file.read_text(encoding="utf-8"))

        post_id = post["id"]

        date = datetime.datetime.strptime(
            post["modified_gmt"],
            "%Y-%m-%dT%H:%M:%S",
        )

        save_path = Path(f"./archive/posts/{date.date()}_{post['slug']}")

        print(save_path)
        save_path.mkdir(exist_ok=True)

        content = initial_cleanup(post["content"]["rendered"])
        content = html_to_markdown.convert(content)

        if not Path(save_path, "meta.json").exists():
            with Path(save_path, "meta.json").open("w", encoding="utf-8") as f:
                json.dump(post, f)

            print("created json")

        # convert post to markdown and save
        if not Path(save_path, "post.md").exists():
            with Path(save_path, "post.md").open("w", encoding="utf-8") as f:
                f.write(content)

            print("created md")
