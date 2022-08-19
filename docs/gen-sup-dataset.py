import os

import mkdocs_gen_files

from indoNLP.dataset.list import DATASETS


def md_table(headings, aligins, data):
    mapper = {"center": ":--:", "left": ":--", "right": "--:"}
    table = "| " + " | ".join(map(lambda x: x.title(), headings)) + " |\n"
    table += "| " + " | ".join([mapper[x.lower()] for x in aligins]) + " |\n"
    for row in data:
        table += "| " + " | ".join([str(x) for x in row]) + " |\n"
    return table


docs = os.path.join("api", "dataset", "sup-dataset.md")

heading = ["name", "description", "author", "year", "homepage", "tags"]
datas = []
for name in DATASETS:
    data = [name]
    for needed_col in ["description", "author", "year"]:
        data.append(DATASETS[name]["info"][needed_col])
    data.append(f'[{name}]({DATASETS[name]["info"]["homepage"]})')
    data.append(", ".join(DATASETS[name]["info"]["tags"]))
    datas.append(data)

table = md_table(heading, ["center", "left", "center", "center", "left", "center"], datas)
with mkdocs_gen_files.open(docs, "a") as fd:
    fd.write("\n" + table)
