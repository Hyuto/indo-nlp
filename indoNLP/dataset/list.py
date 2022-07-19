from typing import Any, Dict

from indoNLP.dataset.reader import *

__all__ = ["DATASETS"]


DATASETS: Dict[str, Dict[str, Any]] = {
    "twitter-puisi": {
        "info": {
            "description": "Loosely filtered poem from various user on Twitter",
            "author": None,
            "year": None,
            "citation": "no-citation",
            "homepage": "https://github.com/Wikidepia/indonesian_datasets/tree/master/crawl/twitter-puisi",
            "tags": {"unlabeled"},
        },
        "urls": [
            {
                "filename": "pelangipuisi.jsonl",
                "url": "https://raw.githubusercontent.com/Wikidepia/indonesian_datasets/master/crawl/twitter-puisi/data/pelangipuisi.jsonl",
                "is_large": False,
                "extract": False,
            }
        ],
        "files": {
            "pelangipuisi.jsonl": {"is_table": True, "reader": jsonl_table_reader, "tag": "main"}
        },
    }
}
