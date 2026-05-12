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

# toedit = []

# cookies = {"wordpress_test_cookie": "WP Cookie check"}
# headers = {
#     "User-Agent": generate_user_agent(),
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Connection": "keep-alive",
#     "Cookie": "wordpress_test_cookie=WP%20Cookie%20check",
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "cross-site",
#     "Priority": "u=0, i",
# }

# with httpx.Client(headers=headers, cookies=cookies, timeout=180) as client:
#     for file in Path("./archive/posts").glob("**/*.md"):
#         text = file.read_text(encoding="utf-8")

#         if file.parent.name == "2023-01-01_roll-of-the-dice-tucson-train":
#             # print(file.parent.name)
#             data = json.loads(
#                 Path(file.parent, "meta.json").read_text(encoding="utf-8"),
#             )
#             url = data["_links"]["self"][0]["href"]
#             print(file.parent.name)

#             content = initial_cleanup(data["content"]["rendered"])
#             content = html_to_markdown.convert(content)

#             with Path(file.parent, "post.md").open("w", encoding="utf-8") as f:
#                 f.write(content)

with Path(r".\archive\posts\1983-01-12_roll-of-the-dice-my-hometown\post.md") as f:
    text = f.read_text(encoding="utf-8")

    pattern = r"(^\*[^*]+\*(?:\n\*[^*]+\*)+)"
    result = re.sub(
        pattern,
        lambda m: re.sub(r"(?m)^", "> ", m.group(1)),
        text,
        flags=re.MULTILINE,
    )

    print(result)
    print()
