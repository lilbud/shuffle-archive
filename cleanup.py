import datetime
import json
import re
import time
from pathlib import Path

import ftfy
import html_to_markdown
from bs4 import BeautifulSoup as bs4

# from markdownify import markdownify as md


def format_date(date: str) -> datetime.datetime:
    """Convert date string to datetime object."""
    return datetime.datetime.strptime(
        date,
        "%Y-%m-%dT%H:%M:%S",
    ).astimezone(
        datetime.timezone.utc,
    )


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
                src = re.sub(r"(\?|&)feature=oembed", "", src)

            elif "videopress" in src:
                src = re.sub(r"\?hd.*", "", src)

        iframe["src"] = src

    for img in soup.find_all("img"):
        src = img["src"]

        if re.search(r"i\d.wp.com/", img["src"]):
            src = re.sub(r"i\d.wp.com/|\?resize.*", "", img["src"])

        img["src"] = src

    return str(soup.body.decode_contents())
