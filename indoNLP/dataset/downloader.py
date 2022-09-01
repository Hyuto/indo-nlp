import os
import shutil
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from urllib.error import HTTPError

from indoNLP.dataset.utils import DatasetDirectoryHandler, _progress_bar, _progress_text, logger

__all__ = ["DataDownloader"]


class DataDownloader:
    """Dataset downloader, berfungsi untuk mendownload dan mengekstrak data secara langsung.
    Dapat digunakan untuk mendownload data yang tidak disupport oleh `indoNLP` dengan beberapa
    konfigurasi tambahan.

    Args:
        name (str): Nama dataset.
        files (List[Dict[str, str]]): List dari file - file yang terdapat pada dataset. Dictionary
            data harus mengandung elemen "filename" (str), "url" (str), dan "extract" (bool) agar
            proses dapat berjalan dengan baik.
        download_dir (Union[str, DatasetDirectoryHandler], optional): indoNLP dataset download
            direktori handler.

    Attributes:
        dataset_name (str): Nama dataset.
        dataset_files (List[Dict[str, str]]): List dari file - file yang terdapat pada dataset.
        file (DatasetDirectoryHandler): indoNLP dataset download direktori handler.
        dataset_dir (str): Direktori tempat dataset didownload.

    Examples:
        Mendownload data yang tidak disupport oleh `indoNLP`.

        >>> downloader = indoNLP.dataset.downloader.DataDownloader(
        ...    "msa-all-tab",
        ...    files=[
        ...        {
        ...            "filename": "Bahasa-Wordnet-master.zip",
        ...            "url": "https://codeload.github.com/limaginaire/Bahasa-Wordnet/zip/refs/heads/master",
        ...            "is_large": True,
        ...            "extract": True,
        ...        }
        ...    ],
        ...    download_dir="temp",
        ...)
        >>> downloader.download()
    """

    def __init__(
        self,
        name: str,
        files: List[Dict[str, str]],
        download_dir: Optional[Union[str, DatasetDirectoryHandler]] = None,
    ) -> None:
        self.dataset_name = name
        self.dataset_files = files

        if type(download_dir) == DatasetDirectoryHandler:
            self.file = download_dir
        elif type(download_dir) == str or download_dir is None:
            self.file = DatasetDirectoryHandler(download_dir)
        else:
            raise TypeError("Unacceptable download_dir type!")  # pragma: no cover

        self.dataset_dir = os.path.join(self.file.download_dir, self.dataset_name)
        os.makedirs(self.dataset_dir, exist_ok=True)

    def _is_completed(self) -> bool:
        """Mengecek konfigurasi dataset"""
        if self.file.handler_config.get(self.dataset_name) is not None:
            if self.file.handler_config[self.dataset_name]["status"] == "completed":
                return True
        return False

    def _get_filesize(self, response: Any) -> Union[int, None]:
        """Mendapatkan ukuran file dari endpoint url"""
        filesize: Union[int, None] = response.getheader("content-length")
        filesize = int(filesize) if filesize is not None else None
        return filesize

    def _download(self, index: int) -> None:
        """Mendownload sebuah file.

        Args:
            index (int): Index file tersebut pada dataset files.
        """
        file_ = self.file.handler_config[self.dataset_name]["files"][index]
        file_["status"] = "downloading"
        try:
            with urllib.request.urlopen(file_["url"]) as response:
                filesize = self._get_filesize(response)
                filename = os.path.join(self.dataset_dir, file_["filename"])
                with open(filename, "wb") as writer:
                    blocksize = 1000000  # default blocksize
                    if filesize is not None:
                        blocksize = max(4096, filesize // 20)
                    downloaded_size = 0
                    while True:
                        buffer = response.read(blocksize)
                        if not buffer:
                            if filesize is None:
                                _progress_text(file_["filename"], downloaded_size, True)
                            break
                        writer.write(buffer)
                        downloaded_size += len(buffer)
                        if filesize is not None:
                            _progress_bar(file_["filename"], downloaded_size, filesize)
                        else:
                            _progress_text(file_["filename"], downloaded_size)

                self.file.handler_config[self.dataset_name]["files"][index] = {
                    **self.file.handler_config[self.dataset_name]["files"][index],
                    "status": "downloaded",
                    "date": datetime.now().isoformat(),
                    "size": os.path.getsize(filename),
                }
        except HTTPError as e:  # pragma: no cover
            logger.error(e)
        finally:
            self.file._update_config()

    def _extract_file(self, index: int) -> None:
        """Ekstraksi file yang telah didownload.

        Args:
            index (int): Index file tersebut pada dataset files.

        Note:
            Proses ini hanya akan berlangsung jika `extract=True` diberikan pada dataset dictionary
            di parameter `files`.
        """
        file_ = self.file.handler_config[self.dataset_name]["files"][index]
        file_["status"] = "extracting"
        try:
            filename = os.path.join(self.dataset_dir, file_["filename"])
            shutil.unpack_archive(filename, self.dataset_dir)
            self.file.handler_config[self.dataset_name]["files"][index]["status"] = "extracted"
        except Exception as e:
            logger.error(e)
        finally:
            self.file._update_config()

    def check(self) -> List[Dict[str, Union[str, int]]]:
        """Melakukan pengecekan apakah dataset masih tersedia pada url yang diberikan.

        Returns:
            List status ketersediaan dari file - file di dataset. (status code)

        Examples:
            Mengecek ketersediaan dataset yang tidak disupport `indoNLP` di internet.

            >>> downloader = indoNLP.dataset.downloader.DataDownloader(
            ...    "msa-all-tab",
            ...    files=[
            ...        {
            ...            "filename": "Bahasa-Wordnet-master.zip",
            ...            "url": "https://codeload.github.com/limaginaire/Bahasa-Wordnet/zip/refs/heads/master",
            ...            "is_large": True,
            ...            "extract": True,
            ...        }
            ...    ],
            ...    download_dir="temp",
            ...)
            >>> downloader.check()
            [{"filename": "Bahasa-Wordnet-master.zip", "available": True, "status": 200}]
        """
        urls = [(x["filename"], x["url"]) for x in self.dataset_files]
        results = []
        for filename, url in urls:
            try:
                with urllib.request.urlopen(url) as response:
                    pass
                results.append({"filename": filename, "available": True, "status": response.status})
            except HTTPError as e:  # pragma: no cover
                logger.error(e)
                results.append({"filename": filename, "available": False, "status": e.code})
        return results

    def download(self) -> None:
        """Mendownload dataset, proses ini dilakukan dengan mengiterasi setiap file yang ada
        di dalam dataset untuk di download. Proses ini termasuk dengan proses ekstraksi ketika
        file telah selesai di download dan `extract=True` terdapat pada dataset dictionary di
        parameter `files`.

        !!! note
            Proses ini hanya akan berjalan jika file - file dalam dataset belum pernah didownload
            sebelumnya.
        """
        if not self._is_completed():
            if self.file.handler_config.get(self.dataset_name) is None:
                self.file.handler_config[self.dataset_name] = {
                    "status": "downloading",
                    "path": self.dataset_dir,
                    "files": self.dataset_files,
                }
                self.file._update_config()
            for i, file_ in enumerate(self.file.handler_config[self.dataset_name]["files"]):
                status = file_.get("status")
                if status == "completed":  # pragma: no cover
                    continue
                elif status == "extracting" and file_["extract"]:  # pragma: no cover
                    self._extract_file(i)
                    self.file.handler_config[self.dataset_name]["files"][i]["status"] = "completed"
                    continue
                self._download(i)
                if file_["extract"]:
                    self._extract_file(i)
                self.file.handler_config[self.dataset_name]["files"][i]["status"] = "completed"
            self.file.handler_config[self.dataset_name]["status"] = "completed"
            self.file._update_config()
            print(f" ✅ {self.dataset_name} ready")
