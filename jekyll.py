import json
import re
import shutil
from pathlib import Path

import pandas as pd
import psycopg

from database import load_db


def copy_media(cur: psycopg.Cursor):
    img_dir = Path(
        r"C:\Users\bvw20\Documents\Personal\Projects\Bruce Stuff\Websites\e-street-shuffle\shuffle-archive\downloads",
    )

    res = cur.execute(
        """select id, url from media where id in (select featured_media from posts) and url is not null""",
    )

    if res:
        for img in res:
            img_path = "/".join(img["url"].split("/")[-3:-1])
            filename = img["url"].split("/")[-1]

            if Path(img_dir, img_path, filename).exists():
                old_path = Path(img_dir, img_path, filename)

                new_path = Path(
                    r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\assets\img\uploads",
                    img_path,
                    filename,
                )

                Path(new_path).parent.mkdir(exist_ok=True, parents=True)
                if not new_path.exists():
                    print(old_path)
                    print(new_path)
                    print("----")

                    shutil.copy(old_path, new_path)
                else:
                    print(f"{new_path} already exists")


def originals_data(cur: psycopg.Cursor) -> None:
    data = json.load(Path("data.json").open("r", encoding="utf-8"))

    with Path(
        r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_data\originals_1.yml",
    ).open(
        "w",
        encoding="utf-8",
    ) as f:
        for album in data:
            album_name = album["name"]

            album_img = album.get("image", None)

            songs = album["songs"]

            f.write(f"- name: {album_name}\n")

            if album_img:
                f.write(f"  img: {album_img}\n")

            f.write("  songs:\n")

            for song in songs:
                if song["url"]:
                    slug = song["url"].split("/")[-2]

                    res = cur.execute(
                        """
                        select
                            p.published::date as date,
                            p.published::date || '-' || slugify(p.title) as filename,
                            p.slug as slug
                        from posts p
                        where p.slug = %(slug)s
                        """,
                        {"slug": slug},
                    ).fetchone()

                    if res:
                        date = str(res["date"]).replace("-", "/")
                        url = f"{date}/{res['slug']}/"

                        f.write(f"    - name: {song['text']}\n")
                        f.write(f"      url: {url}\n")
                else:
                    f.write(f"    - name: {song['text']}\n")
                    f.write("      url: \n")

            f.write("\n")


def covers_data(cur) -> None:
    data = json.load(Path("data-covers.json").open("r", encoding="utf-8"))

    with Path(
        r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_data\covers.yml",
    ).open("w", encoding="utf-8") as f:
        for item in data:
            url = item["url"].replace("https://estreetshuffle.com/index.php/", "")

            f.write(f"- name: {item['name']}\n")
            f.write(f"  url: {url}\n")
            f.write("  songs:\n")

            for song in item["links"]:
                res = cur.execute(
                    """
                    select
                        p.published::date as date,
                        p.published::date || '-' || p.slug as filename,
                        p.slug as slug
                    from posts p
                    where p.slug = %(slug)s
                    -- and p.published > '2018-01-05'
                    """,
                    {"url": song["url"], "slug": song["url"].split("/")[-2]},
                ).fetchone()

                if res:
                    date = str(res["date"]).replace("-", "/")
                    url = f"{date}/{res['slug']}/"

                    f.write(f"    - name: {song['name']}\n")
                    f.write(f"      url: {url}\n")

            f.write("\n")


# def export_covers(cur) -> None:


def replace_with_internal(cur: psycopg.Cursor) -> None:
    post_dir = Path(
        r"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_posts",
    )

    for file in post_dir.iterdir():
        print(file.stem)
        text = file.read_text(encoding="utf-8")

        link_pattern = r"\[([^\]]+)\]\(([^\)]+)\)"

        links = re.findall(link_pattern, text)

        for url_text, url in links:
            if re.search(r"https://estreetshuffle.com/index.php/\d+/\d+/\d+/", url):
                new_url = re.search(r"(/\d+/\d+/\d+/.*)/", url)
                slug = re.search(r"/\d+/\d+/\d+/(.*)/", url)

                text = re.sub(
                    url,
                    new_url[1],
                    text,
                )

                main(slug=slug[1], cur=cur)

        with Path(
            file.parent,
            f"{file.stem}.md",
        ).open(
            "w",
            encoding="utf-8",
        ) as f:
            f.write(text)


def get_posts(
    slug: int,
    cur: psycopg.Cursor,
) -> list | None:
    res = cur.execute(
        """
        with ids as (
            select max(id) as id, post_id from posts where last_modified < '2025-10-31' group by 2
        ),
        rows as (
            select
                p.version as version,
                p.id as id,
                p.post_id,
                p.published as published,
                p.last_modified,
                p.title,
                p.excerpt,
                'Ken' as author,
                p.published::date || '-' || p.slug as filename,
                string_agg(distinct t.slug, ' ') as tag_list,
                string_agg(distinct c.slug, ' ') FILTER (WHERE c.id < 3601) as category_list,
                regexp_replace(m.url, 'http://estreetshuffle.com/wp-content/uploads/', '../../assets/') as header_img,
                p.post_id,
                p.content,
                p.url,
                p.slug
            from posts p
                left join post_categories pc on pc.post_id = p.id
                left join categories c on c.id = pc.category_id
                left join post_tags pt on pt.post_id = p.id
                left join tags t on t.id = pt.tag_id
                left join featured_media m on m.id = p.featured_media
            group by
            2,3,12
        )

        select * from rows
        where id = %(id)s
        """,
        {"id": slug},
    ).fetchall()

    if res:
        return res

    return None


def main(cur: psycopg.Cursor, slug: int) -> None:
    res = get_posts(slug, cur)

    if res:
        for post in res:
            print(post["filename"])

            title = post["title"].strip('"').replace('"', "'")

            post_file = Path(
                rf"C:\Users\bvw20\Documents\Software\Programming\Website\shuffle\_posts\{post['filename']}.md",
            )

            with post_file.open("w", encoding="utf-8") as f:
                f.write("---\n")

                if post["header_img"]:
                    f.write("layout: post\n")
                else:
                    f.write("layout: default-post\n")

                f.write(f'title: "{title}"\n')
                f.write(f'author: "{post["author"]}"\n')
                f.write(f'excerpt: "{post["excerpt"].strip()}"\n')

                if post["tag_list"]:
                    f.write(f"tags: {post['tag_list']}\n")

                if post["category_list"]:
                    f.write(f"categories: {post['category_list']}\n")

                if post["header_img"]:
                    f.write(f"header_img: {post['header_img']}\n")

                f.write(f"post_id: {post['post_id']}\n")

                f.write("---\n")
                f.write(post["content"])


if __name__ == "__main__":
    with load_db() as conn, conn.cursor() as cur:
        df = pd.read_csv(
            r"C:\Users\bvw20\Documents\Personal\Projects\Bruce Stuff\Websites\e-street-shuffle\shuffle-archive\notes\sheets\master-post-list.csv",
        )

        for row in df.itertuples():
            main(slug=row.id, cur=cur)
        # with Path(
        #     r"C:\Users\bvw20\Documents\Personal\Projects\Bruce Stuff\Websites\e-street-shuffle\shuffle-archive\notes\sheets\master-post-list.csv",
        # ).open("r", encoding="utf-8") as f:
        #     for line in f:
        #         main(slug=line.split(",")[0], cur=cur)
