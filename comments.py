import datetime
import json
import re
from pathlib import Path

import ftfy
import markdown
import unidecode
from bs4 import BeautifulSoup as bs4
from html_to_markdown import convert

from database import load_db
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

    with Path("comments_new_1.json").open("w") as f:
        json.dump(comments, f)


new_comments = {}
author_img = []

avatar_list = (
    Path(r"C:\Users\bvw20\Downloads\avatars\default\list.txt").read_text().split("\n")
)


def comments_format():
    """Format comments file, remove unneeded fields."""
    comments = json.loads(Path("comments_merged.json").read_text())

    # fields needed: id, post, author_name, date_gmt, content['rendered'], author_avatar_urls['96']
    # author_avatar_urls can have the 's' param changed to 9999 for max res
    # also change to a single default url if needed

    for comment in comments:
        id = comment["id"]
        post = comment["post"]
        author_name = unidecode.unidecode(comment["author_name"])
        date_gmt = comment["date_gmt"]

        parent = None

        if comment["parent"] != 0:
            parent = comment["parent"]

        content = convert(comment["content"]["rendered"])
        content = unidecode.unidecode(content)

        author_avatar_urls = comment["author_avatar_urls"]["96"]

        avatar_id = re.search(
            r"https://secure.gravatar.com/avatar/(.*)\?s=96&d=mm&r=g",
            author_avatar_urls,
        )[1]
        avatar_url = re.sub(
            r"https://secure.gravatar.com/avatar/(.*)\?s=96&d=mm&r=g",
            "/assets/img/avatars/\\1.jpg",
            author_avatar_urls,
        )

        if avatar_id in avatar_list:
            avatar_url = "/assets/img/avatars/default.jpg"

        new_comment = {
            "id": id,
            "parent": parent,
            "author_name": author_name,
            "date_gmt": date_gmt,
            "content": content,
            "author_avatar_url": avatar_url,
        }

        try:
            new_comments[f"{post}"].append(new_comment)
        except KeyError:
            new_comments[f"{post}"] = []
            new_comments[f"{post}"].append(new_comment)

    # comments_sorted = sorted(new_comments, key=lambda x: (x['name'], x['age']))

    for c in new_comments:
        new_comments[c] = sorted(new_comments[c], key=lambda x: x["date_gmt"])

    with Path("comments_new_2.json").open("w") as f:
        json.dump(new_comments, f)


# comments_format()


# comments = json.load(Path(r"C:\Users\bvw20\Documents\Personal\Projects\Bruce Stuff\Websites\e-street-shuffle\shuffle-archive\comments_merged.json").open("r"))


# # id, post, author_name, date_gmt, content.rendered
# with load_db() as conn, conn.cursor() as cur:
#     for c in comments:

#         author_name = c["author_name"]

#         author = cur.execute("""
#             SELECT id FROM authors
#             WHERE name = %s""", (author_name,)).fetchone()

#         comment_id = c['id']

#         content = convert(c["content"]["rendered"])
#         content = unidecode.unidecode(content)
#         parent = None
#         reply = False

#         if c['parent'] != 0:
#             parent = c['parent']
#             reply = True

#         published = datetime.datetime.strptime(c['date_gmt'], "%Y-%m-%dT%H:%M:%S")

#         cur.execute("""
#             INSERT INTO comments (comment_id, author_id, post_id, text, parent, published, is_reply)
#             VALUES (%s, %s, %s, %s, %s, %s, %s) on conflict (comment_id) do nothing""", (c['id'], author['id'], c["post"], content, parent, published, reply))

comments = json.loads(
    Path(
        r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_data\new_comments.json",
    ).read_text(),
)

for c in comments:
    img = c["avatar_thumb"].replace("/", "\\")

    if not Path(
        rf"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\{img}",
    ).exists():
        c["avatar_thumb"] = "/assets/img/avatars/default.jpg"

with Path(
    r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_data\new_comments_1.json",
).open("w") as f:
    json.dump(comments, f)
