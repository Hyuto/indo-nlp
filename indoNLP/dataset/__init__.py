import os
from typing import Any, Optional, Sequence, Tuple, Union

from indoNLP.dataset.downloader import DataDownloader
from indoNLP.dataset.list import DATASETS
from indoNLP.dataset.utils import DatasetDirectoryHandler

__all__ = ["get_supported_dataset_list", "get_supported_dataset_info", "Dataset"]


def get_supported_dataset_list(filter_tags: Optional[Union[str, Sequence[str]]] = None) -> None:
    """Listing all indoNLP supported dataset

    Args:
        filter_tags (Union[str, Sequence[str]], optional): Filter dataset based on tags.
            Defaults to None.
    """
    print("Supported Datasets")
    print("-----------------")
    count = 0
    for dataset, values in DATASETS.items():
        info = values["info"]

        if filter_tags is not None:
            if type(filter_tags) == str:
                filter_tags = [filter_tags]
            if not any([tag.lower() in info["tags"] for tag in filter_tags]):
                continue

        count += 1
        tab = " " * (len(str(count)) + 1)

        header = (
            f"{count}. {dataset}"
            + (f", {info['author']}" if info["author"] != "unknown" else "")
            + (f", {info['year']}" if info["year"] != "unknown" else "")
        )
        print(header)
        print(f"{tab} {info['description']}")
        print(f"{tab} tags : {', '.join(info['tags'])}")


def get_supported_dataset_info(name: str) -> None:
    """Get supported dataset info

    Args:
        name (str): Dataset name

    Raises:
        KeyError: Dataset not found (not supported dataset)
    """
    dataset = DATASETS.get(name)
    if dataset is not None:
        print(f"📖 {name}")
        print("-" * len(name))
        for k, v in dataset["info"].items():
            if k == "tags":
                v = ", ".join(v)
            print(f" * {k} : {v}")
        print(f" * files :")
        for k in dataset["reader"].keys():
            print(f"  - {k}")
    else:
        raise KeyError("Dataset not found!")


class Dataset:
    """Supported dataset handler

    Args:
        name (str): Supported dataset name
        dataset_dir (str, optional): indoNLP dataset download directory. Defaults to None.
        auto_download (bool, optional): Auto download dataset when class initiated.
            Defaults to True.

    Attributes:
        dataset_name (str): Supported dataset name
        dataset_config (Dict[str, Any]): Dataset configurations
        file (DatasetDirectoryHandler): indoNLP dataset download directory handler
        downloader (DataDownloader): indoNLP dataset downloader

    Examples:
        Download and Load supported dataset

        >>> data_handler = indoNLP.dataset.Dataset("twitter-puisi")
        >>> data_handler.read()
        ...
    """

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
        """Read dataset file"""
        handler = self.dataset_config["reader"][tag]
        path = os.path.join(
            self.file.handler_config[self.dataset_name]["path"],
            handler["path"],
        )
        return handler["reader"](path, **handler["args"])

    def get_info(self) -> None:
        """Get supported dataset info"""
        get_supported_dataset_info(self.dataset_name)  # pragma: no cover

    def read(self, get: Union[str, Tuple[str]] = "all") -> Union[Any, Tuple[Any]]:
        """Read supported dataset.

        Args:
            get (Union[str, Tuple[str]], optional): File to read, if "all" is set then all files in
                the dataset will be read and returned as tuple. Defaults to "all".

        Returns:
            Union[Any, Tuple[Any]]: Dataset, it can be a tuple if multiple file is returned.

        Examples:
            Read multiple files

            >>> data_handler = indoNLP.dataset.Dataset("asian-language-treebank-parallel-corpus")
            >>> data_id, data_ja = data_handler.read(get=("id", "ja"))
            ...
        """
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
