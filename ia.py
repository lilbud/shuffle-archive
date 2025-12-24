import os
import re
import time
from pathlib import Path

import ftfy
import httpx
import internetarchive as ia
import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()


def get_archive_session() -> ia.ArchiveSession:
    """Configure archive.org session."""
    if Path.exists(Path("config.ini")):
        print("Found custom config file")
        return ia.get_session(config_file=r".\\config.ini")

    print(
        r"no custom config found, using default stored at $HOME\.config\internetarchive\ia.ini (C:\Users\[USERNAME]\.config\internetarchive\ia.ini on Windows)",  # noqa: E501
    )

    return ia.get_session()


with httpx.Client() as client:
    url = "https://web.archive.org/web/timemap/json?url=https%3A%2F%2Festreetshuffle.com%2Findex.php%2Fwp-json%2Fwp%2Fv2%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=10000&_=1766502603892"

    res = client.get(url)

    print(res.json())
