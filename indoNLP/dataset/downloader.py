import os
import sys
from cgi import parse_header
from datetime import datetime
from shutil import get_terminal_size
from typing import Any, Dict, Optional, Tuple, Union
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen

from indoNLP.dataset.list import DATASETS
from indoNLP.dataset.utils import DatasetDirectoryHandler, logger, sizeof_fmt


class DataDownloader:
    """Download dataset

    Args:
        name (str): dataset name
        dataset_dir (Union[str, DatasetDirectoryHandler]): dataset main directory
    """

    def __init__(self, name: str, dataset_dir: Union[None, str, DatasetDirectoryHandler]) -> None:
        self.dataset_name = name
        self.info = DATASETS.get(name)

        if type(dataset_dir) == DatasetDirectoryHandler:
            self.file = dataset_dir
        elif type(dataset_dir) == str:
            self.file = DatasetDirectoryHandler(dataset_dir)
        else:
            raise TypeError("Unacceptable dataset_dir type!")

    def _check_config(self) -> bool:
        """Check status dataset in config"""
        if self.file.handler_config.get(self.dataset_name) is not None:
            if self.file.handler_config[self.dataset_name]["status"] == "completed":
                return True
        return False

    def _get_filename(self, response: Any, url: str) -> str:
        """Get filename from url"""
        content = response.getheader("Content-Disposition")
        if content is not None:
            _, params = parse_header(content)
            return params["filename"]
        path = urlparse(url).path
        return os.path.basename(path)

    def _get_filesize(self, response: Any) -> Union[int, None]:
        """Get filesize from url"""
        filesize: Union[int, None] = response.getheader("content-length")
        filesize = int(filesize) if filesize is not None else None
        return filesize

    def _progress_text(self, downloaded: int, last: bool = False) -> None:
        """Text progressing while downloading dataset

        Args:
            downloaded (int): downloaded buffer
            last (bool, optional): last print. Defaults to False.
        """
        simplified_downloaded = sizeof_fmt(downloaded)
        template = f"   Downloading : {self.dataset_name} [{simplified_downloaded}]"
        if not last:
            print(template, end="\r", file=sys.stdout, flush=True)
        if last:
            terminal_width, _ = get_terminal_size((80, 20))
            print(" " * terminal_width, end="\r", file=sys.stdout, flush=True)
            print(f"   📖 {self.dataset_name} saved [{simplified_downloaded}]")

    def _progress_bar(self, downloaded: int, total_size: int) -> None:
        """Bar progressing while downloading dataset

        Args:
            downloaded (int): downloaded buffer
            total_size (int): filesize
        """
        simplified_downloaded = sizeof_fmt(downloaded)
        simplified_total_size = sizeof_fmt(total_size)

        # get progressbar width
        terminal_width, _ = get_terminal_size((80, 20))
        width = terminal_width - (len(self.dataset_name) + len(simplified_total_size) * 2 + 23)
        width = width if width <= 70 else 70

        progress = int(width * downloaded / total_size)
        template = (
            f"   Downloading : {self.dataset_name} "
            + f"[{'█' * progress}{('.' * (width - progress))}]"
            + f" {simplified_downloaded}/{simplified_total_size}  "
        )

        # out
        if downloaded < total_size:
            print(template, end="\r", file=sys.stdout, flush=True)
        else:
            print(" " * terminal_width, end="\r", file=sys.stdout, flush=True)
            print(f"   📖 {self.dataset_name} saved [{simplified_downloaded}]")

    def check(self, url: Optional[str] = None) -> Dict[str, Union[str, int]]:
        """Check if data available

        Args:
            url (Optional[str]): dataset url, no need to specify for supported dataset however
                for non-supported dataset it's a must. Defaults to None.

        Returns:
            Dict[str, str]: Dataset availability
        """
        if self.info is not None:
            url = self.info["url"]
        assert url is not None, "Please specify url endpoint to download dataset"
        try:
            with urlopen(url) as response:
                pass
            return {"available": True, "status": response.status}
        except HTTPError as e:
            logger.error(e)
            return {"available": True, "status": e.code}

    def download(self, url: Optional[str] = None) -> None:
        """Download dataset

        Args:
            url (Optional[str]): dataset url, no need to specify for supported dataset however
                for non-supported dataset it's a must. Defaults to None.
        """
        if self.info is not None:
            url = self.info["url"]
        assert url is not None, "Please specify url endpoint to download dataset"
        complete = self._check_config()
        if not complete:
            self.file.handler_config[self.dataset_name] = {"status": "downloading", "path": None}
            try:
                with urlopen(url) as response:
                    filename = self._get_filename(response, url)
                    filesize = self._get_filesize(response)
                    filename = os.path.join(self.file.dataset_dir, filename)
                    with open(filename, "wb") as writer:
                        blocksize = 1000000
                        if filesize is not None:
                            blocksize = max(4096, filesize // 20)

                        size = 0
                        while True:
                            buffer = response.read(blocksize)
                            if not buffer:
                                if filesize is None:
                                    self._progress_text(size, True)
                                break
                            writer.write(buffer)
                            size += len(buffer)
                            if filesize is not None:
                                self._progress_bar(size, filesize)
                            else:
                                self._progress_text(size)

                    self.file.handler_config[self.dataset_name] = {
                        "status": "completed",
                        "path": filename,
                        "date": datetime.now().isoformat(),
                        "size": os.path.getsize(filename),
                    }
            except HTTPError as e:
                logger.error(e)
            finally:
                self.file._update_config()
        else:
            logger.info(f"Dataset {self.dataset_name} is already downloaded!")
