import json
import re
from pathlib import Path

import ftfy
import html_to_markdown
import httpx
import tidy
from bs4 import BeautifulSoup as bs4

from cleanup import format_article_content
from database import insert_post, load_db

posts = Path(r".\archive\posts")

tags = []

if __name__ == "__main__":
    with load_db() as conn, conn.cursor() as cur:
        res = cur.execute("""SELECT id, excerpt FROM posts""").fetchall()

        for i in res:
            print(i["id"])
            ex = ftfy.fix_text(html_to_markdown.convert(i["excerpt"]))

            cur.execute(
                """UPDATE posts SET excerpt = %s WHERE id = %s""",
                (ex, i["id"]),
            )
