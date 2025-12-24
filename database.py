import datetime
import json
import os
from pathlib import Path

import ftfy
import html_to_markdown
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

from cleanup import format_article_content

load_dotenv()

DATABASE_URL = "postgresql://postgres:password@localhost:5432/shuffle"


def load_db() -> psycopg.Connection:
    """Load DB and return connection."""
    return psycopg.connect(
        conninfo=DATABASE_URL,
        row_factory=dict_row,
    )


def insert_post(data: dict, cur: psycopg.Cursor) -> None:
    """Insert post into database."""
    id = data["id"]
    url = data["link"]

    published = datetime.datetime.strptime(
        data["date_gmt"],
        "%Y-%m-%dT%H:%M:%S",
    ).astimezone(datetime.UTC)

    last_modified = datetime.datetime.strptime(
        data["modified_gmt"],
        "%Y-%m-%dT%H:%M:%S",
    ).astimezone(datetime.UTC)

    title = ftfy.fix_text(data["title"]["rendered"])

    content = format_article_content(data["content"]["rendered"])

    excerpt = data["excerpt"]["rendered"]

    author = cur.execute(
        """select id from authors where author_id = %(id)s""",
        {"id": int(data["author"])},
    ).fetchone()["id"]

    cur.execute(
        """INSERT INTO posts (post_id, published, last_modified, url, title, content, excerpt, author, slug)
            values (%(id)s, %(published)s, %(last_modified)s, %(url)s, %(title)s, %(content)s, %(excerpt)s, %(author)s, %(slug)s)
            on conflict (post_id,published) do nothing""",
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

    print(f"Successfully inserted post {id}")

    post_id = cur.execute(
        """select id from posts where post_id = %(id)s""",
        {"id": id},
    ).fetchone()["id"]

    if post_id:
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


if __name__ == "__main__":
    with load_db() as conn, conn.cursor() as cur:
        for post in Path("./posts").iterdir():
            data = json.load(post.open())

            post_id = data["id"]
            slug = data["slug"]

            print(post_id)

            cur.execute(
                """UPDATE posts SET slug=%s WHERE post_id = %s""",
                (slug, post_id),
            )
