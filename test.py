import json
import re
import traceback
from pathlib import Path

import ftfy
import html_to_markdown
import httpx
import markdown
import regex
import se
import slugify
import tidy
from bs4 import BeautifulSoup as bs4
from bs4 import Comment
from minify_html import minify
from se import formatting
from se.se_epub import SeEpub
import datetime
from cleanup import initial_cleanup, link_fixes
from database import insert_post, load_db

posts = Path(r".\archive\posts")
json_posts = Path(r".\posts_json")

tags = []

template = Path("./template.html")
soup = bs4(template.read_text(), "html.parser")


# se_epub = SeEpub(r".\books\spare-parts\lilbud_e-street-shuffle-spare-parts")


# print(se_epub)

# print(se_epub.generate_toc())


if __name__ == "__main__":
    with load_db() as conn, conn.cursor() as cur:
        for file in json_posts.iterdir():
            post = json.loads(file.read_text(encoding="utf-8"))

            post_id = post['id']

            date = datetime.datetime.strptime(
                post["modified_gmt"],
                "%Y-%m-%dT%H:%M:%S",
            )

            save_path = Path(f"./archive/posts/{date.date()}_{post['slug']}")

            print(save_path)
            save_path.mkdir(exist_ok=True)

            content = initial_cleanup(post["content"]['rendered'])
            content = html_to_markdown.convert(content)

            # if not Path(save_path, "meta.json").exists():
            #     # save the updated dict to the post folder
            #     with Path(save_path, "meta.json").open("w", encoding="utf-8") as f:
            #         json.dump(post, f)

            #     print("created json")

            # # write post HTML from database to post folder
            # if not Path(save_path, "post.html").exists():
            #     with Path(save_path, "post.html").open("w", encoding="utf-8") as f:
            #         f.write(str(template))

            #     print("created html")

            # convert post to markdown and save
            if not Path(save_path, "post.md").exists():
                with Path(save_path, "post.md").open("w", encoding="utf-8") as f:
                    f.write(content)

                print("created md")



        # if not Path(f"./archive/posts/{date}_{post['slug']}").exists():
        #     print(f"./archive/posts/{date}_{post['slug']}")
        #     insert_post(post, cur, conn)

        # Path(f"./archive/posts/{date}_{post['slug']}").mkdir(exist_ok=True)




    # with load_db() as conn, conn.cursor() as cur:
    #     soup.title.string = "E Street Shuffle: Spare Parts"

    #     meta_description_tag = soup.find("meta", attrs={"name": "description"})

    #     if meta_description_tag:
    #         meta_description_tag["content"] = (
    #             "Posts from the E Street Shuffle 'Spare Parts' category."
    #         )

    #     body = soup.find("body")

    #     posts = [
    #         "37fb361f-23aa-4134-85c1-795590c7565f",
    #         "1641f8ad-4fdf-44bd-a2db-ef14f2412f10",
    #         "8a5f08fe-6c61-4827-b888-4590011fa934",
    #         "dac32ee4-d995-4e5a-919e-d00aac5c2a60",
    #         "6867ca83-44ac-4367-aad4-a85287682cdd",
    #         "02041313-a0fc-4bc9-b24b-571dfcad1370",
    #         "8bcb5913-e612-4e35-958e-a10868c64e12",
    #         "fe4f92e7-4696-41b4-bc2a-a119ce590235",
    #         "a4cbd165-9241-4fb6-a0ef-612e316236c1",
    #         "76c42a6b-0b47-4867-9d7e-9b786bc9da85",
    #         "83b2026d-5c31-4c51-9e2b-45d5c4b86e3c",
    #         "9a2ed144-e7cb-4f52-9ad5-f2d41b0095ed",
    #         "dd22b312-d29e-447a-94fa-619aac082438",
    #         "cfc8fdea-e18f-42a1-b494-02bb9a14dea3",
    #         "8acceda3-de65-4d9c-9482-fc546abfb565",
    #         "c55d8aa2-16ac-4727-9172-dc6241d5f93d",
    #         "7e9a0814-3608-4594-b2e1-b8cd8009d2a9",
    #         "d66b8a7d-c54a-4faa-805e-1ec25e521403",
    #         "d45f9ee7-5eb9-4a70-a471-98c251b8d89f",
    #     ]

    #     for post in posts:
    #         res = cur.execute(
    #             """SELECT * from posts where id = %s""",
    #             (post,),
    #         ).fetchone()

    #         html = Path(
    #             f"./archive/posts/{res['published'].date()}_{res['slug']}/post.html",
    #         )

    #         if html:
    #             print(html)

    #             content = html.read_text(encoding="utf-8")
    #             content = initial_cleanup(content)

    #             content = bs4(content, "html.parser")

    #             post_title = soup.new_tag("h2")
    #             post_title.string = res["title"]
    #             post_title["epub:type"] = "title"

    #             # if "Cheap Motel" in res['title']:
    #             #     print(content.find('body'))

    #             post_published = soup.new_tag("span")

    #             post_published.string = (
    #                 f"Originally Published: {res['published'].strftime('%B %d, %Y')}"
    #             )

    #             soup.body.append(Comment("se:split"))
    #             soup.body.append(post_title)
    #             soup.body.append(post_published)
    #             soup.body.append(content.find('body'))


            
    #     with Path(
    #         r".\books\\spare-parts\\lilbud_e-street-shuffle-spare-parts\\src\\epub\text\body.xhtml",
    #     ).open("w", encoding="utf-8") as f:
    #         content = str(soup.find("body"))

    #         content = re.sub("(\r?\n){2,}", "\n", content)
    #         content = re.sub("</?body>", "", content)

    #         f.write(content)
