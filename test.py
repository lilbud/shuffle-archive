import glob
import json
import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup as bs4

# uncategorized
# kingdom-of-days
# roll-of-the-dice
# cover-me
# meeting-across-the-river
# where-the-band-was
# hearts-of-stone
# spare-parts

category = "spare-parts"

cmpath = Path(
    rf"C:\Users\bvw20\Documents\Personal\Projects\Bruce Stuff\Websites\e-street-shuffle\2025-11-30 - httrack\estreetshuffle\estreetshuffle.com\index.php\category\{category}",
)

titles = []

for file in cmpath.glob("**/*.html"):
    print(file.parent.name)

    if file.parent.name == "feed":
        continue

    with file.open("r", encoding="utf-8") as f:
        soup = bs4(f.read(), "html.parser")

        for item in soup.find_all("h1", {"class": "entry-title"}):
            title = item.text

            url = re.search(
                r"(/\d+/\d+/\d+/.*/)index.html",
                item.find_next("a")["href"],
            ).group(1)

            published = item.find_next("time", {"class": "published"})["datetime"]
            updated = item.find_next("time", {"class": "updated"})["datetime"]

            titles.append([title, url, published, updated])

df = pd.DataFrame(titles, columns=["title", "url", "published", "updated"])
df.to_csv(f"master_lists/{category}-titles.csv", index=False)
