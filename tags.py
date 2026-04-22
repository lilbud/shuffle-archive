import json
from pathlib import Path

import httpx

from main import get_client


def get_tags() -> None:
    """Get all tags using WP REST API."""
    tags = []

    with get_client() as client:
        res = client.get(
            "https://estreetshuffle.com/index.php/wp-json/wp/v2/tags?per_page=100",
        )

        total_pages = int(res.headers["x-wp-totalpages"])

        if total_pages > 1:
            print(f"Found {total_pages} of tags")

            for i in range(1, total_pages + 1):
                url = f"https://estreetshuffle.com/index.php/wp-json/wp/v2/tags?per_page=100&page={i}"

                try:
                    res = client.get(url)

                    if res:
                        for tag in res.json():
                            tags.append(tag)  # noqa: PERF402

                except httpx.HTTPError:
                    pass

            with Path("tags.json").open("w") as f:
                json.dump(tags, f)

        else:
            with Path("tags.json").open("w") as f:
                json.dump(res.json(), f)
