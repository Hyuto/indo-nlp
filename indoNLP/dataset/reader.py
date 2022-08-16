import csv
import json
from typing import Any, Dict, List

__all__ = ["csv_reader", "txt_table_reader", "jsonl_table_reader"]


def csv_reader(
    path: str,
    fd_kwargs: Dict[str, Any] = {},
    reader_kwargs: Dict[str, Any] = {},
) -> Dict[str, List[Any]]:
    """csv file reader where returned data can be read into pandas.DataFrame

    Args:
        path (str): Path to csv file
        fd_kwargs (Dict[str, Any], optional): File opener kwargs. Defaults to {}.
        reader_kwargs (Dict[str, Any], optional): Reader kwargs. Defaults to {}.

    Returns:
        Dict[str, List[Any]]: Ready to use dataset
    """
    with open(path, **fd_kwargs) as fd:
        reader = csv.DictReader(fd, **reader_kwargs)
        header = reader.fieldnames
        assert header is not None  # ensure type
        data: Dict[str, List[Any]] = {c: [] for c in header}
        for row in reader:
            for k, v in row.items():
                data[k].append(v)
    return data


def txt_table_reader(
    path: str,
    header: bool = True,
    delimiter: str = "\t",
    fd_kwargs: Dict[str, Any] = {},
) -> Dict[str, List[Any]]:
    r"""txt file reader where returned data can be read into pandas.DataFrame

    Args:
        path (str): Path to csv file
        header (bool, optional): Is header included?. Defaults to True
        delimiter (str, optional): Delimiter. Defaults to '\t'
        fd_kwargs (Dict[str, Any], optional): File opener kwargs. Defaults to {}.

    Returns:
        Dict[str, List[Any]]: Ready to use dataset
    """
    with open(path, **fd_kwargs) as fd:
        read_data = fd.readlines()
    if header:
        head = read_data.pop(0)[:-1].split(delimiter)
    else:
        head = read_data[0][:-1].split(delimiter)
        head = list(range(len(head)))

    data: Dict[str, List[Any]] = {c: [] for c in head}
    for row in read_data:
        row_data = row[:-1].split(delimiter)
        for k, v in zip(head, row_data):
            data[k].append(v)
    return data


def jsonl_table_reader(
    path: str,
    fd_kwargs: Dict[str, Any] = {},
    reader_kwargs: Dict[str, Any] = {},
) -> Dict[str, List[Any]]:
    """Symmetric jsonl file reader where returned data can be read into pandas.DataFrame

    Args:
        path (str): Path to jsonl file
        fd_kwargs (Dict[str, Any], optional): File opener kwargs. Defaults to {}.
        reader_kwargs (Dict[str, Any], optional): Reader kwargs. Defaults to {}.

    Returns:
        Dict[str, List[Any]]: Ready to use dataset
    """
    with open(path, **fd_kwargs) as reader:
        data = reader.read().splitlines()
    columns = json.loads(data[0], **reader_kwargs).keys()
    transformed_data: Dict[str, List[Any]] = {c: [] for c in columns}
    for line in data:
        line_data = json.loads(line)
        for key, val in line_data.items():
            transformed_data[key].append(val)
    return transformed_data
