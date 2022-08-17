import os
from pathlib import Path

import mkdocs_gen_files

docs = "reference.md"
project_dir = "indoNLP"
generate = [
    os.path.join(project_dir, "preprocessing", "__init__.py"),
    os.path.join(project_dir, "dataset", "__init__.py"),
    os.path.join(project_dir, "dataset", "downloader.py"),
    os.path.join(project_dir, "dataset", "reader.py"),
    os.path.join(project_dir, "dataset", "utils.py"),
]

for path in generate:
    path = Path(path)
    module_path = path.with_suffix("")
    parts = tuple(path.relative_to(project_dir).with_suffix("").parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]

    with mkdocs_gen_files.open(docs, "a") as fd:
        ident = ".".join([project_dir, *parts])
        fd.write(f"\n::: {ident}" + "\n    options:\n      show_root_heading: false")
