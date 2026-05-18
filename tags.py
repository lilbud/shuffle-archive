import json
from pathlib import Path

import httpx
import psycopg
from psycopg.rows import dict_row

from main import get_client

DATABASE_URL = "postgresql://postgres:password@localhost:5432/shuffle_new"


def load_db() -> psycopg.Connection:
    """Load DB and return connection."""
    return psycopg.connect(
        conninfo=DATABASE_URL,
        row_factory=dict_row,
    )


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


def insert_tags() -> None:
    """Insert tags into database."""
    with load_db() as conn, conn.cursor() as cur:
        with Path("tags.json").open("r") as f:
            tags = json.load(f)

            for tag in tags:
                cur.execute(
                    """INSERT INTO tags (tag_id, name, slug) VALUES (%s, %s, %s)""",
                    (
                        tag["id"],
                        tag["name"],
                        tag["slug"],
                    ),
                )

                conn.commit()


if __name__ == "__main__":
    insert_tags()
