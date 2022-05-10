from os.path import join
import pandas as pd
from sklearn.model_selection import train_test_split
from constants import (
    data_dir,
    data_file,
    train_fname,
    test_fname,
    val_fname,
    split_config,
    target_col,
    save_config,
    drop_col,
)
from utilities import lower_strings

data_path = join(data_dir, data_file)
train_path = join(data_dir, train_fname)
val_path = join(data_dir, val_fname)
test_path = join(data_dir, test_fname)

data = pd.read_csv(data_path)

data.drop(columns=drop_col, inplace=True)
# convert column names to lower case (easier to work with)
data.columns = lower_strings(data.columns)

train, test = train_test_split(data, **split_config, stratify=data[target_col])
train, val = train_test_split(train, **split_config, stratify=train[target_col])

train.to_csv(train_path, **save_config)
val.to_csv(val_path, **save_config)
test.to_csv(test_path, **save_config)
