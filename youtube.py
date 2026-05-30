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

ydl_opts = {
    # Specify the runtime (e.g., 'deno', 'node', 'bun')
    "js_runtimes": {
        "deno": {"path": None},  # Set 'path' to a string if it's not in your PATH
    },
    "verbose": False,
    "sleep_interval": 5,
    "max_sleep_interval": 15,
    "sleep_requests": 2,
    "quiet": False,  # Suppresses standard output messages
    "no_warnings": False,  # Suppresses warning indicators
    "extract_flat": True,  # Extracts playlist metadata not videos
    "skip_download": True,
}

posts_dir = Path("./archive/posts")


def find_missing_youtube_titles(content: str, ydl: yt_dlp.YoutubeDL) -> None:
    """Find missing youtube titles."""
    for i in re.findall(
        r"\[Watch on Youtube: Watch Video\]\((https://www.youtube.com/watch\?v=.{11}|https://www.youtube.com/playlist\?list=.*)\)",
        content,
        flags=re.IGNORECASE,
    ):
        print(i)

        try:
            info_dict = ydl.extract_info(i, download=False)
            video_title = info_dict.get("title", None)
            print(video_title)

            old = f"[Watch on Youtube: Watch Video]({i})"
            new = f"[Watch on Youtube: {video_title}]({i})"
            content = content.replace(old, new)
            time.sleep(2)
        except DownloadError:
            time.sleep(2)
            continue

    return content


def get_meta(id: str, client: httpx.Client) -> dict:
    api_url = f"https://ytapi.apps.mattw.io/v3/videos?key=foo1&quotaUser=kliztQ2dPFm5380ysatNZFvRQVC8EZaLtY6c1Zny&part=snippet%2Cstatistics%2CrecordingDetails%2Cstatus%2CliveStreamingDetails%2Clocalizations%2CcontentDetails%2CpaidProductPlacementDetails%2Cplayer%2CtopicDetails&id={id}&_=1780165154120"

    response = client.get(api_url)

    if response.json().get("items"):
        return response.json()

    return None


if __name__ == "__main__":
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for post in posts_dir.glob("**/*.md"):
            print(post.parent.name)
            content = post.read_text(encoding="utf-8")

            if "[Watch on Youtube: Watch Video]" in content:
                content = find_missing_youtube_titles(content, ydl)

            post.write_text(content, encoding="utf-8")
            print("-" * 20)
