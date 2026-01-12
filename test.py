import re
from pathlib import Path

from bs4 import BeautifulSoup as bs4

from database import insert_post, load_db

f = Path("./test.html").read_text(encoding="utf-8")

soup = bs4(f, "lxml")
songs = [
    "Clouds",
    "Crystal",
    "Death of a Good Man",
    "The Fire Engines Are Returning Home",
    "For Never Asking",
    "Love Cycle",
    "Mississippi",
    "New York Morning Love",
    "Oh No No No",
    "Phantom Love (Just 16)",
    "Slum Sentiments",
    "Sun Time",
    "Turn Around",
    "Until the Rain Comes",
    "Upon This Day (Eurydice)",
    "Vaginal Vandals",
    "The Virgin Flower",
    "The War Song",
    "The Window",
    "A Winter's Revelation (In 9 Illusions)",
]

with load_db() as conn, conn.cursor() as cur:
    for s in songs:
        res = cur.execute(
            """select distinct p.id, p.post_id, p.title, p.published, p.last_modified from posts p left join post_categories pc ON pc.post_id = p.id where LOWER(p.title) LIKE %s""",
            (f"%{s.lower()}%",),
        ).fetchone()

        if res:
            res["title"] = re.sub("^Roll of the Dice: ", "", res["title"])
            print("|".join(str(res[i]) for i in res))
