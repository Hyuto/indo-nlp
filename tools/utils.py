import json
import re
import unicodedata


def normalizer(text: str) -> str:
    """Unicode text normalizer

    Args:
        text (str): raw text

    Returns:
        str: cleaned text
    """
    text = unicodedata.normalize("NFKD", text.lower()).encode("ascii", "ignore").decode("ascii")
    text = re.sub("[:,]", "", text)
    return re.sub(" ", "_", text.strip())


def format_unicode(text: str) -> str:
    """Format unicode string

    Args:
        text (str): unicode string

    Returns:
        str: formated unicode string
    """
    return "".join(
        ["\\U0000" + code if len(code) == 4 else "\\U000" + code for code in text.split()]
    )


def write_python_file(emoji_data: dict) -> None:
    """Write emoji data to python file

    Args:
        emoji_data (dict): emoji data dictionary
    """
    template = "# -*- coding: utf-8 -*-\n\n"
    template += '"""Data containing emoji mapper retrieved from https://emojiterra.com\n'
    template += '   and https://unicode.org/Public/emoji/14.0/emoji-test.txt"""\n\n'
    template += '__all__ = ["EMOJI_DATA"]\n\n'
    template += "EMOJI_DATA = {\n"
    template += ",\n".join([f'    "{x}" : {json.dumps(emoji_data[x])}' for x in emoji_data])
    template += "\n}"

    with open("emoji_data.py", "w") as writer:
        writer.write(template)
