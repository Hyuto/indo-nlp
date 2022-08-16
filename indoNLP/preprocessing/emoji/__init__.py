from typing import Dict

from indoNLP.preprocessing.emoji.emoji_data import EMOJI_DATA

# fmt: off
__all__ = [
    # data
    "EMOJI_DATA", "WORDS_EMOJI_DATA",

    # regex patterns
    "EMOJI_PATTERN", "EN_WORDS_EMOJI_PATTERN",
    "ID_WORDS_EMOJI_PATTERN", "ALIAS_WORDS_EMOJI_PATTERN",
]

# fmt: on
def _generate_words_to_emoji_mapper(
    emoji_data: Dict[str, Dict[str, str]]
) -> Dict[str, Dict[str, str]]:
    """Generate words to emoji mapper"""
    result: Dict[str, Dict[str, str]] = {"en": {}, "id": {}, "alias": {}}
    for emoji, values in emoji_data.items():
        result["en"][values["en"]] = emoji
        result["id"][values["id"]] = emoji
        if values.get("alias"):
            result["alias"][values["alias"]] = emoji
        else:
            result["alias"][values["id"]] = emoji
    return result


# data
EMOJI_DATA = {k: v for k, v in sorted(EMOJI_DATA.items(), key=lambda x: len(x[0]), reverse=True)}
WORDS_EMOJI_DATA = _generate_words_to_emoji_mapper(EMOJI_DATA)

# pattern
EMOJI_PATTERN = f"({'|'.join(EMOJI_DATA.keys())})"
EN_WORDS_EMOJI_PATTERN = f"({'|'.join(WORDS_EMOJI_DATA['en'].keys())})"
ID_WORDS_EMOJI_PATTERN = f"({'|'.join(WORDS_EMOJI_DATA['id'].keys())})"
ALIAS_WORDS_EMOJI_PATTERN = f"({'|'.join(WORDS_EMOJI_DATA['alias'].keys())})"
