import json
import re
import shutil
from pathlib import Path

import pandas as pd
import psycopg

from database import load_db


def get_posts(
    cur: psycopg.Cursor,
) -> list | None:
    res = cur.execute(
        """
        select * from published_posts
        """,
    ).fetchall()

    if res:
        return res

    return None


def replace_links(content: str):
    content = re.sub(
        r"../(\d{4}-\d{2}-\d{2})_([^/]*)/post.md",
        r'{{< relref "\1-\2.md" >}}',
        content,
    )

    content = re.sub(
        "https?://estreetshuffle.com/index.php/roll-of-the-dice-album-by-album/",
        "/roll-of-the-dice-album-by-album/",
        content,
    )

    content = re.sub(
        "https?://estreetshuffle.com/index.php/category/",
        "/categories/",
        content,
    )

    content = re.sub(
        "https?://estreetshuffle.com/index.php/tag/",
        "/tags/",
        content,
    )

    return content


def replace_audio(content: str) -> str:
    audio_pattern = r"(\[(.*.(mp3|flac|wav|m4a))\]\(.*.(mp3|flac|wav|m4a)\))"

    content = re.sub(
        audio_pattern,
        r'\1\n{{< audio url="\2" >}}',
        content,
        flags=re.IGNORECASE,
    )

    return content


def replace_video(content: str) -> str:
    """Append video iframe include under video link."""
    videopress_pattern = (
        r"(\[Watch Video Highlight\]\(https://videopress.com/embed/(.*)\??.*\))"
    )
    youtube_pattern = (
        r"(\[Watch on youtube.*\]\(https://www.youtube.com/watch\?v=([^\?\(\)]*).*\))"
    )
    youtube_playlist_pattern = (
        r"(\[Watch on youtube.*\]\(https://www.youtube.com/playlist\?list=(.*)\))"
    )
    vimeo_pattern = r"(\[[^\[\]]*\]\(https://player.vimeo.com/video/([^\?]*)\?.*\))"

    content = re.sub(
        videopress_pattern,
        r"{{< videopress id=\2 >}}",
        content,
        flags=re.IGNORECASE,
    )

    content = re.sub(
        youtube_pattern,
        r"{{< youtube \2 >}}",
        content,
        flags=re.IGNORECASE,
    )

    content = re.sub(
        youtube_playlist_pattern,
        r"{{< youtube-playlist \2 >}}",
        content,
        flags=re.IGNORECASE,
    )

    content = re.sub(
        vimeo_pattern,
        r"{{< vimeo \2 >}}",
        content,
        flags=re.IGNORECASE,
    )

    return content


def main(cur: psycopg.Cursor) -> None:
    res = get_posts(cur)

    if res:
        for post in res:
            print(post["filename"])

            title = post["title"].strip('"').replace('"', "'")

            post_file = Path(
                rf"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle-hugo\content\post\{post['published'].strftime('%Y-%m-%d')}-{post['slug']}.md",
            )

            content = replace_links(post["content"])
            content = replace_video(content)
            content = replace_audio(content)

            with post_file.open("w", encoding="utf-8") as f:
                f.write("---\n")

                f.write("aliases:\n")
                f.write(f"- /{post['slug']}/\n")
                f.write(f"- /{post['post_id']}/\n")

                if post["header_img"]:
                    f.write("layout: post\n")
                else:
                    f.write("layout: default-post\n")

                f.write(f"date: {post['published'].strftime('%Y-%m-%dT%H:%M:%S')}\n")
                f.write(
                    f"lastmod: {post['last_modified'].strftime('%Y-%m-%dT%H:%M:%S')}\n",
                )
                f.write(f'title: "{title}"\n')
                f.write(f"slug: {post['slug']}\n")
                f.write(f"author: {post['author_name']}\n")
                f.write(f'description: "{post["excerpt"].strip()}"\n')

                if post["tag_slug_list"]:
                    tags = [
                        tag.replace('"', r"\"").strip(".")
                        for tag in post["tag_slug_list"].split(",")
                    ]

                    f.write("tags:\n")
                    for tag in tags:
                        f.write(f'- "{tag}"\n')

                if post["category_slug_list"]:
                    categories = [
                        category.replace('"', r"\"").strip(".")
                        for category in post["category_slug_list"].split(",")
                    ]

                    f.write("categories:\n")
                    for category in categories:
                        f.write(f'- "{category}"\n')

                f.write("params:\n")

                if post["header_img"]:
                    f.write(
                        f"  header_img: {post['header_img'].replace('.jpg', '.jpg.webp').replace('.png', '.png.webp').replace('.jpeg', '.jpeg.webp')}\n",
                    )

                f.write(f"  post_id: {post['post_id']}\n")

                f.write("---\n")
                f.write(content)


if __name__ == "__main__":
    ids = []
    with load_db() as conn, conn.cursor() as cur:
        main(cur=cur)
