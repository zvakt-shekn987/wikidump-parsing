import re
import yaml

YAML_INDENT = '  '
YAML_HYPHEN = ''
CHAR_QUOTE = '"'

TEXT_RE = re.compile(
    r"<text\b[^>]*/>|<text\b[^>]*>.*?</text>",
    re.DOTALL)

TEXT_RE2 = re.compile(
    r"<text\b[^>]*>(.*?)</text>",
    re.DOTALL)

HEAD_LEFT = re.compile(r"\n(\={2,})", re.DOTALL)
HEAD_RIGHT = re.compile(r"(\={2,})¶", re.DOTALL)

def extract_text_element(page, include_tags=False):
    """Extracts the first <text> element in the .xml, 
    which is most likely the one we are looking for."""
    if include_tags:

        match = TEXT_RE.search(page)
        if match:
            text = match.group()
            return text
        return None

    else:

        match = TEXT_RE2.search(page)
        if match:
            text = match.group(1)
            return text
        return None

def text_to_yaml(text, title, *args, linebreak_placeholder="¶"):
    """Wikitext to YAML
    Line breaks get converted into pillcrows '¶';
    there are ways to handle line breaks in YAML
    but not dealing with them makes our lives easier.
    """

    if not text:
        text = ''

    text = text.replace('\n', '¶') 
    text = text.replace('¶=', '\n=')

    # text = HEAD_RIGHT.sub(f": {CHAR_QUOTE}", text)  # left quote

    text = HEAD_RIGHT.sub(lambda m: f": "
                         + "\n" + YAML_INDENT
                         + YAML_INDENT * (len(m.group()) - 2)
                         + f"CONTENT: {CHAR_QUOTE}" 
                         ,text)

    # text = text.replace('\n=', '\n-=')
    # text = HEAD_LEFT.sub(r"\n\1- ", text)
    text = HEAD_LEFT.sub(lambda m: '\n' 
                         + YAML_INDENT * (len(m.group()) - 2) 
                         + CHAR_QUOTE
                         ,text)
    
    text = text.replace('\n', f"{CHAR_QUOTE}\n") # right quote
    text = text.replace(f": {CHAR_QUOTE}\n", f"{CHAR_QUOTE}:\n")
    # text = re.sub()

    text = f"{CHAR_QUOTE}{title}{CHAR_QUOTE}:\n{YAML_INDENT}{YAML_HYPHEN}{f"CONTENT: {CHAR_QUOTE}" }{text}{CHAR_QUOTE}"

    return text