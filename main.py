import datetime
import json
from pathlib import Path

import httpx
from user_agent import generate_user_agent

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


def get_client() -> httpx.Client:
    """Return httpx client with headers and cookies."""
    return httpx.Client(
        headers=headers,
        cookies=cookies,
        timeout=60,
    )


def get_posts_by_page(client: httpx.Client, url: str) -> httpx.Response | None:
    """Make request to WP API and return response."""
    try:
        return client.get(url)
    except httpx.HTTPError:
        return None


def save_posts(
    posts: list[dict],
) -> None:
    """Iterate list of post dicts and save each to file."""
    for post in posts:
        timestamp = datetime.datetime.strptime(
            post["modified_gmt"],
            "%Y-%m-%dT%H:%M:%S",
        ).timestamp()

        save_path = Path(f"./posts_json/{post['id']}_{int(timestamp)}.json")

        if not save_path.exists():
            with save_path.open("w", encoding="utf-8") as f:
                json.dump(post, f)


def get_latest_posts() -> None:
    """Get posts ordered by modified date.

    Rather than creating new posts, the site is instead opting to replace the content of
    old posts with new content. This is a problem for a few reasons. Namely that the
    "replaced" posts are basically gone without being archived.

    This function grabs those posts and saves them separately from the originals.
    """
    page = 1
    url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/posts?per_page=25&page={page}&order=desc&orderby=modified"

    with get_client() as client:
        res = get_posts_by_page(client=client, url=url)

        if res:
            total_posts = int(res.headers["x-wp-total"])
            total_pages = int(res.headers["x-wp-totalpages"])

            print(
                f"Found {total_pages} pages and {total_posts} posts",
            )

            posts = res.json()
            save_posts(posts)
