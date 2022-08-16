import re
from typing import Callable, Match, Sequence, Tuple

from indoNLP.preprocessing.emoji import *
from indoNLP.preprocessing.slang_data import SLANG_DATA
from indoNLP.preprocessing.stopwords_data import STOPWORDS

# fmt: off
__all__ = [
    # main functions
    "remove_html", "remove_url", "remove_stopwords", "replace_slang", 
    "replace_word_elongation", "pipeline", "emoji_to_words", "words_to_emoji",

    # data
    "EMOJI_DATA", "WORDS_EMOJI_DATA", "SLANG_DATA", "STOPWORDS",

    # regex patterns
    "HTML_PATTERN", "URL_PATTERN", "SLANG_PATTERN", "STOPWORDS_PATTERN",
    "WE_PATTERN", "EMOJI_PATTERN", "EN_WORDS_EMOJI_PATTERN", 
    "ID_WORDS_EMOJI_PATTERN", "ALIAS_WORDS_EMOJI_PATTERN",
]

# fmt: on
HTML_PATTERN = r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"
URL_PATTERN = (
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
    + r"\b/?(?!@)))"
)
SLANG_PATTERN = rf"\b({'|'.join(SLANG_DATA.keys())})\b"
STOPWORDS_PATTERN = rf"\b({'|'.join(STOPWORDS)})\b"
WE_PATTERN = r"\b\w*([a-zA-Z])(\1{1,})\b"


def remove_html(text: str) -> str:
    """Remove HTML tags from text.

    Args:
        text (str): Text that have html tags on

    Returns:
        str: Cleaned text

    Examples:
        Removing all html tags inside of a string.

        >>> indoNLP.preprocessing.remove_html("website <a href='https://google.com'>google</a>")
        "website google"
    """
    return re.sub(HTML_PATTERN, "", text, flags=re.IGNORECASE).strip()


def remove_url(text: str) -> str:
    """Remove URL from text.

    Args:
        text (str): Text that have url on

    Returns:
        str: Cleaned text

    Examples:
        Removing all urls inside of a string.

        >>> indoNLP.preprocessing.remove_url("retrieved from https://gist.github.com/gruber/8891611")
        "retrieved from"
    """
    return re.sub(URL_PATTERN, "", text, flags=re.IGNORECASE).strip()


def remove_stopwords(text: str) -> str:
    """Remove stopwords from text.

    Args:
        text (str): Text/sentence

    Returns:
        str: Text after

    Examples:
        Removing stopwords inside of a string.

        >>> indoNLP.preprocessing.remove_stopwords("siapa yang suruh makan?!!")
        "suruh makan?!!"
    """
    return re.sub(STOPWORDS_PATTERN, "", text, flags=re.IGNORECASE).strip()


def replace_slang(text: str) -> str:
    """Replace slang words in sentence

    Args:
        text (str): Text/sentence

    Returns:
        str: Text after

    Examples:
        Replacing all slang words in a string to formal words.

        >>> indoNLP.preprocessing.replace_slang("emg siapa yg nanya?")
        "memang siapa yang bertanya?"
    """
    # https://stackoverflow.com/a/15175239
    return re.sub(
        SLANG_PATTERN,
        lambda mo: SLANG_DATA[mo.group(0).lower()],
        text,
        flags=re.IGNORECASE,
    )


def replace_word_elongation(text: str) -> str:
    """Replace word elongation inside text

    Args:
        text (str): Text/sentence

    Returns:
        str: Text after

    Examples:
        Replacing word elongation.

        >>> indoNLP.preprocessing.replace_word_elongation("kenapaaa?")
        "kenapa?"
    """
    # TODO: implement validation with wordlist using get_close_matches
    return re.sub(
        WE_PATTERN,
        lambda mo: re.sub(r"(?i)([a-zA-Z])(\1{1,})", r"\1", mo.group(0)),
        text,
        flags=re.IGNORECASE,
    )


def pipeline(pipe: Sequence[Callable[[str], str]]) -> Callable[[str], str]:
    """Pipelining multiple preprocessing functions

    Args:
        pipe (Sequence[Callable[[str], str]]): Sequence of functions

    Returns:
        Callable[[str], str]: Callable pipeline function

    Examples:
        Pipelining preprocessing functions

        >>> from indoNLP.preprocessing import pipeline, replace_word_elongation, replace_slang
        >>> pipe = pipeline([replace_word_elongation, replace_slang])
        >>> pipe("Knp emg gk mw makan kenapaaa???")
        "kenapa memang enggak mau makan kenapa???"
    """
    # https://stackoverflow.com/a/57763458
    def _run(value: str) -> str:
        for step in pipe:
            value = step(value)
        return value

    return _run


