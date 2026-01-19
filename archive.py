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

from cleanup import initial_cleanup
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

        # create folder
        save_path = Path(f"./archive/posts/{date}_{post['slug']}")
        save_path.mkdir(exist_ok=True)

        soup = bs4(post["content"], "html.parser")

        if not soup.find("html"):
            new_html = soup.new_tag("html", lang="en")
            head = soup.new_tag("head")
            meta = soup.new_tag("meta", charset="UTF-8")
            title = soup.new_tag("title")
            title.string = post["title"]
            head.append(meta)
            head.append(title)

            body = soup.new_tag("body")
            # Move existing content into the new body
            for element in list(soup.contents):
                body.append(element.extract())

            new_html.append(head)
            new_html.append(body)
            soup.append(new_html)

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

        # write post HTML from database to post folder
        # if not Path(save_path, "post.html").exists():
        with Path(save_path, "post.html").open("w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write(str(soup))

        if not Path(save_path, "post.md").exists():
            # convert post to markdown and save
            with Path(save_path, "post.md").open("w", encoding="utf-8") as f:
                f.write(html_to_markdown.convert(str(soup)))


if __name__ == "__main__":
    with load_db() as conn, conn.cursor() as cur:
        archive_posts(cur)
