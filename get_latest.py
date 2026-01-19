import datetime
import json
from pathlib import Path

import httpx
import psycopg
from user_agent import generate_user_agent

from main import get_posts_by_page

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


def get_latest_posts() -> None:
    """Get posts ordered by modified date.

    This function is a modified version of the one in main,
    which will be used in a github action.
    """
    page = 1
    url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?per_page=100&page={page}&order=desc&orderby=modified"

    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=60,
    ) as client:
        try:
            res = client.get(url)
        except httpx.HTTPError:
            res = None

    if res:
        total_posts = int(res.headers["x-wp-total"])
        total_pages = int(res.headers["x-wp-totalpages"])

        print(
            f"Found {total_pages} pages and {total_posts} posts",
        )

        with Path("./notes/report.txt").open("a") as f:
            f.write(
                f"{datetime.datetime.now().astimezone(datetime.UTC)} Found {total_pages} pages and {total_posts} posts",
            )

        posts = res.json()

        for post in posts:
            timestamp = datetime.datetime.strptime(
                post["modified_gmt"],
                "%Y-%m-%dT%H:%M:%S",
            ).timestamp()

            save_path = Path(f"./posts_json/{post['id']}_{int(timestamp)}.json")

            if not save_path.exists():
                with save_path.open("w", encoding="utf-8") as f:
                    json.dump(post, f)


if __name__ == "__main__":
    get_latest_posts()
