import datetime
import glob
import json
import re
import time
from pathlib import Path

import html_to_markdown
import httpx
import pandas as pd
import yt_dlp
from bs4 import BeautifulSoup as bs4
from user_agent import generate_user_agent

from cleanup import initial_cleanup
from convert import save_to_archive
from database import load_db

ydl_opts = {
    # Specify the runtime (e.g., 'deno', 'node', 'bun')
    "js_runtimes": {
        "deno": {"path": None},  # Set 'path' to a string if it's not in your PATH
    },
    "verbose": False,
}

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
jekyll_dir = Path(
    r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_posts",
)

# for file in jekyll_dir.iterdir():
#     link_pattern = r"({% link _posts/([^\]]*).md %})"
#     content = file.read_text(encoding="utf-8")

#     for match in re.findall(link_pattern, content):
#         if not Path(jekyll_dir, match[1]).exists():
#             date = re.search(r"\d{4}-\d{2}-\d{2}", match[1])[0]
#             slug = re.search(r"\d{4}-\d{2}-\d{2}-(.*)", match[1])[1]

#             print(date, slug)


with load_db() as conn, conn.cursor() as cur:  # noqa: SIM117
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for post in posts_dir.glob("**/*.md"):
            print(post.parent.name)
            content = post.read_text(encoding="utf-8")

            for i in re.findall(
                r"\[Watch on Youtube: Watch Video\]\((https://www.youtube.com/watch\?v=.{11})\)",
                content,
                flags=re.MULTILINE,
            ):
                info_dict = ydl.extract_info(i, download=False)
                video_title = info_dict.get("title", None)
                print(i)

                re.sub(
                    rf"\[Watch on Youtube: Watch Video\]\({i}\)",
                    f"[Watch on Youtube: {video_title}]({i})",
                    content,
                )

        # post.write_text(content, encoding="utf-8")

# test_url = "https://www.youtube.com/watch?v=7-AMJV5EDRI"


# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info_dict = ydl.extract_info(test_url, download=False)
#     video_title = info_dict.get("title", None)

# print(f"Video Title: {video_title}")
