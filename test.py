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
from convert import save_to_archive
from database import load_db

# toedit = []

# cookies = {"wordpress_test_cookie": "WP Cookie check"}
# headers = {
# "User-Agent": generate_user_agent(),
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
# }


# for file in Path("ia_json").glob("*.txt"):
#     data = json.loads(file.read_text(encoding="utf-8"))

#     timestamp = datetime.datetime.strptime(
#         data["modified_gmt"],
#         "%Y-%m-%dT%H:%M:%S",
#     ).timestamp()

#     with Path(f"ia_json/{data['id']}_{int(timestamp)}.json").open("w", encoding="utf-8") as f:
#         json.dump(data, f)

# with load_db() as conn, conn.cursor() as cur:
#     folder = Path(r".\archive\posts\2024-01-02_cover-me-fire")

#     data = Path(folder, "meta.json").read_text(encoding="utf-8")

#     data = json.loads(data)

#     content = initial_cleanup(data["content"]["rendered"])
#     content = html_to_markdown.convert(content)

#     Path(folder, "post.md").write_text(content, encoding="utf-8")


posts_dir = Path("./archive/posts")

linklist = []
with load_db() as conn, conn.cursor() as cur:
    for post in posts_dir.glob("**/*.md"):
        print(post.parent.name)
        content = post.read_text(encoding="utf-8")
        data = json.loads(Path(post.parent, "meta.json").read_text(encoding="utf-8"))

        last_modified = datetime.datetime.strptime(
            data["modified_gmt"],
            "%Y-%m-%dT%H:%M:%S",
        )

        res = cur.execute(
            """select * from all_posts where post_id = %(id)s and published = %(last_modified)s""",
            {"id": data["id"], "last_modified": last_modified},
        ).fetchone()

        title = res["title"].strip('"').replace('"', "'")

        with post.open("w", encoding="utf-8") as f:
            f.write("---\n")

            if res["header_img"]:
                f.write("layout: post\n")
            else:
                f.write("layout: default-post\n")

            f.write(f'title: "{res["title"]}"\n')
            f.write(f'author: "{res["author"]}"\n')
            f.write(f'excerpt: "{res["excerpt"].strip()}"\n')

            if res["tag_list"]:
                f.write(f"tags: {res['tag_list']}\n")

            if res["category_list"]:
                f.write(f"categories: {res['category_list']}\n")

            if res["header_img"]:
                f.write(f"header_img: {res['header_img']}\n")

            f.write(f"post_id: {res['post_id']}\n")

            f.write("---\n")
            f.write(content)
