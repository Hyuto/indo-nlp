import os

import mkdocs_gen_files

from indoNLP.dataset.list import DATASETS


class Formater:
    def format_title(self, title):
        return f"## {title}\n\n"

    def format_author_year(self, author, year):
        text = ""
        if author != "unknown" and year != "unknown":
            text = f"{author} - {year}\n\n"
        elif author != "unknown":
            text = f"{author}\n\n"
        elif year != "unknown":
            text = f"{year}\n\n"
        return text

    def run(self, title, data):
        text = self.format_title(title)
        text += self.format_author_year(data["author"], data["year"])
        text += f"{data['description']}\n\n"
        text += f":material-home-circle: [Homepage]({data['homepage']})\n\n"
        if data["citation"] != "no-citation":
            text += f"!!! cite\n    {data['citation']}\n\n"
        text += f":fontawesome-solid-tags: {', '.join(sorted(data['tags']))}\n\n"
        return text


docs = os.path.join("api", "dataset", "sup-dataset.md")
text = ""
formater = Formater()
for name in DATASETS:
    data = DATASETS[name]["info"]
    text += formater.run(name, data)

with mkdocs_gen_files.open(docs, "a") as fd:
    fd.write("\n" + text)
