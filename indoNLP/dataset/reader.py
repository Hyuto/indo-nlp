import csv
import json
from typing import Any, Dict, List


def csv_reader(
    path: str,
    fd_kwargs: Dict[str, Any] = {},
    reader_kwargs: Dict[str, Any] = {},
) -> Dict[str, List[Any]]:
    """csv file reader where returned data can be read into pandas.DataFrame

    Args:
        path (str): path to csv file
        fd_kwargs (Dict[str, Any], optional): file opener kwargs. Defaults to {}.
        reader_kwargs (Dict[str, Any], optional): reader kwargs. Defaults to {}.

    Returns:
        Dict[str, List[Any]]: dataset
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


def jsonl_table_reader(
    path: str,
    fd_kwargs: Dict[str, Any] = {},
    reader_kwargs: Dict[str, Any] = {},
) -> Dict[str, List[Any]]:
    """Symmetric jsonl file reader where returned data can be read into pandas.DataFrame

    Args:
        path (str): path to jsonl file
        fd_kwargs (Dict[str, Any], optional): file opener kwargs. Defaults to {}.
        reader_kwargs (Dict[str, Any], optional): reader kwargs. Defaults to {}.

    Returns:
        Dict[str, List[Any]]: dataset
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
