import pandas as pd


def get_classes(data: pd.DataFrame, column: str):
    return sorted(data[column].unique(), reverse=True)


def read_data(data_path: str, index_col: list[str]):
    data = pd.read_csv(data_path, index_col=index_col)
    # convert column names to lower case
    data.columns = list(
        map(lambda col: col.lower(), data.columns)
    )  # easier to work with
    return data
