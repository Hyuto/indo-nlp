import csv
import json
from typing import Any, Dict, List

__all__ = ["csv_reader", "txt_table_reader", "jsonl_table_reader"]


def csv_reader(
    path: str,
    fd_kwargs: Dict[str, Any] = {},
    reader_kwargs: Dict[str, Any] = {},
) -> Dict[str, List[Any]]:
    """csv file reader dimana data yang dikembalikan dapat langsung di pass kedalam
    `pandas.DataFrame` untuk melihat data dalam versi tablenya.

    Args:
        path (str): Path ke file csv.
        fd_kwargs (Dict[str, Any], optional): File opener kwargs.
        reader_kwargs (Dict[str, Any], optional): Reader kwargs.

    Returns:
        Data yang siap digunakan.
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
    r"""txt file reader dimana data yang dikembalikan dapat langsung di pass kedalam
    `pandas.DataFrame` untuk melihat data dalam versi tablenya.

    Args:
        path (str): Path ke file txt.
        header (bool, optional): Apakah data memiliki header, jika `True` diberikan maka baris
            pertama dari data akan dianggap sebagai header.
        delimiter (str, optional): Delimiter (pemisah).
        fd_kwargs (Dict[str, Any], optional): File opener kwargs.

    Returns:
        Data yang siap digunakan.
    """

    if header:
        return csv_reader(path, fd_kwargs, reader_kwargs={"delimiter": delimiter})

    with open(path, **fd_kwargs) as fd:
        read_data = fd.readlines()
        head = read_data[0][:-1].split(delimiter)
        head = list(range(len(head)))

    return csv_reader(path, fd_kwargs, reader_kwargs={"fieldnames": head, "delimiter": delimiter})


def jsonl_table_reader(
    path: str,
    fd_kwargs: Dict[str, Any] = {},
    reader_kwargs: Dict[str, Any] = {},
) -> Dict[str, List[Any]]:
    """Symmetric jsonl file reader dimana data yang dikembalikan dapat langsung di pass kedalam
    `pandas.DataFrame` untuk melihat data dalam versi tablenya.

    Args:
        path (str): Path ke jsonl file.
        fd_kwargs (Dict[str, Any], optional): File opener kwargs.
        reader_kwargs (Dict[str, Any], optional): Reader kwargs.

    Returns:
        Data yang siap digunakan.
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
