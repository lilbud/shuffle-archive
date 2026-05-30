import json
import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from main import get_client


def load_db() -> psycopg.Connection:
    """Load DB and return connection."""
    return psycopg.connect(
        conninfo=os.getenv("DATABASE_URL"),
        row_factory=dict_row,
    )


def get_categories() -> None:
    """Get all categories using WP REST API."""
    with get_client() as client:
        url = "https://estreetshuffle.com/index.php/wp-json/wp/v2/categories?per_page=100&page=1"

        res = client.get(url)

        with load_db() as conn, conn.cursor() as cur:
            for cat in res.json():
                cur.execute(
                    """INSERT INTO categories (id, name, slug) VALUES (%s, %s, %s) on conflict (id, name) do nothing""",
                    (
                        cat["id"],
                        cat["name"],
                        cat["slug"],
                    ),
                )

                conn.commit()

        json.dump(res.json(), Path("categories_20260530.json").open("w"))


if __name__ == "__main__":
    get_categories()
