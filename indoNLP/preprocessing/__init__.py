import re
from typing import Sequence, Callable, Any

from indoNLP.preprocessing.slang_data import SLANG_DATA
from indoNLP.preprocessing.stopwords_data import STOPWORDS

# TODO
# 1. support case sensitive
# 2. make pipeline
# 3. vectorization

__all__ = [
    # main functions
    "remove_html",
    "remove_url",
    "remove_stopwords",
    "replace_slang",
    "replace_word_elongation",
    # dictionaries
    "SLANG_DATA",
    "STOPWORDS",
    # regex patterns
    "HTML_PATTERN",
    "URL_PATTERN",
    "SLANG_PATTERN",
    "STOPWORDS_PATTERN",
    "WE_PATTERN",
]

# PATTERNS
HTML_PATTERN = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
URL_PATTERN = re.compile(
    # WEB URL matching pattern retrieved from https://gist.github.com/gruber/8891611
    r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia"
    + r"|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|"
    + r"am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|"
    + r"ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|"
    + r"er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|"
    + r"hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|"
    + r"la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|"
    + r"mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|"
    + r"qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|"
    + r"td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|"
    + r"ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))"
    + r"+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?"
    + r"<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|"
    + r"int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|"
    + r"au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|"
    + r"ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|"
    + r"fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|"
    + r"il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|"
    + r"lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|"
    + r"ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|"
    + r"sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|"
    + r"tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)"
    + r"\b/?(?!@)))",
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
    return HTML_PATTERN.sub("", text).strip()


def remove_url(text: str) -> str:
    """Remove URL from text.

    Args:
        text (str): text that have url on

    Returns:
        str: cleaned text
    """
    return URL_PATTERN.sub("", text).strip()


def remove_stopwords(text: str) -> str:
    """Remove stopwords from text.

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    return STOPWORDS_PATTERN.sub("", text).strip()


def replace_slang(text: str) -> str:
    """Replace slang words in sentence

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    # https://stackoverflow.com/a/15175239
    return SLANG_PATTERN.sub(
        lambda mo: SLANG_DATA[mo.string[mo.start() : mo.end()].lower()], text
    ).strip()


def replace_word_elongation(text: str) -> str:
    """Replace word elongation inside text

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    return WE_PATTERN.sub(
        lambda mo: re.sub(r"(?i)([a-zA-Z])(\1{1,})", r"\1", mo.string[mo.start() : mo.end()]), text
    ).strip()


def pipline(pipe: Sequence[Callable[[Any], Any]]) -> Callable[[Any], Any]:
    """Pipelining multiple of functions

    Args:
        pipe (Sequence[Callable[[Any], Any]]): Sequence of functions

    Returns:
        Callable[[Any], Any]: Callable pipeline function
    """
    # https://stackoverflow.com/a/57763458
    def _run(value: Any):
        for step in pipe:
            value = step(value)
        return value

    return _run
