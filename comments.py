import datetime
import json
import re
from pathlib import Path

import html_to_markdown
import httpx
import psycopg
import tidy
from bs4 import BeautifulSoup as bs4

from cleanup import clean_file
from database import insert_post, load_db


def insert_comment(cur: psycopg.Cursor, comment: dict):
    comment_id = comment.get("id")

    date = datetime.datetime.strptime(
        comment["date_gmt"],
        "%Y-%m-%dT%H:%M:%S",
    )

    post = cur.execute(
        """select id from posts where post_id = %s and published <= %s""",
        (comment.get("post"), date),
    ).fetchone()["id"]

    author = cur.execute(
        """select id from authors where name = %s""",
        (comment.get("author_name"),),
    ).fetchone()["id"]

    content = html_to_markdown.convert(comment["content"]["rendered"])

    cur.execute(
        """insert into comments (comment_id, author, post, text, published) values (%s,%s,%s,%s,%s)""",
        (comment_id, author, post, content, date),
    )


def get_comment(comment_id: int, cur: psycopg.Cursor) -> dict:
    """Get single comment by ID."""
    return cur.execute(
        "select * from comments where comment_id = %s",
        (comment_id,),
    ).fetchone()


if __name__ == "__main__":
    with load_db() as conn, conn.cursor() as cur:
        authors = []
        comments: list[dict] = json.load(Path("comments.json").open())

        for item in comments:
            try:
                insert_comment(cur, item)
            except TypeError:
                print(item.get("id"))
