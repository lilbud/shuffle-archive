import psycopg


def insert_author(cur: psycopg.Cursor, author: dict):
    name = author.get("name")
    url = author.get("url")

    cur.execute(
        """INSERT INTO authors (name, url) values (%s, %s) on conflict do nothing""",
        (name, url),
    )
