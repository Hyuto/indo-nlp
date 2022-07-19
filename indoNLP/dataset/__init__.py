from typing import Optional, Sequence

from indoNLP.dataset.downloader import DataDownloader
from indoNLP.dataset.list import DATASETS
from indoNLP.dataset.utils import DatasetDirectoryHandler


def get_supported_dataset_list(filter_tags: Optional[Sequence[str]] = None) -> None:
    """Listing all indoNLP supported dataset

    Args:
        filter_tags (Optional[Sequence[str]]): filter dataset based on tags. Defaults to None.
    """
    print("Supported Datasets")
    print("-----------------")
    count = 0
    for dataset, values in DATASETS.items():
        info = values["info"]

        if filter_tags is not None:
            assert type(info["tags"]) == set  # ensure type
            if len(info["tags"].intersection(filter_tags)) > 0:
                continue

        count += 1
        tab = " " * (len(str(count)) + 1)

        header = (
            f"{count}. {dataset}"
            + (f" - {info['author']}" if info["author"] is not None else "")
            + (f" - {info['year']}" if info["year"] is not None else "")
        )
        print(header)
        print(f"{tab} {info['description']}")
        print(f"{tab} tags : {', '.join(info['tags'])}")


def get_supported_dataset_info(name: str) -> None:
    """Get supported dataset info

    Args:
        name (str): dataset name
    """
    dataset = DATASETS.get(name)
    if dataset is not None:
        print(f"📖 {name}")
        print("-" * len(name))
        for k, v in dataset["info"].items():
            if k == "tags":
                v = ", ".join(v)
            print(f" * {k} : {v}")
    else:
        print("Dataset not found!")


class Dataset:
    def __init__(self, name: str, dataset_dir: Optional[str] = None) -> None:
        assert DATASETS.get(name) is not None, (
            "Unknown dataset! please revere to 'indoNLP.dataset.get_supported_dataset_list' "
            + "output to see supported datasets"
        )

        self.dataset_name = name
        self.dataset_config = DATASETS[name]
        self.file = DatasetDirectoryHandler(dataset_dir)
        self.downloader = DataDownloader(self.dataset_name, self.file)

    def get_info(self) -> None:
        """Get supported dataset info"""
        get_supported_dataset_info(self.dataset_name)
