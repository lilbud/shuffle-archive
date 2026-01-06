import datetime
import json
import re
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import ftfy
import httpx
import psycopg
from psycopg.rows import dict_row
from user_agent import generate_user_agent

from cleanup import format_article_content
from database import insert_post, load_db

cookies = {"wordpress_test_cookie": "WP Cookie check"}
headers = {
    "User-Agent": generate_user_agent(),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Cookie": "wordpress_test_cookie=WP%20Cookie%20check",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=0, i",
}


def get_tags() -> None:
    """Get all tags using WP REST API."""
    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=20,
    ) as client:
        res = client.get(
            "https://estreetshuffle.com/index.php/wp-json/wp/v2/tags?per_page=100",
        )

        save_path = Path("./tags")
        total_pages = int(res.headers["x-wp-totalpages"])

        if total_pages > 1:
            print(f"Found {total_pages} of tags")

            for i in range(1, total_pages + 1):
                url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/tags?per_page=100&page={i}"

                try:
                    res = client.get(url)

                    print(f"saving page {i} to {save_path}")

                    with Path(save_path, f"{i}.json").open("w") as f:
                        json.dump(res.json(), f)

                    for tag in res.json():
                        cur.execute(
                            """INSERT INTO tags (tag_id, name, slug) VALUES (%s, %s, %s)""",
                            (tag["id"], ftfy.fix_text(tag["name"]), tag["slug"]),
                        )
                except httpx.HTTPError:
                    pass

                time.sleep(1)


def get_categories() -> None:
    """Get all categories using WP REST API."""
    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=20,
    ) as client:
        res = client.get(
            "https://estreetshuffle.com/index.php/wp-json/wp/v2/categories?per_page=100",
        )

        save_path = Path("./categories")

        url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/categories?per_page=100&page=1"

        res = client.get(url)

        with Path(save_path, f"categories.json").open("w") as f:
            json.dump(res.json(), f)

        for cat in res.json():
            cur.execute(
                """INSERT INTO categories (category_id, name) VALUES (%s, $s) ON CONFLICT (category_id) DO NOTHING""",
                (cat["id"], cat["name"]),
            )


def get_posts_by_page(client: httpx.Client, url: str) -> httpx.Response | None:
    """Make request to WP API and return response."""
    try:
        return client.get(url)
    except httpx.HTTPError:
        return None


def get_media(cur: psycopg.Cursor, conn: psycopg.Connection):
    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=60,
    ) as client:
        media = cur.execute(
            """SELECT media_id FROM media WHERE url IS NULL""",
        ).fetchall()

        if len(media) > 1:
            print(f"{len(media)} objects missing URL, grabbing now")

            for row in media:
                print(row["media_id"])

                res = client.get(
                    f"https://estreetshuffle.com/index.php/wp-json/wp/v2/media/{row['media_id']}"
                )

                if res:
                    data = res.json()
                    try:
                        url = data["guid"]["rendered"]

                        cur.execute(
                            """UPDATE media SET url = %s WHERE media_id = %s""",
                            (url, row["media_id"]),
                        )
                    except KeyError:
                        continue

                    conn.commit()

                time.sleep(1)

        else:
            print(f"no missing media URLs")


def save_posts(posts: list[dict], cur: psycopg.Cursor) -> None:
    """Iterate list of post dicts and save each to file."""
    for post in posts:
        timestamp = datetime.datetime.strptime(
            post["modified_gmt"],
            "%Y-%m-%dT%H:%M:%S",
        ).timestamp()

        save_path = Path(f"./posts/{post['id']}_{int(timestamp)}.json")

        if not save_path.exists():
            with save_path.open("w", encoding="utf-8") as f:
                json.dump(post, f)

        insert_post(post, cur)


def get_latest_posts(cur: psycopg.Cursor) -> None:
    """Get posts ordered by modified date.

    Rather than creating new posts, the site is instead opting to replace the content of
    old posts with new content. This is a problem for a few reasons. Namely that the
    "replaced" posts are basically gone without being archived.

    This function grabs those posts and saves them separately from the originals.
    """
    page = 1
    url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?per_page=25&page={page}&order=desc&orderby=modified"

    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=60,
    ) as client:
        res = get_posts_by_page(client=client, url=url)

        if res:
            total_posts = int(res.headers["x-wp-total"])
            total_pages = int(res.headers["x-wp-totalpages"])

            print(
                f"Found {total_pages} pages and {total_posts} posts",
            )

            cur.execute(
                """INSERT INTO update_log (pages, posts, created_at) values(%s, %s, %s)""",
                (
                    total_pages,
                    total_posts,
                    datetime.datetime.now().astimezone(datetime.UTC),
                ),
            )

            posts = res.json()
            save_posts(posts, cur)


def get_newest_posts(cur: psycopg.Cursor) -> None:
    """Get newest posts from the site.

    Posts are saved in individual files, as well as inserted into database.
    """
    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=60,
    ) as client:
        page = 1
        url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?per_page=25&page={page}"
        res = get_posts_by_page(client, url)

        if res:
            total_posts = int(res.headers["x-wp-total"])
            total_pages = int(res.headers["x-wp-totalpages"])

            print(
                f"Found {total_pages} pages and {total_posts} posts",
            )

            # cur.execute(
            #     """INSERT INTO update_log (pages, posts, created_at) values(%s, %s, %s)""",
            #     (total_pages, total_posts, datetime.datetime.now()),
            # )

            posts = res.json()
            save_posts(posts, cur)

        # if total_pages > 1:
        #     for i in range(2, total_pages + 1):
        #         print(f"Page {i}")

        #         res = get_posts_by_page(client, i)

        #         if res:
        #             posts = res.json()

        #             post_ids = {int(post["id"]) for post in posts}

        #             if not post_ids.issubset(existing_posts):
        #                 print("found unsaved posts")
        #                 save_posts(posts, db_posts, cur)
        #             else:
        #                 print("posts already saved, exiting")
        #                 break


if __name__ == "__main__":
    with load_db() as conn, conn.cursor() as cur:  # noqa: SIM117
        print("Grabbing newest posts.")
        get_newest_posts(cur)

        print("Grabbing recently updated posts.")
        get_latest_posts(cur)

        # get_media(cur, conn)
