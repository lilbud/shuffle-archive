import datetime
import json
import os
from pathlib import Path

import ftfy
import html_to_markdown
import psycopg
from bs4 import BeautifulSoup as bs4
from dotenv import load_dotenv
from psycopg.rows import dict_row

from cleanup import format_article_content
from database import load_db

post_folder = Path("./archive/posts/")
json_folder = Path("./posts_json/")


def archive_posts(cur: psycopg.Cursor) -> None:
    """Export posts from database as HTML and MD."""
    posts = cur.execute(
        """SELECT * FROM posts order by post_id""",
    ).fetchall()

    for post in posts:
        date = post["published"].date()

        # if not Path(f"./archive/posts/{date}_{post['slug']}").exists():
        print(f"./archive/posts/{date}_{post['slug']}")
        post_id = post["post_id"]

        date = post["published"].date()
        last_modified = int(post["last_modified"].timestamp())

        print(f"{post_id}_{last_modified}")

        # create folder
        save_path = Path(f"./archive/posts/{date}_{post['slug']}")
        save_path.mkdir(exist_ok=True)

        content = format_article_content(post["content"])

        if not Path(save_path, "meta.json").exists():
            with Path(f"./posts_json/{post_id}_{last_modified}.json").open(
                "r",
                encoding="utf-8",
            ) as f:
                post_file = json.load(f)

            # add database UUID to the post dict
            new_post_dict = {"uuid": str(post["id"]), **post_file}

            # save the updated dict to the post folder
            with Path(save_path, "meta.json").open("w", encoding="utf-8") as f:
                json.dump(new_post_dict, f)

            print("created json")

        if not Path(save_path, "post.html").exists():
            # write post HTML from database to post folder
            with Path(save_path, "post.html").open("w", encoding="utf-8") as f:
                f.write(content)

        if not Path(save_path, "post.md").exists():
            # convert post to markdown and save
            with Path(save_path, "post.md").open("w", encoding="utf-8") as f:
                f.write(html_to_markdown.convert(content))


with load_db() as conn, conn.cursor() as cur:
    archive_posts(cur)
