import datetime
import json
import os
from pathlib import Path
import re

import ftfy
import html_to_markdown
import psycopg
from bs4 import BeautifulSoup as bs4
from dotenv import load_dotenv
from psycopg.rows import dict_row

from cleanup import initial_cleanup
from database import load_db

post_folder = Path("./archive/posts/")
json_folder = Path("./posts_json/")

# for file in json_folder.iterdir():
#     data = json.loads(file.read_text(encoding="utf-8"))
#     print(data['slug'])

#     published = datetime.datetime.strptime(
#         data["date_gmt"],
#         "%Y-%m-%dT%H:%M:%S",
#     )

#     last_modified = datetime.datetime.strptime(
#         data["modified_gmt"],
#         "%Y-%m-%dT%H:%M:%S",
#     )

#     date = published.date()
#     last_modified_ts = int(last_modified.timestamp())

#     save_path = Path(f"./archive/posts/{date}_{data['slug']}")
#     save_path.mkdir(exist_ok=True)

#     if not Path(save_path, "meta.json").exists():
#         # save the updated dict to the post folder
#         with Path(save_path, "meta.json").open("w", encoding="utf-8") as f:
#             json.dump(data, f)

#         print(f"created meta.json for {data['slug']}")

#     # convert post to markdown and save
#     if not Path(save_path, "post.md").exists():
#         with Path(save_path, "post.md").open("w", encoding="utf-8") as f:
#             f.write(html_to_markdown.convert(data['content']['rendered']))

#         print(f"created post.md for {data['slug']}")
    
#     print("--" * 20)

for post in post_folder.iterdir():
    print(post.name)
    if post.is_dir():
        post_path = Path(post, "post.md")

        post_text = post_path.read_text(encoding="utf-8")

        bold_fixed = re.sub(r"^\*{2}([^*]+?)\s*$", r"**\1**", post_text, flags=re.MULTILINE)
        trimmed = re.sub(r"\s+$", r"", bold_fixed)

        with Path(post, "post.md").open("w", encoding="utf-8") as f:
            f.write(trimmed)
        