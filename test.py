import datetime
import glob
import json
import re
import time
from pathlib import Path

import html_to_markdown
import httpx
import pandas as pd
from bs4 import BeautifulSoup as bs4
from user_agent import generate_user_agent

from cleanup import initial_cleanup
from database import load_db

# toedit = []

# cookies = {"wordpress_test_cookie": "WP Cookie check"}
headers = {
    "User-Agent": generate_user_agent(),
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    # "Connection": "keep-alive",
    # "Cookie": "wordpress_test_cookie=WP%20Cookie%20check",
    # "Upgrade-Insecure-Requests": "1",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "cross-site",
    # "Priority": "u=0, i",
}


# for file in Path("ia_json").glob("*.txt"):
#     data = json.loads(file.read_text(encoding="utf-8"))

#     timestamp = datetime.datetime.strptime(
#         data["modified_gmt"],
#         "%Y-%m-%dT%H:%M:%S",
#     ).timestamp()

#     with Path(f"ia_json/{data['id']}_{int(timestamp)}.json").open("w", encoding="utf-8") as f:
#         json.dump(data, f)

with load_db() as conn, conn.cursor() as cur:
    folder = Path(r"./archive/posts")

    for file in folder.glob("**/*.md"):
        print(file.parent.name)
        content = file.read_text(encoding="utf-8")
        content = re.sub(
            r"\?hd=1&amp;cover=1&amp;loop=0&amp;autoPlay=0&amp;permalink=1&amp;muted=0&amp;controls=1&amp;playsinline=0&amp;useAverageColor=0&amp;preloadContent=metadata",
            "",
            content,
            flags=re.MULTILINE,
        )

        file.write_text(content, encoding="utf-8")
