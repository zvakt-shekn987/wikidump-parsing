import yaml

from extraction.read_config import conf
from extraction.functions_parse import extract_text_element, text_to_yaml


def main():

    with open(conf["dirs"]["sample_page"], 'r', encoding="utf-8") as f:
        page = f.read()

    title = "sample_title"

    text = extract_text_element(page)
    text = text_to_yaml(text, title)

    fp_write = conf["dirs"]["sample_page"].replace(".txt", ".yaml")
    with open(fp_write, 'w', encoding="utf-8") as f:
        f.write(text)

    fp_write = conf["dirs"]["sample_page"].replace(".txt", ".py")
    data = yaml.safe_load(text)
    with open(fp_write, 'w', encoding="utf-8") as f:
        f.write(str(data))

if __name__ == "__main__":
    main()
