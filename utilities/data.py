from typing import List
import pandas as pd


def get_classes(data: pd.DataFrame, column: str):
    return sorted(data[column].unique(), reverse=True)


def lower_strings(strings: List[str]):
    return [string.lower() for string in strings]


def read_data(data_path: str, index_col: list[str]):
    data = pd.read_csv(data_path, index_col=index_col)
    return data
