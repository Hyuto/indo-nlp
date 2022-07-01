import json
import requests
import unicodedata
from bs4 import BeautifulSoup

if __name__ == "__main__":
    normalize = (
        lambda x: unicodedata.normalize("NFKD", x.lower()).encode("ascii", "ignore").decode("ascii")
    )

    page_en = requests.get("https://emojiterra.com/copypaste/")
    soup_en = BeautifulSoup(page_en.content, "html.parser")
    container_en = soup_en.find(id="cp-emojis")
    emojis_en = container_en.find_all("li")

    emoji_data_en = {}

    for emoji in emojis_en:
        emoji_data_en[emoji.attrs["data-clipboard-text"]] = normalize(emoji.attrs["title"])

    page_id = requests.get("https://emojiterra.com/copypaste/id/")
    soup_id = BeautifulSoup(page_id.content, "html.parser")
    container_id = soup_id.find(id="cp-emojis")
    emojis_id = container_id.find_all("li")

    emoji_data_id = {}

    for emoji in emojis_id:
        emoji_data_id[emoji_data_en[emoji.attrs["data-clipboard-text"]]] = {
            "transform": normalize(emoji.attrs["title"]),
            "alias": normalize(emoji.attrs["data-f"]),
        }

    missing = set(emoji_data_en.values()).difference(set(emoji_data_id.keys()))
    print("Missing indonesian emoji")
    for miss in missing:
        print(f"* {miss}")

    with open("emoji-data.json", "w") as reader:
        reader.write(json.dumps(emoji_data_id))
