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

link_list = Path("./links.txt").open("w", encoding="utf-8")

for post in posts_dir.glob("**/*.md"):
    content = post.read_text(encoding="utf-8")

    link_pattern = r"\[([^\)]*)\]\(([^\)/]*)/\)"

    links = re.findall(link_pattern, content)

    if len(links) > 0:
        print(post.parent.name)
        # link_list.write(f"{post.parent.name}:\n")
        for url_text, url in links:
            if "estreetshuffle" in url and "roll-of-the-dice-album-by-album" not in url:
                slug = f"{'-'.join(url.split('/')[-4:-1])}_{url.split('/')[-1]}"
                # print(slug)

                exists = False

                if Path(f"./archive/posts/{slug}").exists():
                    exists = True
                    content = content.replace(url, f"../{slug}/post.md")

                # print(url_text, url)
        #         link_list.write(f"\t{url} -> {exists}\n")

        # link_list.write("\n")

        post.write_text(content, encoding="utf-8")
