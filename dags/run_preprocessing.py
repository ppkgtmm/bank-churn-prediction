import os
from datetime import datetime
from constants import *
import pandas as pd
from utilities.data import (
    read_data,
    lower_strings,
    serialize_df,
    deserialize_df,
    serialize_series,
)
from utilities.feature_selection import select_categorical_features
from utilities.preprocess import get_feature_preprocessor, label_encode
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from sklearn.model_selection import train_test_split
import pickle

project_root = os.path.abspath(".")

default_args = dict(
    owner="airflow",
    start_date=datetime(2022, 1, 1),
    depends_on_past=False,
    email_on_failure=False,
    email_on_retry=False,
    schedule_interval="@daily",
    max_active_runs=1,  # no concurrent runs
)
std_kwargs = dict(
    train_key=prep_std_train_key,
    test_key=prep_std_test_key,
    # columns_key=columns_key_std,
    out_dir=std_out_dir,
)
mm_kwargs = dict(
    train_key=prep_mm_train_key,
    test_key=prep_mm_test_key,
    # columns_key=columns_key_mm,
    out_dir=minmax_out_dir,
)


def read_data_wrapper():
    data = read_data(data_path, index_col)

    data.drop(columns=drop_col, inplace=True)

    # convert column names to lower case (easier to work with)
    data.columns = lower_strings(data.columns)

    return serialize_df(data)


def split_data_wrapper(ti):
    data = deserialize_df(ti.xcom_pull(task_ids=read_data_task_id))

    train, test = train_test_split(
        data,
        test_size=test_size,
        random_state=seed,
        stratify=data[target_col],
    )

    ti.xcom_push(key=train_set_key, value=serialize_df(train))
    ti.xcom_push(key=test_set_key, value=serialize_df(test))


def select_categorical_features_wrapper(ti):
    train = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=train_set_key))

    features, target = train.drop(columns=[target_col]), train[target_col]
    cat_cols = features.select_dtypes(include=["object"]).columns

    return select_categorical_features(features, target, cat_cols)


def preprocess_feature_wrapper(ti, **kwargs):
    cat_cols = ti.xcom_pull(task_ids=select_features_task_id)
    train = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=train_set_key))
    test = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=test_set_key))

    num_cols = list(
        train.drop(columns=[target_col]).select_dtypes(exclude=["object"]).columns
    )

    preprocessor, col_names = get_feature_preprocessor(
        train, cat_cols, num_cols, kwargs.get("std")
    )

    out_file_name = os.path.join(kwargs.get("out_dir", ""), preprocessor_fname)
    with open(out_file_name, "wb") as out_file:
        pickle.dump(preprocessor, out_file)

    X_train_prep = pd.DataFrame(
        preprocessor.transform(train), index=train.index, columns=col_names
    )
    X_test_prep = pd.DataFrame(
        preprocessor.transform(test), index=test.index, columns=col_names
    )

    ti.xcom_push(key=kwargs.get("train_key"), value=serialize_df(X_train_prep))
    ti.xcom_push(key=kwargs.get("test_key"), value=serialize_df(X_test_prep))


def preprocess_target_wrapper(ti):
    train = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=train_set_key))
    test = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=test_set_key))

    ti.xcom_push(
        key=prep_label_train_key,
        value=serialize_series(label_encode(train[target_col])),
    )
    ti.xcom_push(
        key=prep_label_test_key, value=serialize_series(label_encode(test[target_col]))
    )


def save_data_wrapper(ti, **kwargs):
    feat_prep_task_id = kwargs.get("feat_prep_task_id")

    X_train = deserialize_df(
        ti.xcom_pull(task_ids=feat_prep_task_id, key=kwargs.get("train_key"))
    )
    y_train = deserialize_df(
        ti.xcom_pull(task_ids=preprocess_target_task_id, key=prep_label_train_key)
    )

    train_out_name = os.path.join(kwargs.get("out_dir", ""), train_fname)
    pd.concat([y_train, X_train], axis=1).reset_index().to_csv(
        train_out_name, index=False
    )

    X_test = deserialize_df(
        ti.xcom_pull(task_ids=feat_prep_task_id, key=kwargs.get("test_key"))
    )
    y_test = deserialize_df(
        ti.xcom_pull(task_ids=preprocess_target_task_id, key=prep_label_test_key)
    )
    test_out_name = os.path.join(kwargs.get("out_dir", ""), test_fname)
    pd.concat([y_test, X_test], axis=1).reset_index().to_csv(test_out_name, index=False)


with DAG(
    "preprocessing_dag",
    default_args=default_args,
    catchup=False,  # to not auto run dag
) as dag:
    read_data_task = PythonOperator(
        task_id=read_data_task_id,
        python_callable=read_data_wrapper,
    )
    split_data_task = PythonOperator(
        task_id=split_data_task_id, python_callable=split_data_wrapper
    )
    select_features_task = PythonOperator(
        task_id=select_features_task_id,
        python_callable=select_categorical_features_wrapper,
    )
    create_dir_std_task = BashOperator(
        task_id=std_dir_task_id,
        bash_command="cd {} && mkdir -p {}".format(project_root, std_out_dir),
    )
    create_dir_mm_task = BashOperator(
        task_id=minmax_dir_task_id,
        bash_command="cd {} && mkdir -p {}".format(project_root, minmax_out_dir),
    )
    preprocess_std_task = PythonOperator(
        task_id=preprocess_std_task_id,
        python_callable=preprocess_feature_wrapper,
        op_kwargs=std_kwargs,
    )
    preprocess_minmax_task = PythonOperator(
        task_id=preprocess_minmax_task_id,
        python_callable=preprocess_feature_wrapper,
        op_kwargs=dict(std=False, **mm_kwargs),
    )
    preprocess_target_task = PythonOperator(
        task_id=preprocess_target_task_id,
        python_callable=preprocess_target_wrapper,
    )
    save_std_task = PythonOperator(
        task_id=std_save_task_id,
        python_callable=save_data_wrapper,
        op_kwargs=dict(feat_prep_task_id=preprocess_std_task_id, **std_kwargs),
    )
    save_minmax_task = PythonOperator(
        task_id=minmax_save_task_id,
        python_callable=save_data_wrapper,
        op_kwargs=dict(feat_prep_task_id=preprocess_minmax_task_id, **mm_kwargs),
    )
    # need to add sqlite connection in airflow UI (host = path to db file)
    delete_xcom_task = SqliteOperator(
        task_id=delete_xcom_task_id,
        sqlite_conn_id=sqlite_conn_id,
        sql=delete_xcom_sql.format(dag.dag_id),
    )

    (
        read_data_task
        >> split_data_task
        >> preprocess_target_task
        >> select_features_task
        >> [create_dir_std_task, create_dir_mm_task]
    )
    create_dir_std_task >> preprocess_std_task >> save_std_task
    create_dir_mm_task >> preprocess_minmax_task >> save_minmax_task
    [save_std_task, save_minmax_task] >> delete_xcom_task
