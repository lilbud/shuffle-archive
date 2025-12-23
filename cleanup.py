import datetime
import json
import re
import time
from pathlib import Path

import ftfy
import html_to_markdown
from bs4 import BeautifulSoup as bs4
from markdownify import markdownify as md

# title: title -> rendered
# author: author
# category: categories -> list?
# page content: content -> rendered
# tags: list of IDs
# header image: jetpack_featured_media_url (remove params after .jpg)
# published: date (%Y-%m-%dT%H:%M:%S)

cat_dict = dict(json.loads(Path("./categories_fixed.json").read_text()))
tag_dict = dict(json.loads(Path("./tags.json").read_text()))


def format_date(date: str) -> datetime.datetime:
    """Convert date string to datetime object."""
    return datetime.datetime.strptime(
        date,
        "%Y-%m-%dT%H:%M:%S",
    ).astimezone(
        datetime.timezone.utc,
    )


def format_categories(category_list: list[int]) -> list[dict]:
    """Create list of categories using list of IDs."""
    categories = []

    for item in category_list:
        res = cat_dict.get(str(item))

        categories.append(f"[{res['name']}]({res['url']})")

    return categories


def format_tags(tags_list: list[int]) -> list[dict]:
    """Create list of tags using list of IDs."""
    tags = []

    for item in tags_list:
        res = tag_dict.get(str(item))

        tags.append(f"[{res['name']}]({res['url']})")

    return tags


def format_article_content(orig_content: str) -> str:
    """Format article markup.

    The articles are formatted as HTML, which needs some fixes done before
    inserting into database. Various fixes related to missing/incorrect tags.
    This helps with markdown conversion later.
    """
    # multiple new line replace
    orig_content = re.sub("(\r?\n){2}", "<p></p>", orig_content)

    soup = bs4(orig_content, "lxml")

    # fix iframes having embed links instead of direct
    for iframe in soup.find_all("iframe"):
        src = iframe["src"]

        if src:
            if "youtube" in src:
                # Replace embedded video with direct link
                src = re.sub(
                    r"youtube.com\/embed\/(?!videoseries)",
                    "youtube.com/watch?v=",
                    src,
                )

                # Replace embedded playlist with direct link
                src = re.sub(
                    r"youtube.com\/embed\/videoseries",
                    "youtube.com/playlist",
                    src,
                )

                # Remove embed params
                src = re.sub(r"\?feature=oembed", "", src)
                src = re.sub(r"&feature=oembed", "", src)

            elif "videopress" in src:
                src = re.sub(r"\?hd.*", "", src)

        iframe["src"] = src

    for img in soup.find_all("img"):
        src = img["src"]

        if "i0.wp" in img["src"]:
            src = re.sub(r"i0.wp.com/|\?resize.*", "", img["src"])

        img["src"] = src

    return str(soup.body.decode_contents())