def emoji_to_words(
    text: str,
    lang: str = "id",
    use_alias: bool = False,
    delimiter: Tuple[str, str] = ("!", "!"),
) -> str:
    """Transform emoji to words

    Args:
        text (str): Emoji included text.
        lang (str, optional): Language code. available "en" and "id". Defaults to "id".
        use_alias (bool, optional): Use alias translation. Only supported when lang == "id".
            Defaults to False.
        delimiter (Tuple[str, str], optional): Delimiter on emoji translation.
            Defaults to ("!", "!").

    Returns:
        str: Transformed text.

    Examples:
        Translate emoji to bahasa

        >>> indoNLP.preprocessing.emoji_to_words("emoji 😀😁")
        "emoji !wajah_gembira!!wajah_gembira_dengan_mata_bahagia!"

        Translate emoji to english

        >>> indoNLP.preprocessing.emoji_to_words("emoji 😀😁", lang="en")
        "emoji !grinning_face!!beaming_face_with_smiling_eyes!"

        Using alias. Only works on ``lang == "id"``

        >>> indoNLP.preprocessing.emoji_to_words("emoji 😀", use_alias=True)
        "emoji !wajah_gembira_bahagia_muka_senang!"

        Using custom delimiter

        >>> indoNLP.preprocessing.emoji_to_words("emoji 😁", delimiter=("^","$"))
        "emoji ^wajah_gembira_dengan_mata_bahagia$"
    """

    def _get_emoji_translation(mo: Match[str]) -> str:
        """Get emoji translation"""
        _emoji = EMOJI_DATA[mo.group(0)]
        if use_alias:
            assert lang == "id", "use_alias only support Indonesian language"
            return delimiter[0] + _emoji["alias"] + delimiter[1]
        return delimiter[0] + _emoji[lang] + delimiter[1]

    assert lang in ["en", "id"], "Only supported English (en) and Indonesian (id) language"
    return re.sub(EMOJI_PATTERN, _get_emoji_translation, text, flags=re.UNICODE)


def words_to_emoji(
    text: str,
    lang: str = "id",
    use_alias: bool = False,
    delimiter: Tuple[str, str] = ("!", "!"),
) -> str:
    """Transform words to emoji

    Args:
        text (str): Emoji code included text
        lang (str, optional): Language code. available "en" and "id". Defaults to "id".
        use_alias (bool, optional): Use alias translation. Only supported when lang == "id".
            Defaults to False.
        delimiter (Tuple[str, str], optional): Delimiter on emoji translation.
            Defaults to ("!", "!").

    Returns:
        str: Transformed text.

    Examples:
        Transform words to emoji

        >>> indoNLP.preprocessing.emoji_to_words("emoji !wajah_gembira!!wajah_gembira_dengan_mata_bahagia!")
        "emoji 😀😁"

        Transform english words to emoji

        >>> indoNLP.preprocessing.emoji_to_words("emoji !beaming_face_with_smiling_eyes!", lang="en")
        "emoji 😁"

        Using alias. Only works on ``lang == "id"``

        >>> indoNLP.preprocessing.emoji_to_words("emoji !wajah_gembira_bahagia_muka_senang!", use_alias=True)
        "emoji 😀"

        Using custom delimiter

        >>> indoNLP.preprocessing.emoji_to_words("emoji ^wajah_gembira_dengan_mata_bahagia$", delimiter=("^","$"))
        "emoji 😁"
    """

    def _get_emoji(mo: Match[str]) -> str:
        """Get emoji from words"""
        keyword = re.search(rf"{delimiter[0]}(.*?){delimiter[1]}", mo.group(0))
        assert keyword is not None  # ensure type
        return WORDS_EMOJI_DATA["alias" if use_alias else lang][keyword.group(1)]

    assert lang in ["en", "id"], "Only supported English (en) and Indonesian (id) language"
    pattern = EN_WORDS_EMOJI_PATTERN if lang == "en" else ID_WORDS_EMOJI_PATTERN
    if use_alias:
        assert lang == "id", "use_alias only support Indonesian language"
        pattern = ALIAS_WORDS_EMOJI_PATTERN
    return re.sub(rf"{delimiter[0]}{pattern}{delimiter[1]}", _get_emoji, text)
