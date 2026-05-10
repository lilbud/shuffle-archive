import json
from pathlib import Path
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

def get_categories() -> None:
    """Get all categories using WP REST API."""
    with get_client() as client:
        url = "https://estreetshuffle.com/index.php/wp-json/wp/v2/categories?per_page=100&page=1"

        res = client.get(url)

        with Path("categories.json").open("w") as f:
            json.dump(res.json(), f)

def insert_categories() -> None:
    """Insert categories into database."""
    with load_db() as conn, conn.cursor() as cur:
        with Path("categories.json").open("r") as f:
            categories = json.load(f)

            for cat in categories:
                cur.execute(
                    """INSERT INTO categories (category_id, name, slug) VALUES (%s, %s, %s) on conflict (category_id, name) do nothing""",
                    (
                        cat["id"],
                        cat["name"],
                        cat["slug"],
                    ),
                )

                conn.commit()

if __name__ == "__main__":
    insert_categories()