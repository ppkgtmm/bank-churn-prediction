from typing import List
import pandas as pd
from constants import json_orient


def get_classes(data: pd.DataFrame, column: str):
    return sorted(data[column].unique(), reverse=True)


def lower_strings(strings: List[str]):
    return [string.lower() for string in strings]


def read_data(data_path: str, index_col: list[str]):
    data = pd.read_csv(data_path, index_col=index_col)
    return data


def serialize_df(df: pd.DataFrame, orient=json_orient):
    return df.to_json(orient=orient)


def serialize_series(series: pd.Series, orient=json_orient):
    return series.to_json(orient=orient)


def deserialize_df(json_str, orient=json_orient):
    return pd.read_json(str(json_str), orient=orient)
