import datetime
import json
import os
from pathlib import Path

import ftfy
import html_to_markdown
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

from cleanup import initial_cleanup

load_dotenv()

DATABASE_URL = "postgresql://postgres:password@localhost:5432/shuffle"


def load_db() -> psycopg.Connection:
    """Load DB and return connection."""
    return psycopg.connect(
        conninfo=DATABASE_URL,
        row_factory=dict_row,
    )


def insert_post(data: dict, cur: psycopg.Cursor, conn: psycopg.Connection) -> None:
    """Insert post into database.

    Posts are only inserted if the post_id and modified date in the
    API response object are different than the one in the database.
    """
    id = data["id"]
    url = data["link"]

    published = datetime.datetime.strptime(
        data["date_gmt"],
        "%Y-%m-%dT%H:%M:%S",
    )

    last_modified = datetime.datetime.strptime(
        data["modified_gmt"],
        "%Y-%m-%dT%H:%M:%S",
    )

    title = ftfy.fix_text(data["title"]["rendered"])

    content = initial_cleanup(data["content"]["rendered"])

    excerpt = html_to_markdown(data["excerpt"]["rendered"])

    # the only author on the site is Ken, so no point in querying with only one result.
    author = "c8f4a2a5-a55d-4ef7-82d3-d59a8940c107"

    # post = cur.execute(
    #     """select id, post_id, last_modified from posts where post_id = %s and last_modified = %s""",
    #     (id, last_modified),
    # ).fetchone()

    cur.execute(
        """INSERT INTO posts (post_id, published, last_modified, url, title, content, excerpt, author, slug)
            values (%(id)s, %(published)s, %(last_modified)s, %(url)s, %(title)s, %(content)s, %(excerpt)s, %(author)s, %(slug)s)
            on conflict (post_id, last_modified) do nothing""",
        {
            "id": id,
            "published": published,
            "last_modified": last_modified,
            "url": url,
            "title": title,
            "content": content,
            "excerpt": excerpt,
            "author": author,
            "slug": data["slug"],
        },
    )

    conn.commit()

    # print(f"Successfully inserted post {id}")

    post_id = cur.execute(
        """select id, post_id, last_modified from posts where post_id = %s and last_modified = %s""",
        (id, last_modified),
    ).fetchone()["id"]

    if post_id and int(data["featured_media"]) != 0:
        cur.execute(
            """insert into media (media_id, url, post_id)
                values (%(media)s, %(url)s, %(post)s) on conflict do nothing""",
            {"media": int(data["featured_media"]), "url": None, "post": post_id},
        )

        media = cur.execute(
            """select id from media where media_id = %(media)s""",
            {"media": int(data["featured_media"])},
        ).fetchone()["id"]

        cur.execute(
            """update posts set featured_media = %(media)s where post_id = %(post)s""",
            {"media": media, "post": id},
        )

    for item in data["categories"]:
        category = cur.execute(
            """select id from categories where category_id = %(category)s""",
            {"category": item},
        ).fetchone()["id"]

        cur.execute(
            """INSERT INTO post_categories (post_id, category_id)
            VALUES (%(post)s, %(category)s) on conflict do nothing""",
            {"post": post_id, "category": category},
        )

    for item in data["tags"]:
        tag = cur.execute(
            """select id from tags where tag_id = %(tag)s""",
            {"tag": item},
        ).fetchone()["id"]

        cur.execute(
            """INSERT INTO post_tags (post_id, tag_id)
            VALUES (%(post)s, %(tag)s) on conflict do nothing""",
            {"post": post_id, "tag": tag},
        )

    for item in data["jetpack-related-posts"]:
        related = cur.execute(
            """select id from posts where post_id = %(post)s""",
            {"post": item["id"]},
        ).fetchone()["id"]

        cur.execute(
            """INSERT INTO related_posts (post_id, related_post) VALUES (%(post)s, %(related)s) on conflict do nothing""",
            {"post": post_id, "related": related},
        )
