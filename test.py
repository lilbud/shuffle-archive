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
from yt_dlp.utils import DownloadError

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
jekyll_dir = Path(
    r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_posts",
)
hugo_dir = Path(
    r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle-hugo\content\post",
)

files = [
    re.sub(r"\d{4}-\d{2}-\d{2}-", "", str(file.stem)) for file in hugo_dir.iterdir()
]

# for file in jekyll_dir.iterdir():
#     link_pattern = r"({% link _posts/([^\]]*).md %})"
#     content = file.read_text(encoding="utf-8")

#     for match in re.findall(link_pattern, content):
#         if not Path(jekyll_dir, match[1]).exists():
#             date = re.search(r"\d{4}-\d{2}-\d{2}", match[1])[0]
#             slug = re.search(r"\d{4}-\d{2}-\d{2}-(.*)", match[1])[1]

#             print(date, slug)


# for post in posts_dir.glob("**/*.md"):
#     # print(post.parent.name)
#     content = post.read_text(encoding="utf-8")

#     meta = json.loads(Path(post.parent, "meta.json").read_text(encoding="utf-8"))

#     if "[Watch on Youtube: Watch Video]" in content:
#         new_content = initial_cleanup(meta["content"]["rendered"])
#         new_content = html_to_markdown.convert(new_content)

#         post.write_text(new_content, encoding="utf-8")

#         print(f"Updated {post.parent.name}")


# with load_db() as conn, conn.cursor() as cur:
#     res = cur.execute(
#         """select * from posts where "slug" ilike 'kingdom%' AND "title" not ilike 'Kingdom of Days:%'""",
#     ).fetchall()

#     for post in res:
#         id = post["id"]
#         new_title = f"Kingdom of Days: {post['title']}"

#         cur.execute(
#             """update posts set "title" = %s where "id" = %s""", (new_title, id)
#         )
