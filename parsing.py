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
    """Format article markup into markdown.

    The articles are formatted as HTML, which is to be converted to markdown
    This function fixes encoding errors, as well as additional fixes using regex
    """
    options = html_to_markdown.ConversionOptions(preserve_tags={"p"})

    content = html_to_markdown.convert(orig_content)
    soup = bs4(orig_content, "lxml")

    content = "\n".join(line.strip() for line in content.splitlines())

    # https://i0.wp.com/estreetshuffle.com/wp-content/uploads/2020/11/1975-12-02.png?resize=768%2C1136&ssl=1

    regex_fixes = [
        [r"&#8211;", "–"],  # sometimes em dashes are not converted
        [
            r"(\s*\r?\n){2,}",
            "\r\n",
        ],  # replaces extraneous new lines, replaces groups of 2 or more with a single
        [r"(>\n){5}", ">\n"],  # fix blockquotes having a ton of empty quoted lines
        [r"\*\(", "* ("],  # fix no space between star and parenthesis
        [r"\)\*", ")* "],  # fix no space between closing star and parenthesis
        [r"\*\.\*", "."],  # replace *.* with ., unknown why this appears
        [
            r"i0.wp.com\/|\?resize=.*ssl=1",
            "",
        ],  # remove resize param from image tag
    ]

    youtube_urls = re.findall(
        r"\[https://www.youtube.com/embed/(.{11}).*\]\(.*\)",
        content,
    )

    if youtube_urls:
        for match in youtube_urls:
            try:
                youtube = soup.find("iframe", {"src": re.compile(match)})
                title = youtube["title"]
                url = f"https://www.youtube.com/watch?v={match}"

                content = re.sub(
                    r"\[https://www.youtube.com/embed/" + match + r".*\]\(.*\)",
                    f"[Youtube: {title}]({url})\n![]({url})",
                    content,
                )
            except KeyError:
                pass

    for pattern in regex_fixes:
        content = re.sub(pattern[0], pattern[1], content)

    return content


for post in Path("./posts").iterdir():
    print(post.name)

# for category in cat_dict:
#     slug = cat_dict[category]["slug"]
#     print(slug)

#     # create export folder for category
#     Path(f"./export/{slug}").mkdir(exist_ok=True)

#     for file in Path(f"./categories/{slug}").iterdir():
#         data = json.loads(file.read_text())

#         for article in data:
#             title = ftfy.fix_text(article["title"]["rendered"])
#             note = f"Originally Published on Ken Rosen's E Street Shuffle blog at {article['link']}"

#             # header image url, needs to be regexed to remove params and wordpress site prefix
#             header_img = re.sub(
#                 r"i0.wp.com\/|\?.*$",
#                 "",
#                 article["jetpack_featured_media_url"],
#             )
#             header_img_name = header_img.split("/")[-1]

#             categories = format_categories(article["categories"])
#             tags = format_tags(article["tags"])

#             publish_date = format_date(article["date"])
#             updated_date = format_date(article["modified"])

#             filename = f"{publish_date.strftime(f'%Y%m%d_{article["slug"]}')}"

#             content = format_article_content(article["content"]["rendered"])

#             with Path(f"./export/{slug}/{filename}.md").open(
#                 "w",
#                 encoding="utf-8",
#             ) as f:
#                 f.write(f"# {title}\n")
#                 f.write(f"#### {note}\n")
#                 f.write(f"#### Published: {publish_date.strftime('%B %d, %Y')}\n")
#                 f.write(f"#### Last Updated: {updated_date.strftime('%B %d, %Y')}\n")
#                 # f.write(f"#### Categories: {', '.join(categories)}\n")
#                 # f.write(f"#### Tags: {', '.join(tags)}\n")
#                 f.write(f"![{header_img_name}]({header_img})\n\n")
#                 f.write(f"{content.strip()}")
