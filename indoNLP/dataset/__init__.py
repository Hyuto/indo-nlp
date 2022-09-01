"""`indoNLP.dataset` adalah modul yang bertujuan untuk memudahkan mengakses 
open dataset dalam bidang NLP untuk Bahasa Indonesia."""

import os
from typing import Any, Optional, Sequence, Tuple, Union

from indoNLP.dataset.downloader import DataDownloader
from indoNLP.dataset.list import DATASETS
from indoNLP.dataset.utils import Data, DatasetDirectoryHandler

__all__ = ["get_supported_dataset_list", "get_supported_dataset_info", "Dataset"]


def get_supported_dataset_list(filter_tags: Optional[Union[str, Sequence[str]]] = None) -> None:
    """Mendapatkan list dataset yang disupport oleh indoNLP.

    Args:
        filter_tags (Union[str, Sequence[str]], optional): Filter dataset berdasarkan tags.

    !!! info "Informasi"
        Untuk lebih lengkapnya list dataset yang disupport indoNLP dapat dilihat pada
            [Supported Dataset](./sup-dataset/).
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
    """Mendapatkan informasi terkait salah satu dataset yang disupport indoNLP.

    Args:
        name (str): Nama dataset yang dipilih.

    Raises:
        KeyError: Dataset tidak ditemukan (tidak disupport indoNLP).
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
        raise KeyError("Dataset tidak ditemukan!")


class Dataset:
    """Handler untuk dataset yang disupport indoNLP, berfungsi untuk mendownload, mengekstract, dan
    membaca data.

    Args:
        name (str): Nama dataset yang disupport indoNLP.
        dataset_dir (str, optional): indoNLP dataset download direktori.
        auto_download (bool, optional): Auto download dataset ketika kelas di inisiasi, jika dataset
            telah didownload sebelumnya maka proses download akan dilewati secara otomatis.

    Attributes:
        dataset_name (str): Nama dataset yang disupport indoNLP.
        dataset_config (Dict[str, Any]): Konfigurasi dataset.
        file (DatasetDirectoryHandler): indoNLP dataset download direktori handler.
        downloader (DataDownloader): indoNLP dataset downloader.

    Examples:
        Download dan Loading dataset yang disupport.

        >>> handler = indoNLP.dataset.Dataset("twitter-puisi")
        >>> data = handler.read()
        >>> data

        Melihat dataset secara keseluruhan.

        >>> data.data
    """

    def __init__(
        self,
        name: str,
        dataset_dir: Optional[str] = None,
        auto_download: bool = True,
    ) -> None:
        if DATASETS.get(name) is None:
            raise KeyError(
                "Dataset tidak diketahui! tolong tinjau https://hyuto.github.io/indo-nlp/api/sup-dataset/ "
                + "atau output dari `indoNLP.dataset.get_supported_dataset_list` untuk melihat dataset "
                + "yang disupport"
            )

        self.dataset_name = name
        self.dataset_config = DATASETS[name]
        self.file = DatasetDirectoryHandler(dataset_dir)
        self.downloader = DataDownloader(self.dataset_name, self.dataset_config["files"], self.file)

        if auto_download:
            self.downloader.download()

    def _read_file(self, tag: str) -> Data:
        """Membaca sebuah file di dalam dataset"""
        handler = self.dataset_config["reader"][tag]
        path = os.path.join(
            self.file.handler_config[self.dataset_name]["path"],
            handler["path"],
        )
        return Data(
            name=tag,
            data=handler["reader"](path, **handler["args"]),
            part_of=self.dataset_name,
            table=handler["is_table"],
        )

    def cite(self) -> None:
        """Mendapatkan cara mengutip dataset.

        Examples:
            >>> handler = indoNLP.dataset.Dataset("id-abusive-language-detection")
            >>> handler.cite()
            Ibrohim, M.O., Budi, I.. A Dataset and Preliminaries Study for Abusive Language Detection in Indonesian Social Media. Procedia Computer Science 2018;135:222-229.
        """
        print(self.dataset_config["info"]["citation"])  # pragma: no cover

    def get_info(self) -> None:
        """Mendapatkan informasi dari dataset.

        !!! info "Informasi"
            Menghasilkan output yang sama dengan fungsi `get_supported_dataset_info`.
        """
        get_supported_dataset_info(self.dataset_name)  # pragma: no cover

    def read(self, get: Union[str, Tuple[str]] = "all") -> Union[Data, Tuple[Data, ...]]:
        """Membaca file yang terdapat dalam dataset dan meloadnya kedalam memori. Jika data yang
        terdapat dalam file adalah simetric maka data dapat diload dengan menggunakan
        `pandas.DataFrame`.

        Args:
            get (Union[str, Tuple[str]], optional): Nama file di dalam dataset untuk dibaca dan
                diload kedalam memori, jika "all" diset maka akan dibaca semua file yang ada di
                dalam dataset.

        Returns:
            Data dari file yang telah di read. Jika file yang dibaca berjumlah lebih dari 2 maka
                akan mengembalikan dalam bentuk Tuple sesuai dengan urutan nama file yang
                dispesifikasikan pada parameter `get`, jika "all" yang diberikan maka urutan data dari
                file akan sesuai dengan urutan yang ada pada metode `get_info()`.

        Examples:
            Membaca dan loading sebuah file.

            >>> handler = indoNLP.dataset.Dataset("twitter-puisi")
            >>> puisi = handler.read()

            ??? info "twitter-puisi"
                twitter-puisi dataset hanya memiliki 1 file didalamnya.

            Membaca beberapa file.

            >>> handler = indoNLP.dataset.Dataset("asian-language-treebank-parallel-corpus")
            >>> data_id, data_ja = handler.read(get=("id", "ja"))

            ??? info "asian-language-treebank-parallel-corpus"
                asian-language-treebank-parallel-corpus dataset memiliki banyak file didalamnya.
        """
        assert (
            self.file.handler_config[self.dataset_name]["status"] == "completed"
        ), "Dataset isn't downloaded yet!"

        if get == "all":
            get = tuple(self.dataset_config["reader"].keys())  # type: ignore
        if type(get) == str or len(get) <= 1:
            get = get if type(get) == str else get[0]
            assert type(get) == str  # ensure type
            return self._read_file(get)
        return tuple(self._read_file(x) for x in get)
