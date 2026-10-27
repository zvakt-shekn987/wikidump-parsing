import bz2
import re
import html
import pickle
import pandas as pd

from collections import defaultdict
from tqdm import tqdm

from . import utils as ut
from .read_config import conf

PAGE_RE = re.compile(rb"<page\b[^>]*>.*?</page>", re.DOTALL)
TITLE_RE = re.compile(rb"<title\b[^>]*>(.*?)</title>", re.DOTALL)
TEXT_RE = re.compile(rb"<text\b[^>]*>(.*?)</text>", re.DOTALL)
NAMESPACE_RE = re.compile(rb"<ns>(\d+)</ns>")
HEADER_RE = re.compile(
    r"^(={1,6})[ \t]*(.*?)[ \t]*\1[ \t]*$",
    re.MULTILINE
)

def process_page(page):
    title_match = TITLE_RE.search(page)
    text_match = TEXT_RE.search(page)
    namespace_match = NAMESPACE_RE.search(page)

    title = html.unescape(title_match.group(1).decode("utf-8")) if title_match else None
    page_text = html.unescape(text_match.group(1).decode("utf-8")) if text_match else ""   
    namespace = html.unescape(namespace_match.group(1).decode("utf-8")) if namespace_match else ""
    headers = [(len(level), heading) for level, heading in HEADER_RE.findall(page_text)]

    return title, namespace, headers

def _extract_headers(fp_dump, *args, buffer_size=1024 * 1024):
    buffer = b""

    with bz2.open(fp_dump, "rb") as f, tqdm(desc="Extracting pages", unit=" pages") as pbar:
        while chunk := f.read(buffer_size):
            buffer += chunk
            matches = list(PAGE_RE.finditer(buffer))

            for match in matches:
                pbar.update(1)
                yield process_page(match.group())

            if matches:
                buffer = buffer[matches[-1].end():]

        for match in PAGE_RE.finditer(buffer):
            pbar.update(1)
            yield process_page(match.group())
            
def write_headers(gen, fp_write, *args, buffer_size=1024):
    ut.buffered_writer(gen, fp_write)

def extract_headers(*args, fp_dump=conf["dirs"]["wikidump"], fp_headers=conf["dirs"]["headers"]):
    gen = _extract_headers(fp_dump)
    write_headers(gen, fp_headers)
    
def read_headers(*args, fp_headers=conf["dirs"]["headers"]):
    with open(fp_headers, "rb") as f, tqdm(unit="page", desc="Reading headers") as pbar:
        while True:
            try:
                yield from pickle.load(f)
                pbar.update(1)
            except EOFError:
                break 
            
def reverse_list(*args, fp_reverse=conf["dirs"]["headers_reverse"]):

    data = defaultdict(list)
    
    for title, namespace, headers in read_headers():
        if namespace == '0':
            for header in headers:
                data[header].append(title)
            
    _pickle = ((k, v) for k, v in tqdm(data.items(), desc="Converting dict to tuple"))
    ut.buffered_writer(_pickle, fp_write=fp_reverse)
         
    data_summary = [{"level": k[0], "header": k[1], "titles": len(v)} for k, v in tqdm(data.items())]
    pd.DataFrame.from_records(data_summary).to_csv(conf["dirs"]["headers_summary"], sep='\t')
    
    
    

    