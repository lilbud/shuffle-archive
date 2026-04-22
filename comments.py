import datetime
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup as bs4

from main import get_client


def get_comments():
    comments = []

    with get_client() as client:
        for i in range(1, 23):
            print(i)
            res = client.get(
                f"https://estreetshuffle.com/index.php/wp-json/wp/v2/comments?per_page=100&page={i}",
            )

            if res:
                for comment in res.json():
                    comments.append(comment)  # noqa: PERF402

    with Path("comments_new.json").open("w") as f:
        json.dump(comments, f)
