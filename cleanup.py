import datetime
import json
import re
import time
from pathlib import Path

import ftfy
import html_to_markdown
from bs4 import BeautifulSoup as bs4


def format_date(date: str) -> datetime.datetime:
    """Convert date string to datetime object."""
    return datetime.datetime.strptime(
        date,
        "%Y-%m-%dT%H:%M:%S",
    ).astimezone(
        datetime.timezone.utc,
    )


def link_fixes(soup: bs4) -> bs4:
    for link in soup.find_all("a"):
        if "estreetshuffle" in link["href"]:
            text = ftfy.fix_text(link.get_text())

            print(text)


def video_fixes(soup: bs4) -> bs4:
    """Fix for video iframe elements."""
    for iframe in soup.find_all("iframe"):
        src = iframe.get("src")
        title = iframe.get("title", "Watch Video")

        if iframe.has_attr("allowfullscreen"):
            iframe["allowfullscreen"] = ""  # Correct HTML5 boolean format

        # Youtube
        if "youtube.com" in src:
            title = f"Watch on Youtube: {title}"
            if "/embed/" in src:
                video_id = src.split("/")[-1].split("?")[0]
                link_url = f"https://www.youtube.com/watch?v={video_id}"
            else:
                link_url = src

        # VideoPress
        elif "videopress.com" in src:
            link_url = src
            if title == "VideoPress Video Player":
                title = "Watch Video Highlight"

        else:
            link_url = src

        link_container = soup.new_tag("p")

        # Create the Markdown-style link as a new paragraph
        md_link = soup.new_tag("a")
        md_link.string = title

        md_link["href"] = link_url

        link_container.append(md_link)

        # Replace the iframe's parent container (the div) if it exists
        # Clean up the container (WordPress often wraps these in specific divs)
        container = iframe.find_parent(
            "div",
            class_=["jetpack-video-wrapper", "video-player"],
        )

        if container:
            container.replace_with(link_container)
        else:
            iframe.replace_with(link_container)

    return soup


def initial_cleanup(orig_content: str) -> str:
    """HTML cleaning.

    Apply a few fixes for missing tags, replace some links.
    """
    # multiple new line replace
    orig_content = re.sub("(\r?\n){2,}", "", orig_content)

    # Replace <p> tag with space with closed tag.
    orig_content = re.sub(r"<p>\s+</p>", "<p></p>", orig_content)

    # replace empty line
    orig_content = re.sub(r"^$", "", orig_content)

    # add break after H element
    orig_content = re.sub(r"(</h\d>)", r"\1\n", orig_content)

    # replace http with https
    orig_content = re.sub("http:", "https:", orig_content)

    soup = bs4(orig_content, "lxml")

    # fix iframes having embed links instead of direct
    soup = video_fixes(soup)

    # image fixes
    for img in soup.find_all("img"):
        # remove wordpress CDN from images, change to direct link
        if img.get("data-orig-file"):
            img["src"] = re.sub(r"i\d.wp.com/|\?.*", "", img["data-orig-file"])
        else:
            img["src"] = re.sub(r"i\d.wp.com/|\?.*", "", img["src"])

        # assign uploaded image id to item id attribute
        if img.get("data-attachment-id"):
            img["id"] = f"image-{img.get('data-attachment-id')}"

        # remove id if empty
        if img.get("id") == "":
            del img.attrs["id"]

        # assign height and width if either is missing
        if not img.get("height"):
            img["height"] = "auto"

        if not img.get("width"):
            img["width"] = "auto"

        # remove wordpress data attributes
        attrs_to_del = [attr for attr in img.attrs if attr.startswith("data-")]
        for attr in attrs_to_del:
            del img[attr]

        # extra unneeded attributes
        extra_attrs = ["srcset", "sizes", "class", "loading", "decoding"]
        for attr in extra_attrs:
            del img[attr]

    for element in soup.find_all(recursive=True):
        if element.get("id") == "":
            del element.attrs["id"]

    return str(soup)
