import json
import re
from pathlib import Path

import html_to_markdown
import httpx
import tidy
from bs4 import BeautifulSoup as bs4

from cleanup import clean_file
from database import insert_post, load_db

# f = Path(r".\archive\posts\2025-01-01_kingdom-of-days-january-1\post.html")

# soup = bs4(f.read_text(encoding="utf-8"), "lxml")

tags = []

if __name__ == "__main__":
    print()
