from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
import numpy as np


oh_config = dict(handle_unknown="ignore", sparse=False, dtype=np.int8)


def get_feature_preprocessors(X, cat_cols, num_cols):
    pipe_std = ColumnTransformer(
        [
            ("OH_encoder", OneHotEncoder(**oh_config), cat_cols),
            ("standard_scaler", StandardScaler(), num_cols),
        ]
    ).fit(X)

    pipe_mm = ColumnTransformer(
        [
            ("OH_encoder", OneHotEncoder(**oh_config), cat_cols),
            ("min_max", MinMaxScaler(), num_cols),
        ]
    ).fit(X)

    return {"std": pipe_std, "min_max": pipe_mm}


def label_encode(y, classes):
    label_map = {v: k for k, v in enumerate(classes)}
    return y.map(lambda x: label_map[x])


def invert_label(y, classes):
    inverse_map = {k: v for k, v in enumerate(classes)}
    return y.map(lambda x: inverse_map[x])
