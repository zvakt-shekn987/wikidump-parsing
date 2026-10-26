import bz2
import sqlite3
from tqdm import tqdm

from .read_config import conf

def bz2_to_sql(*args, fp=conf["dirs"]["index"], fp_db=conf["dirs"]["index_db"]):

    with bz2.open(fp, "rt", encoding="utf-8") as src:
        with sqlite3.connect(fp_db) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS pages (
                    title TEXT PRIMARY KEY,
                    byte_offset INTEGER NOT NULL,
                    page_id INTEGER NOT NULL
                )
            """)

            batch = []

            for line in tqdm(src, desc="Creating SQL database out of index"):
                offset, page_id, title = line.rstrip("\n").split(":", 2)
                batch.append((title, int(offset), int(page_id)))

                if len(batch) >= 10000:
                    db.executemany(
                        "INSERT OR REPLACE INTO pages "
                        "(title, byte_offset, page_id) VALUES (?, ?, ?)",
                        batch
                    )
                    batch.clear()

            if batch:
                db.executemany(
                    "INSERT OR REPLACE INTO pages "
                    "(title, byte_offset, page_id) VALUES (?, ?, ?)",
                    batch
                )

def word_lookup(word, *args, fp_db=conf["dirs"]["index_db"]) -> tuple | None:
    with sqlite3.connect(fp_db) as db:
        row = db.execute(
            "SELECT byte_offset, page_id FROM pages WHERE title = ?",
            (word,)
        ).fetchone()

    return row