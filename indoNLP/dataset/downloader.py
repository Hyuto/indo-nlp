import os
from cgi import parse_header
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen

from indoNLP.dataset.utils import DatasetDirectoryHandler, _progress_bar, _progress_text, logger


class DataDownloader:
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
            raise TypeError("Unacceptable download_dir type!")

        self.dataset_dir = os.path.join(self.file.download_dir, self.dataset_name)
        os.makedirs(self.dataset_dir, exist_ok=True)

    def _is_downloaded(self) -> bool:
        """Check dataset in config"""
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

    def check(self) -> List[Dict[str, Union[str, int]]]:
        urls = [(x["filename"], x["url"]) for x in self.dataset_files]
        results = []
        for filename, url in urls:
            try:
                with urlopen(url) as response:
                    pass
                results.append({"filename": filename, "available": True, "status": response.status})
            except HTTPError as e:
                logger.error(e)
                results.append({"filename": filename, "available": False, "status": e.code})
        return results

    def _download(self, index: int) -> None:
        file_ = self.file.handler_config[self.dataset_name]["files"][index]
        try:
            with urlopen(file_["url"]) as response:
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
                    "status": "completed",
                    "date": datetime.now().isoformat(),
                    "size": os.path.getsize(filename),
                }
        except HTTPError as e:
            logger.error(e)
        finally:
            self.file._update_config()

    def download(self) -> None:
        if not self._is_downloaded():
            if self.file.handler_config.get(self.dataset_name) is None:
                self.file.handler_config[self.dataset_name] = {
                    "status": "downloading",
                    "path": self.dataset_dir,
                    "files": self.dataset_files,
                }
            self.file._update_config()
            for i, file_ in enumerate(self.file.handler_config[self.dataset_name]["files"]):
                status = file_.get("status")
                if status is not None or status == "completed":
                    continue
                elif status is None:
                    self.file.handler_config[self.dataset_name]["files"][i][
                        "status"
                    ] = "downloading"
                self._download(i)
            self.file.handler_config[self.dataset_name]["status"] = "completed"
            self.file._update_config()
            print(f" ✅ {self.dataset_name} downloaded")
