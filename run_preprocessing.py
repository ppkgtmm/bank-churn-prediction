from sklearn.model_selection import train_test_split
from utilities import (
    read_data,
    select_categorical_features,
    get_feature_preprocessor,
    label_encode,
    get_classes,
)

import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


data_path = "data/bank_churners.csv"
index_col = ["CLIENTNUM"]
target_col = "attrition_flag"
seed = 42
test_size = 0.15
data = read_data(data_path=data_path, index_col=index_col)
data = data.drop(columns=["avg_open_to_buy"] + list(data.columns)[-2:])

train, test = train_test_split(
    data,
    test_size=test_size,
    random_state=seed,
    stratify=data[target_col],
)

classes = get_classes(train, target_col)

y_train = pd.Series(
    label_encode(train[target_col], classes), name=target_col, index=train.index
)
y_test = pd.Series(
    label_encode(test[target_col], classes), name=target_col, index=test.index
)

X_train = train.drop(columns=[target_col])
X_test = test.drop(columns=[target_col])

cat_cols = X_train.select_dtypes(include=["object"]).columns
num_cols = X_train.select_dtypes(exclude=["object"]).columns

selected_cat = select_categorical_features(X_train, y_train, cat_cols)

preprocessor_std, cat_feat_names = get_feature_preprocessor(
    X_train, selected_cat, num_cols
)
X_train_std = preprocessor_std.transform(X_train)
X_test_std = preprocessor_std.transform(X_test)

prep_cols = list(cat_feat_names) + list(num_cols)

X_train_std = pd.DataFrame(X_train_std, columns=prep_cols, index=X_train.index)
X_test_std = pd.DataFrame(X_test_std, columns=prep_cols, index=X_test.index)

preprocessor_mm, cat_feat_names = get_feature_preprocessor(
    X_train, selected_cat, num_cols, std=False
)

X_train_mm = preprocessor_mm.transform(X_train)
X_test_mm = preprocessor_mm.transform(X_test)

prep_cols = list(cat_feat_names) + list(num_cols)

X_train_mm = pd.DataFrame(X_train_mm, columns=prep_cols, index=X_train.index)
X_test_mm = pd.DataFrame(X_test_mm, columns=prep_cols, index=X_test.index)

train_prep = pd.concat([y_train, X_train_mm], axis=1)
test_prep = pd.concat([y_test, X_test_mm], axis=1)

# print(train_prep.isna().sum())
# print(test_prep.isna().sum())

# print(train.shape, test.shape, train.columns)
# print(
#     train[target_col].value_counts(normalize=True),
#     test[target_col].value_counts(normalize=True),
# )
# print(
#     (StandardScaler().fit_transform(X_train[num_cols]) != X_train_std[num_cols])
#     .sum()
#     .sum(),
#     (MinMaxScaler().fit_transform(X_train[num_cols]) != X_train_mm[num_cols])
#     .sum()
#     .sum(),
# )
# print(X_train_std.head())
# print(X_train_mm.head())
# print(y_train)
