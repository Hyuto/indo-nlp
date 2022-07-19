import json
from typing import Any, Dict, List


def jsonl_table_reader(path: str) -> Dict[str, List[Any]]:
    """Symmetric jsonl file reader where returned data can be read into pandas DataFrame

    Args:
        path (str): path to jsonl file

    Returns:
        Dict[str, List[Any]]: dataset
    """
    with open(path) as reader:
        data = reader.read().splitlines()
    columns = json.loads(data[0]).keys()
    transformed_data: Dict[str, List[Any]] = {c: [] for c in columns}
    for line in data:
        line_data = json.loads(line)
        for key, val in line_data.items():
            transformed_data[key].append(val)
    return transformed_data
