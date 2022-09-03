import os
from typing import Any, Dict

from indoNLP.dataset.reader import *

__all__ = ["DATASETS"]


DATASETS: Dict[str, Dict[str, Any]] = {
    "twitter-puisi": {
        "info": {
            "description": "Puisi - puisi yang difilter dari beberbagai pengguna di Twitter.",
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
                "path": "pelangipuisi.jsonl",
                "is_table": True,
                "reader": jsonl_table_reader,
                "args": {},
            }
        },
    },
    "id-multi-label-hate-speech-and-abusive-language-detection": {
        "info": {
            "description": "Dataset untuk pembelajaran multi-label tentang hate speech dan abusive language detection dari berbagai tweet di Twitter.",
            "author": "Muhammad Okky Ibrohim dan Indra Budi",
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
                "path": "re_dataset.csv",
                "is_table": True,
                "reader": csv_reader,
                "args": {"fd_kwargs": {"encoding": "ISO-8859-1"}},
            }
        },
    },
    "id-abusive-language-detection": {
        "info": {
            "description": "Dataset untuk pembelajaran multi-label tentang abusive language detection pada Bahasa Indonesia.",
            "author": "Muhammad Okky Ibrohim dan Indra Budi",
            "year": 2018,
            "citation": "Ibrohim, M.O., Budi, I.. A Dataset and Preliminaries Study for Abusive Language Detection in Indonesian Social Media. Procedia Computer Science 2018;135:222-229.",
            "homepage": "https://github.com/okkyibrohim/id-abusive-language-detection",
            "tags": ["labeled", "abusive language detection"],
        },
        "files": [
            {
                "filename": "re_dataset_two_labels.csv",
                "url": "https://raw.githubusercontent.com/okkyibrohim/id-abusive-language-detection/master/re_dataset_two_labels.csv",
                "is_large": False,
                "extract": False,
            },
            {
                "filename": "re_dataset_three_labels.csv",
                "url": "https://raw.githubusercontent.com/okkyibrohim/id-abusive-language-detection/master/re_dataset_three_labels.csv",
                "is_large": False,
                "extract": False,
            },
        ],
        "reader": {
            "two-labels": {
                "path": "re_dataset_two_labels.csv",
                "is_table": True,
                "reader": csv_reader,
                "args": {"fd_kwargs": {"encoding": "ISO-8859-1"}},
            },
            "three-labels": {
                "path": "re_dataset_three_labels.csv",
                "is_table": True,
                "reader": csv_reader,
                "args": {"fd_kwargs": {"encoding": "ISO-8859-1"}},
            },
        },
    },
    "asian-language-treebank-parallel-corpus": {
        "info": {
            "description": "Proyek ALT adalah proyek yang bertujuan untuk memajukan teknik NLP pada bahasa - bahasa di Asia melalui kolaborasi terbuka. Proses membangun ALT dimulai dengan mengambil sampel sekitar 20.000 kalimat dari Wikinews bahasa Inggris, dan kemudian diterjemahkan ke dalam bahasa lain.",
            "author": "Hammam Riza, Michael Purwoadi, Gunarso, Teduh Uliniansyah, Aw Ai Ti, Sharifah Mahani Aljunied, Luong Chi Mai, Vu Tat Thang, Nguyen Phuong Thai, Vichet Chea, Rapid Sun, Sethserey Sam, Sopheap Seng, Khin Mar Soe, Khin Thandar Nwet, Masao Utiyama, dan Chenchen Ding",
            "year": 2016,
            "citation": "Hammam Riza, Michael Purwoadi, Gunarso, Teduh Uliniansyah, Aw Ai Ti, Sharifah Mahani Aljunied, Luong Chi Mai, Vu Tat Thang, Nguyen Phuong Thai, Vichet Chea, Rapid Sun, Sethserey Sam, Sopheap Seng, Khin Mar Soe, Khin Thandar Nwet, Masao Utiyama, Chenchen Ding. (2016) 'Introduction of the Asian Language Treebank' Oriental COCOSDA.",
            "homepage": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/",
            "tags": ["machine translation"],
        },
        "files": [
            {
                "filename": "ALT-Parallel-Corpus-20191206.zip",
                "url": "https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/ALT-Parallel-Corpus-20191206.zip",
                "is_large": True,
                "extract": True,
            }
        ],
        "reader": {
            **{
                lang: {
                    "path": os.path.join("ALT-Parallel-Corpus-20191206", f"data_{lang}.txt"),
                    "is_table": True,
                    "reader": txt_table_reader,
                    "args": {"header": False},
                }
                # fmt: off
                for lang in ["my", "khm", "lo", "bg", "th", "hi", "vi",
                             "ja", "fil", "ms", "id", "en", "en_tok", "zh"]
                # fmt: on
            },
            "URL": {
                "path": os.path.join("ALT-Parallel-Corpus-20191206", "URL.txt"),
                "is_table": True,
                "reader": txt_table_reader,
                "args": {"header": False},
            },
        },
    },
}
