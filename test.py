from pathlib import Path

from bs4 import BeautifulSoup as bs4

f = Path("./test.html").read_text()

soup = bs4(f, "lxml")

for i in soup.find_all("a"):
    print(i["href"])
