import re

from indoNLP.preprocessing.slang_data import SLANG_DATA
from indoNLP.preprocessing.stopwords_data import STOPWORDS

# TODO
# 1. support case sensitive
# 2. make pipeline
# 3. vectorization

__all__ = [
    "remove_html",
    "remove_url",
    "remove_stopwords",
    "replace_slang",
    "replace_word_elongation",
]

# PATTERNS
HTML_PATTERN = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
URL_PATTERN = re.compile(
    r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*"
    + r"([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*",
    flags=re.IGNORECASE,
)
SLANG_PATTERN = re.compile(
    "(%s)" % "|".join(map(lambda x: rf"\b{x}\b", SLANG_DATA.keys())),
    flags=re.IGNORECASE,
)
STOPWORDS_PATTERN = re.compile(
    "(%s)" % "|".join(map(lambda x: rf"\b{x}\b", STOPWORDS)),
    flags=re.IGNORECASE,
)
WE_PATTERN = re.compile(r"\b\w*([a-zA-Z])(\1{1,})\w*\b")


def remove_html(text: str) -> str:
    """Remove HTML tags from text.

    Args:
        text (str): text that have html tags on

    Returns:
        str: cleaned text
    """
    return HTML_PATTERN.sub("", text)


def remove_url(text: str) -> str:
    """Remove URL from text.

    Args:
        text (str): text that have url on

    Returns:
        str: cleaned text
    """
    return URL_PATTERN.sub("", text)


def remove_stopwords(text: str) -> str:
    """Remove stopwords from text.

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    return STOPWORDS_PATTERN.sub("", text)


def replace_slang(text: str) -> str:
    """Replace slang words in sentence based on dictionary
    source : https://stackoverflow.com/a/15175239

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    return SLANG_PATTERN.sub(lambda mo: SLANG_DATA[mo.string[mo.start() : mo.end()].lower()], text)


def replace_word_elongation(text: str) -> str:
    """Replace word elongation inside text

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    return WE_PATTERN.sub(
        lambda mo: re.sub(r"(?i)([a-zA-Z])(\1{1,})", r"\1", mo.string[mo.start() : mo.end()]), text
    )
