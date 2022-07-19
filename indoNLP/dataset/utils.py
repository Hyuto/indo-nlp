import json
import logging
import os
from typing import Dict, Optional, TypedDict, Union

__all__ = ["logger", "sizeof_fmt", "DatasetDirectoryHandler", "DatasetConfig"]


def setup_logger() -> logging.Logger:
    """Setup indoNLP dataset logger

    Returns:
        logging.Logger: logger
    """
    logger = logging.getLogger("indoNLP")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[ %(levelname)s ] %(name)s:%(funcName)s - %(message)s")

    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger()


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


HandlerConfig = TypedDict(
    "HandlerConfig",
    {
        "status": str,
        "path": Union[str, None],
        "date": str,
        "size": Union[int, None],
        "supported": bool,
    },
    total=False,
)


class DatasetDirectoryHandler:
    """Handler dataset directory

    Args:
        dataset_dir (Optional[str], optional): path to main dataset directory. Defaults to None.
            if None is given dataset directory is set to ~/.cache/indoNLP
    """

    dataset_dir: str = os.path.join(os.path.expanduser("~"), ".cache", "indoNLP")

    def __init__(self, dataset_dir: Optional[str] = None) -> None:
        self.dataset_dir = dataset_dir if dataset_dir is not None else self.dataset_dir
        self.config_dir = os.path.join(self.dataset_dir, "config.json")
        os.makedirs(self.dataset_dir, exist_ok=True)

        self.handler_config = self._get_config()  # config
        self._update_config()

    def _get_config(self) -> Dict[str, HandlerConfig]:
        """Get configuration from file"""
        if os.path.exists(self.config_dir):
            with open(self.config_dir) as reader:
                config: Dict[str, HandlerConfig] = json.load(reader)
            return config
        return {}

    def _update_config(self) -> None:
        """Update configuration file"""
        with open(self.config_dir, "w") as writer:
            writer.write(json.dumps(self.handler_config, indent=4))
