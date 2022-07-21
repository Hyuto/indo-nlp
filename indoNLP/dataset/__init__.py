import os
from typing import Any, Dict, Optional, Sequence, Tuple, Union

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
    def __init__(
        self,
        name: str,
        dataset_dir: Optional[str] = None,
        auto_download: bool = True,
    ) -> None:
        if DATASETS.get(name) is None:
            raise KeyError(
                "Unknown dataset! please revere to 'indoNLP.dataset.get_supported_dataset_list' "
                + "output to see supported datasets"
            )

        self.dataset_name = name
        self.dataset_config = DATASETS[name]
        self.file = DatasetDirectoryHandler(dataset_dir)
        self.downloader = DataDownloader(self.dataset_name, self.dataset_config["files"], self.file)

        if auto_download:
            self.downloader.download()

    def _read_file(self, tag: str) -> Any:
        path = os.path.join(
            self.file.handler_config[self.dataset_name]["path"],
            self.dataset_config["reader"][tag]["path"],
        )
        return self.dataset_config["reader"][tag]["reader"](path)

    def get_info(self) -> None:
        """Get supported dataset info"""
        get_supported_dataset_info(self.dataset_name)

    def read(self, get: Union[str, Tuple[str]] = "all") -> Union[Any, Tuple[Any]]:
        assert (
            self.file.handler_config[self.dataset_name]["status"] == "completed"
        ), "Dataset isn't downloaded yet!"

        if get == "all":
            get = tuple(self.dataset_config["reader"].keys())  # type: ignore
        if type(get) == str or len(get) <= 1:
            get = get[0] if type(get) == tuple else get
            assert type(get) == str  # ensure type
            return self._read_file(get)
        return tuple(self._read_file(x) for x in get)
