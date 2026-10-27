import sys, yaml
import argparse

from . import functions as fu
from . import functions_sql as fusql
from . import functions_headers as fuhead

def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    p_bz2_to_sql = subparsers.add_parser("bz2-to-sql",
        help="Turns the .txt.bz2 index into SQL. Run once before any lookup.")
    p_bz2_to_sql.set_defaults(func=fusql.bz2_to_sql)    

    p_all_headers = subparsers.add_parser("all-headers",
        help="Generates list of headers from dump. Run once.")
    p_all_headers.set_defaults(func=fuhead.extract_headers)  

    p_reverse_headers = subparsers.add_parser("reverse-headers",
        help="Header list (title/headers) into header/titles. Run once. \
            Also creates value count summary.")
    p_reverse_headers.set_defaults(func=fuhead.reverse_list)  
    
    p_ext_page = subparsers.add_parser("ext-page")
    p_ext_page.add_argument("-b", "--byte_offset")
    p_ext_page.add_argument("-p", "--page_id")
    p_ext_page.set_defaults(func=lambda args: fu.get_page(
        byte_offset=args.byte_offset,
        page_id=args.page_id
    ))

    p_ext_word = subparsers.add_parser("ext-word")
    p_ext_word.add_argument("-w", "--word")
    p_ext_word.set_defaults(func=lambda args: fu.get_word(
        word=args.word
    ))

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()