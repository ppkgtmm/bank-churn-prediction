from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
import numpy as np


oh_config = dict(handle_unknown="ignore", sparse=False, dtype=np.int8)


def get_feature_preprocessor(data, cat_cols, num_cols, std=True):
    num_processor = StandardScaler()
    if std == False:
        num_processor = MinMaxScaler()

    preprocessor = ColumnTransformer(
        [
            ("OH_encoder", OneHotEncoder(**oh_config), cat_cols),
            ("num_preprocessor", num_processor, num_cols),
        ]
    ).fit(data)

    col_names = (
        preprocessor.transformers_[0][1].get_feature_names_out().tolist() + num_cols
    )
    return preprocessor, col_names


def label_encode(y, classes):
    label_map = {v: k for k, v in enumerate(classes)}
    return y.map(lambda x: label_map[x])


def decode_label(y, classes):
    inverse_map = {k: v for k, v in enumerate(classes)}
    return y.map(lambda x: inverse_map[x])
