import pickle

from tqdm import tqdm

from extraction.read_config import conf
from extraction.functions_headers import read_headers

fp_reverse = conf["dirs"]["headers_reverse"]

def read_pickle(*args, fp_write=fp_reverse):
    with open(fp_write, "rb") as f, tqdm(desc="Reading pickle") as pbar:
        while True:
            try:
                yield from pickle.load(f)
                pbar.update(1)
            except EOFError:
                break        
def main():
    for header, titles in read_pickle():
        print(header)

if __name__ == "__main__":
    main()