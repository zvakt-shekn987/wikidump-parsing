# get_page.py
import bz2
import re
import pandas as pd

from .read_config import conf

from . import functions_sql as fusql

PAGE_RE = re.compile(rb"<page>.*?</page>", re.DOTALL)
ID_RE = re.compile(rb"<id>(\d+)</id>")

def _get_index(*args, fp_index=conf["dirs"]["index_decomp"]):
    ...

def get_page(byte_offset, page_id, *args, 
             fp_dump=conf["dirs"]["wikidump"], 
             write_to_file=True,
             fp_write=None,
             chunk_size=1024 * 1024):
    decoder = bz2.BZ2Decompressor()
    output = bytearray()

    if write_to_file:
        if not fp_write:
            fp_write = f"{byte_offset}_{page_id}.txt"

    with open(fp_dump, "rb") as f:
        f.seek(byte_offset)

        while not decoder.eof:
            chunk = f.read(chunk_size)
            if not chunk:
                raise EOFError("Unexpected end of dump")

            output.extend(decoder.decompress(chunk))

    target = str(page_id).encode("ascii")

    for match in PAGE_RE.finditer(output):
        ids = ID_RE.search(match.group())
        if ids and ids.group(1) == target:

            if write_to_file and fp_write:
                with open(fp_write, 'w', encoding="utf-8") as f:
                    f.write(match.group().decode())

            return match.group()  # Original decompressed XML bytes

    return None

def get_word(word, write_to_file=True, fp_write=None, *args):

    if not fp_write:
        fp_write=f"{word}.txt"

    byte_offset, page_id = fusql.word_lookup(word)
    
    return get_page(byte_offset, page_id, 
                    write_to_file=write_to_file, 
                    fp_write=fp_write)

def main():
    page = get_page(
        "enwiktionary-latest-pages-articles-multistream.xml.bz2",
        byte_offset=698,
        page_id=136,
    )

    if page is None:
        print("Page not found")
    else:
        print(page.decode("utf-8"))