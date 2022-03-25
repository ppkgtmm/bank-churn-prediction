from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
import numpy as np


oh_config = dict(handle_unknown="ignore", sparse=False, dtype=np.int8)


def get_feature_preprocessor(X, cat_cols, num_cols, std=True):
    num_processor = ("standard_scaler", StandardScaler(), num_cols)
    if not std:
        num_processor = ("min_max", MinMaxScaler(), num_cols)

    preprocessor = ColumnTransformer(
        [
            ("OH_encoder", OneHotEncoder(**oh_config), cat_cols),
            num_processor,
        ]
    ).fit(X)
    return preprocessor, preprocessor.transformers_[0][1].get_feature_names_out()


def label_encode(y, classes):
    label_map = {v: k for k, v in enumerate(classes)}
    return y.map(lambda x: label_map[x])


def invert_label(y, classes):
    inverse_map = {k: v for k, v in enumerate(classes)}
    return y.map(lambda x: inverse_map[x])
