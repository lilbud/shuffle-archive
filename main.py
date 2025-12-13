import datetime
import json
import re
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
from user_agent import generate_user_agent

categories = {
    1: "uncategorized",
    2: "kingdom-of-days",
    3: "roll-of-the-dice",
    4: "cover-me",
    5: "meeting-across-the-river",
    152: "where-the-band-was",
    2295: "hearts-of-stone",
    2583: "spare-parts",
    3326: "two-faces",
    3601: "greetings",
    3602: "holiday",
    3603: "encore",
    3604: "tunnel",
}

# def get_page(page: int):

authors = {
    1: "Ken Rosen",
}

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
    # fields: link, name

    for file in folder.iterdir():
        data = json.loads(file.read_text())

        for tag in data:
            tags[tag["id"]] = {
                "name": tag["name"],
                "url": tag["link"],
            }

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


def get_posts_by_page(client: httpx.Client, page: int = 1) -> dict | None:
    url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?per_page=25&page={page}"

    try:
        res = client.get(url)
        return res.json()
    except httpx.HTTPError:
        return None


def get_latest_posts() -> None:
    """Get latest posts from the site.

    Posts are saved in individual files, named with their post_id.
    """
    with httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=30,
    ) as client:
        existing_posts = {int(i.stem) for i in Path("./posts").iterdir()}

        res = client.get(
            "https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?per_page=25",
        )

        total_posts = int(res.headers["x-wp-total"])
        total_pages = int(res.headers["x-wp-totalpages"])

        if total_pages > 1:
            print(
                f"Found {total_pages} pages and {total_posts} posts",
            )

            for i in range(1, total_pages + 1):
                print(f"Page {i}")

                url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?page={i}&per_page=25"
                res = client.get(url)

                posts = get_posts_by_page(client, i)

                if posts:
                    post_ids = {int(post["id"]) for post in posts}

                    if not post_ids.issubset(existing_posts):
                        print("found unsaved posts")
                        for post in posts:
                            save_path = Path(f"./posts/{post['id']}.json")

                            if not save_path.exists():
                                print(f"{save_path.name} doesn't exist")

                                with save_path.open("w", encoding="utf-8") as f:
                                    json.dump(post, f)
                    else:
                        print("all posts already saved, exiting")
                        break

        print("-" * 20)


if __name__ == "__main__":
    get_latest_posts()
