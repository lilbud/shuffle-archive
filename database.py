import datetime
import json
import os
import re
from pathlib import Path

import ftfy
import html_to_markdown
import psycopg
import unidecode
from dotenv import load_dotenv
from psycopg.rows import dict_row

from cleanup import initial_cleanup

load_dotenv()

DATABASE_URL = "postgresql://postgres:password@localhost:5432/shuffle_new"


def load_db() -> psycopg.Connection:
    """Load DB and return connection."""
    return psycopg.connect(
        conninfo=DATABASE_URL,
        row_factory=dict_row,
    )


def insert_post() -> None:
    """Insert post into database."""
    post_dir = Path("./archive/posts")

    with load_db() as conn, conn.cursor() as cur:
        for post in post_dir.iterdir():
            content = Path(post / "post.md").read_text(encoding="utf-8")
            meta = json.loads(Path(post / "meta.json").read_text())

            content = re.sub("^---[\\s\\S]+?---\n?", "", content)

            post_id = meta["id"]
            slug = meta["slug"]
            link = meta["link"]

            published = datetime.datetime.strptime(
                f"{meta['date_gmt']}+0000",
                "%Y-%m-%dT%H:%M:%S%z",
            ).astimezone(datetime.timezone.utc)

            last_modified = datetime.datetime.strptime(
                meta["modified_gmt"],
                "%Y-%m-%dT%H:%M:%S",
            )

            print(post_id, published)
            title = ftfy.fix_text(meta["title"]["rendered"])
            excerpt = html_to_markdown.convert(meta["excerpt"]["rendered"])

            media = meta["featured_media"]
            author = meta["author"]

            if media == 0:
                media = None
            else:
                try:
                    cur.execute(
                        """insert into featured_media (id) values (%s) on conflict (id) do nothing""",
                        (media,),
                    )
                    conn.commit()
                except psycopg.errors.InFailedSqlTransaction:
                    media = None

            cur.execute(
                """INSERT INTO posts (post_id, published, last_modified, title, content, excerpt, featured_media, author_id, slug, url)
                                values (%(id)s, %(published)s, %(last_modified)s, %(title)s, %(content)s, %(excerpt)s, %(media)s, %(author)s, %(slug)s, %(link)s)
                                on conflict (post_id, last_modified) do update set content=%(content)s""",
                {
                    "id": post_id,
                    "published": published,
                    "last_modified": last_modified,
                    "title": title,
                    "content": content,
                    "excerpt": excerpt,
                    "media": media,
                    "author": author,
                    "slug": slug,
                    "link": link,
                },
            )

            conn.commit()

            db_post_id = cur.execute(
                """select id from posts where post_id = %(id)s and last_modified = %(last_modified)s""",
                {"id": post_id, "last_modified": last_modified},
            ).fetchone()

            for tag in meta["tags"]:
                try:
                    cur.execute(
                        """insert into post_tags (tag_id, post_id) values (%(tag)s, %(post)s) on conflict (tag_id, post_id) do nothing""",
                        {"tag": tag, "post": db_post_id["id"]},
                    )
                except (
                    psycopg.errors.ForeignKeyViolation,
                    psycopg.errors.InFailedSqlTransaction,
                ) as e:
                    print(f"CATEGORY INSERT FAILED: {e}")
                    continue

            for category in meta["categories"]:
                try:
                    cur.execute(
                        """insert into post_categories (category_id, post_id) values (%(category)s, %(post)s) on conflict (category_id, post_id) do nothing""",
                        {"category": category, "post": db_post_id["id"]},
                    )
                except (
                    psycopg.errors.ForeignKeyViolation,
                    psycopg.errors.InFailedSqlTransaction,
                ) as e:
                    print(f"TAG INSERT FAILED: {e}")
                    continue

            for rp in meta["jetpack-related-posts"]:
                try:
                    rel_id = cur.execute(
                        """select id from posts where post_id = %(id)s order by published asc limit 1""",
                        {"id": rp["id"]},
                    ).fetchone()
                except Exception:
                    continue

                try:
                    cur.execute(
                        """insert into related_posts (related_post_id, post_id) values (%(related_post)s, %(post)s) on conflict (related_post_id, post_id) do nothing""",
                        {"related_post": rel_id["id"], "post": db_post_id["id"]},
                    )
                except TypeError:
                    continue


if __name__ == "__main__":
    insert_post()
