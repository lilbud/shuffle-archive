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
        # print(post.parent.name)
        content = post.read_text(encoding="utf-8")

        # for old, new in links_list:
        #     content = content.replace(old, new)

        # post.write_text(content, encoding="utf-8")

        link_pattern = r"\[([^\)]*)\]\(([^\)]*)/\)"

        links = re.findall(link_pattern, content)

        if len(links) > 0:
            for url_text, url in links:
                if (
                    url
                    and "estreetshuffle" in url
                    and "roll-of-the-dice-album-by-album" not in url
                    and "category" not in url
                    and "tag" not in url
                    and "bookshelf" not in url
                ):
                    date = (
                        re.search(r"(\d{4}\/\d{2}\/\d{2})", url)
                        .group(0)
                        .replace("/", "-")
                    )
                    slug = (
                        re.search(r"\d{4}\/\d{2}\/\d{2}/(.*)/?", url)
                        .group(1)
                        .strip("/")
                    )

                    filename = f"{date}_{slug}"

                    print(url)

                    # if not Path(f"./archive/posts/{filename}").exists():
                    #     print(filename)
                    # content = content.replace(url, f"../{filename}/post.md")
        #                 res = cur.execute(
        #                     """select url, filename from published_posts where slug = %(slug)s""",
        #                     {"slug": slug},
        #                 ).fetchone()

        #                 if res:
        #                     content = content.replace(
        #                         url,
        #                         f"../{res['filename']}/post.md",
        #                     )

        # post.write_text(content, encoding="utf-8")
