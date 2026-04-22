import json
from pathlib import Path

from main import get_client


def get_categories() -> None:
    """Get all categories using WP REST API."""
    with get_client() as client:
        url = "https://estreetshuffle.com/index.php/wp-json/wp/v2/categories?per_page=100&page=1"

        res = client.get(url)

        with Path("categories.json").open("w") as f:
            json.dump(res.json(), f)
