import re
from IndoNLP._dict import CIL as _CIL

# RE PATTERNS
_CLEAN_HTML = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
_CLEAN_CIL = re.compile("|".join([f"\\b{x}\\b" for x in _CIL.keys()]), re.IGNORECASE)


def clean_html(text: str) -> str:
    """Cleaning HTML tags from text.

    Args:
        text (str): text that have html tags on

    Returns:
        str: cleaned text
    """
    clean = re.sub(_CLEAN_HTML, "", text)
    return clean


def fix_slang(text: str) -> str:
    """Fixing slang words in text.

    Dictionary: Kamus Alay - Colloquial Indonesian Lexicon by Salsabila, Ali, Yosef, and Ade
    https://github.com/nasalsabila/kamus-alay

    Args:
        text (str): text that have slang words on

    Returns:
        str: Fixed text without slang words on
    """
    for x in set(_CLEAN_CIL.findall(text)):
        text = re.sub(f"\\b{x}\\b", _CIL[x.lower()], text, flags=re.IGNORECASE)
    return text
