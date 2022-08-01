import json
import logging
import os
import sys
from shutil import get_terminal_size
from typing import Any, Dict, Optional

__all__ = ["logger", "sizeof_fmt", "_progress_bar", "_progress_text", "DatasetDirectoryHandler"]


def _setup_logger() -> logging.Logger:
    """Setup indoNLP dataset logger"""
    logger = logging.getLogger("indoNLP")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[ %(levelname)s ] %(name)s:%(funcName)s - %(message)s")

    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = _setup_logger()


def sizeof_fmt(num: int) -> str:
    """Make readable filesize

    Args:
        num (int): filesize in Bytes

    Returns:
        str: readable filesize
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024:
            return f"{num:.2f} {unit}B"
        num /= 1024  # type: ignore
    return f"{num:.2f} YiB"


def _progress_text(filename: str, downloaded: int, last: bool = False) -> None:
    """Text progressing while downloading dataset

    Args:
        filename (str): filename
        downloaded (int): downloaded buffer
        last (bool, optional): last print. Defaults to False.
    """
    simplified_downloaded = sizeof_fmt(downloaded)
    template = f"   Downloading : {filename} [{simplified_downloaded}]"
    if not last:
        print(template, end="\r", file=sys.stdout, flush=True)
    if last:
        terminal_width, _ = get_terminal_size((80, 20))
        print(" " * terminal_width, end="\r", file=sys.stdout, flush=True)
        print(f"   📖 {filename} saved [{simplified_downloaded}]")


def _progress_bar(filename: str, downloaded: int, total_size: int) -> None:
    """Bar progressing while downloading dataset

    Args:
        filename (str): filename
        downloaded (int): downloaded buffer
        total_size (int): filesize
    """
    simplified_downloaded = sizeof_fmt(downloaded)
    simplified_total_size = sizeof_fmt(total_size)

    # get progressbar width
    terminal_width, _ = get_terminal_size((80, 20))
    width = terminal_width - (len(filename) + len(simplified_total_size) * 2 + 23)
    width = width if width <= 70 else 70

    progress = int(width * downloaded / total_size)
    template = (
        f"   Downloading : {filename} "
        + f"[{'█' * progress}{('.' * (width - progress))}]"
        + f" {simplified_downloaded}/{simplified_total_size}  "
    )

    # out
    if downloaded < total_size:
        print(template, end="\r", file=sys.stdout, flush=True)
    else:
        print(" " * terminal_width, end="\r", file=sys.stdout, flush=True)
        print(f"   📖 {filename} saved [{simplified_downloaded}]")


class DatasetDirectoryHandler:
    """Handler dataset directory

    Args:
        download_dir (Optional[str]): path to main dataset directory. Defaults to None.
            if None is given dataset directory is set to ~/.cache/indoNLP
    """

    download_dir: str = os.path.join(os.path.expanduser("~"), ".cache", "indoNLP")

    def __init__(self, download_dir: Optional[str] = None) -> None:
        self.download_dir = download_dir if download_dir is not None else self.download_dir
        self.config_dir = os.path.join(self.download_dir, "config.json")
        os.makedirs(self.download_dir, exist_ok=True)

        self.handler_config = self._get_config()  # config
        self._update_config()

    def _get_config(self) -> Dict[str, Dict[str, Any]]:
        """Get configuration from file"""
        if os.path.exists(self.config_dir):
            with open(self.config_dir) as reader:
                config: Dict[str, Dict[str, Any]] = json.load(reader)
            return config
        return {}

    def _update_config(self) -> None:
        """Update configuration file"""
        with open(self.config_dir, "w") as writer:
            writer.write(json.dumps(self.handler_config, indent=4))
