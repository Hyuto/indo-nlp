from typing import Any, Dict

from indoNLP.dataset.reader import *

__all__ = ["DATASETS"]


DATASETS: Dict[str, Dict[str, Any]] = {
    "twitter-puisi": {
        "info": {
            "description": "Loosely filtered poem from various user on Twitter",
            "author": "unknown",
            "year": "unknown",
            "citation": "no-citation",
            "homepage": "https://github.com/Wikidepia/indonesian_datasets/tree/master/crawl/twitter-puisi",
            "tags": ["unlabeled"],
        },
        "files": [
            {
                "filename": "pelangipuisi.jsonl",
                "url": "https://raw.githubusercontent.com/Wikidepia/indonesian_datasets/master/crawl/twitter-puisi/data/pelangipuisi.jsonl",
                "is_large": False,
                "extract": False,
            }
        ],
        "reader": {
            "main": {
                "filename": "pelangipuisi.jsonl",
                "path": "pelangipuisi.jsonl",
                "is_table": True,
                "reader": jsonl_table_reader,
                "args": {},
            }
        },
    },
    "id-multi-label-hate-speech-and-abusive-language-detection": {
        "info": {
            "description": "Dataset for multi-label hate speech and abusive language detection in the Indonesian Twitter",
            "author": "Muhammad Okky Ibrohim and Indra Budi",
            "year": 2019,
            "citation": "Muhammad Okky Ibrohim and Indra Budi. 2019. Multi-label Hate Speech and Abusive Language Detection in Indonesian Twitter. In ALW3: 3rd Workshop on Abusive Language Online, 46-57.",
            "homepage": "https://github.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection",
            "tags": [
                "labeled",
                "hate speech",
                "abusive language detection",
                "multi-label",
                "twitter",
            ],
        },
        "files": [
            {
                "filename": "re_dataset.csv",
                "url": "https://raw.githubusercontent.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection/master/re_dataset.csv",
                "is_large": False,
                "extract": False,
            }
        ],
        "reader": {
            "main": {
                "filename": "re_dataset.csv",
                "path": "re_dataset.csv",
                "is_table": True,
                "reader": csv_reader,
                "args": {"fd_kwargs": {"encoding": "ISO-8859-1"}},
            }
        },
    },
}
