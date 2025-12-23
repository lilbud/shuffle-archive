import datetime
import json
import re
import time
from pathlib import Path
from zoneinfo import ZoneInfo

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


def generate_tag_list() -> None:
    """Combine tag json files into a single json file."""
    folder = Path("./tags")

    tags = {}

    for file in folder.iterdir():
        data = json.loads(file.read_text())

        for tag in data:
            tags[tag["id"]] = tag

    json.dump(tags, Path("./tags.json").open("w"))


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
                except httpx.HTTPError:
                    pass

                time.sleep(1)


def get_posts_by_page(client: httpx.Client, page: int = 1) -> httpx.Response | None:
    url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?per_page=25&page={page}"

    try:
        return client.get(url)
    except httpx.HTTPError:
        return None


def save_posts(posts: list[dict], db_posts: list[int], cur: psycopg.Cursor):
    for post in posts:
        save_path = Path(f"./posts/{post['id']}.json")

        if save_path.exists():
            print(f"post {post['id']} already saved")
        else:
            print(f"saving post {post['id']}")
            with save_path.open("w", encoding="utf-8") as f:
                json.dump(post, f)

        if post["id"] not in db_posts:
            print("inserting post into database")
            insert_post(post, cur)


def get_latest_posts(cur: psycopg.Cursor) -> None:
    """Get latest posts from the site.

    Posts are saved in individual files, named with their post_id.
    """
    db_posts = [
        int(post["id"])
        for post in cur.execute(
            """SELECT DISTINCT post_id as id from posts""",
        ).fetchall()
    ]

    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=30,
    ) as client:
        existing_posts = {int(i.stem) for i in Path("./posts").iterdir()}
        res = get_posts_by_page(client, 1)

        total_posts = int(res.headers["x-wp-total"])
        total_pages = int(res.headers["x-wp-totalpages"])

        print(
            f"Found {total_pages} pages and {total_posts} posts",
        )

        with Path("./notes/report.txt").open("a") as f:
            f.write(
                f"\n{datetime.datetime.now()} Found {total_pages} pages and {total_posts} posts",
            )

        if res:
            posts = res.json()
            save_posts(posts, db_posts, cur)

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
    with load_db() as conn, conn.cursor() as cur:
        get_latest_posts(cur)
