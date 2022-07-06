import json
import re
import unicodedata
import requests
from bs4 import BeautifulSoup


def normalizer(text: str) -> str:
    """Unicode text normalizer

    Args:
        text (str): raw text

    Returns:
        str: cleaned text
    """
    text = unicodedata.normalize("NFKD", text.lower()).encode("ascii", "ignore").decode("ascii")
    text = re.sub(":", "", text)
    return re.sub(" ", "_", text.strip())


def get_emoji_data(url: str) -> dict:
    """Get emoji data from https://emojiterra.com

    Args:
        url (str): url

    Returns:
        dict: emoji data
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    container = soup.find(id="cp-emojis")
    emojis = container.find_all("li")

    emoji_data = {}

    for emoji in emojis:
        emoji_data[emoji.attrs["data-clipboard-text"].encode("unicode-escape").decode("ascii")] = {
            "title": normalizer(emoji.attrs["title"]),
            "alias": normalizer(emoji.attrs["data-f"]),
        }

    return emoji_data


def main():
    emoji_data_en = get_emoji_data("https://emojiterra.com/copypaste/")
    emoji_data_id = get_emoji_data("https://emojiterra.com/copypaste/id/")

    assert len(emoji_data_en) >= len(emoji_data_id), "id emoji > en emoji"

    result = {}
    for x in emoji_data_en:
        result[x] = {"en": emoji_data_en[x]["title"], "alias": {"en": emoji_data_en[x]["alias"]}}
        if x in emoji_data_id.keys():
            result[x]["id"] = emoji_data_id[x]["title"]
            result[x]["alias"]["id"] = emoji_data_id[x]["alias"]
        else:
            print(f"missing indonesian emoji : {x} - {emoji_data_en[x]['title']}")

    with open("emoji-data.json", "w") as reader:
        reader.write(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
