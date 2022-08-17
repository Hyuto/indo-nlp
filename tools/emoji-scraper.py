import logging

import requests
from bs4 import BeautifulSoup
from utils import format_unicode, normalizer, write_python_file

# Setup logging
logging.basicConfig(
    format="[%(levelname)s] %(asctime)s %(filename)s -- %(message)s",
    level=logging.INFO,
)


def get_emoji_data_unicode(url):
    def _parse_line(line):
        code = format_unicode(line.split(";")[0].strip())
        status = line.split(";")[1].split("#")[0].strip()
        title = normalizer(" ".join(line.split(";")[1].split("#")[1].split()[2:]))
        return code, status, title

    status_mapper = {
        "component": 1,
        "fully-qualified": 2,
        "minimally-qualified": 3,
        "unqualified": 4,
    }

    page = requests.get(url).text.split("\n")
    data = {}
    for line in page:
        if line != "":
            if line[0] != "#":
                code, status, title = _parse_line(line)
                if title not in data:
                    data[title] = {"code": code, "status": status_mapper[status]}
                else:
                    if status_mapper[status] < data[title]["status"]:
                        data[title] = {"code": code, "status": status_mapper[status]}
    return data


def get_emoji_data_emojiterra(url: str) -> dict:
    """Get emoji data from https://emojiterra.com

    Args:
        url (str): url

    Returns:
        emoji data
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
    emoji_dict = get_emoji_data_unicode("https://unicode.org/Public/emoji/14.0/emoji-test.txt")
    emoji_data_en = get_emoji_data_emojiterra("https://emojiterra.com/copypaste/")
    emoji_data_id = get_emoji_data_emojiterra("https://emojiterra.com/copypaste/id/")

    assert len(emoji_data_en) >= len(emoji_data_id), "id emoji > en emoji"

    result = {}
    for x in emoji_data_en:
        title = emoji_data_en[x]["title"]

        if title in emoji_dict:
            code = emoji_dict[title]["code"]
        else:
            code = x
            logging.warning(f"not found code emoji : {emoji_data_en[x]['title']}")

        result[code] = {"en": emoji_data_en[x]["title"]}

        if x in emoji_data_id.keys():
            result[code]["id"] = emoji_data_id[x]["title"]

            if emoji_data_id[x]["title"] != emoji_data_id[x]["alias"]:
                result[code]["alias"] = emoji_data_id[x]["alias"]
        else:
            logging.warning(f"missing indonesian emoji : {x} - {emoji_data_en[x]['title']}")

    write_python_file(result)


if __name__ == "__main__":
    main()
