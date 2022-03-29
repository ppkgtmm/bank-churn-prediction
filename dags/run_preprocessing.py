import os
from datetime import datetime
from constants import *
import pandas as pd
from utilities.data import (
    get_classes,
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
index_column = index_col.lower()

default_args = dict(
    owner="airflow",
    start_date=datetime(2022, 1, 1),
    depends_on_past=False,
    email_on_failure=False,
    email_on_retry=False,
    schedule_interval="@daily",
    max_active_runs=1,  # no concurrent runs
    catchup=False,
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
    data = pd.read_csv(data_path)

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
    cat_cols = (
        features.set_index(index_column).select_dtypes(include=["object"]).columns
    )

    return select_categorical_features(features, target, cat_cols)


def preprocess_feature_wrapper(ti, **kwargs):
    cat_cols = ti.xcom_pull(task_ids=select_features_task_id)
    train = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=train_set_key))
    test = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=test_set_key))

    num_cols = list(
        train.drop(columns=[target_col])
        .set_index(index_column)
        .select_dtypes(exclude=["object"])
        .columns
    )

    preprocessor, col_names = get_feature_preprocessor(
        train, cat_cols, num_cols, kwargs.get("std")
    )

    out_file_name = os.path.join(kwargs.get("out_dir", ""), preprocessor_fname)
    with open(out_file_name, "wb") as out_file:
        pickle.dump(preprocessor, out_file)

    X_train_prep = pd.DataFrame(preprocessor.transform(train), columns=col_names)
    X_test_prep = pd.DataFrame(preprocessor.transform(test), columns=col_names)

    X_train_prep[index_column] = train[index_column].values
    X_test_prep[index_column] = test[index_column].values

    ti.xcom_push(key=kwargs.get("train_key"), value=serialize_df(X_train_prep))
    ti.xcom_push(key=kwargs.get("test_key"), value=serialize_df(X_test_prep))


def preprocess_target_wrapper(ti):
    train = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=train_set_key))
    test = deserialize_df(ti.xcom_pull(task_ids=split_data_task_id, key=test_set_key))
    classes = get_classes(train, target_col)

    df_cols = [target_col]
    y_train_prep = pd.DataFrame(
        label_encode(train[target_col], classes), columns=df_cols
    )
    y_test_prep = pd.DataFrame(label_encode(test[target_col], classes), columns=df_cols)
    ti.xcom_push(key=prep_label_train_key, value=serialize_df(y_train_prep))
    ti.xcom_push(key=prep_label_test_key, value=serialize_df(y_test_prep))


def save_data(X, y, out_dir, f_name):
    index_cols = [index_column]
    out_name = os.path.join(out_dir, f_name)
    feature_cols = list(X.drop(columns=index_cols).columns)
    out = X
    out[target_col] = y.values
    # make data same format as original
    out = X[index_cols + [target_col] + feature_cols]
    out.to_csv(out_name, index=False)


def save_data_wrapper(ti, **kwargs):
    feat_prep_task_id = kwargs.get("feat_prep_task_id")

    X_train = deserialize_df(
        ti.xcom_pull(task_ids=feat_prep_task_id, key=kwargs.get("train_key"))
    )
    y_train = deserialize_df(
        ti.xcom_pull(task_ids=preprocess_target_task_id, key=prep_label_train_key)
    )

    save_data(X_train, y_train, kwargs.get("out_dir", ""), train_fname)
    # train_out_name = os.path.join(kwargs.get("out_dir", ""), train_fname)
    # pd.concat([y_train, X_train], axis=1).to_csv(
    #     train_out_name, index_label=index_column
    # )

    X_test = deserialize_df(
        ti.xcom_pull(task_ids=feat_prep_task_id, key=kwargs.get("test_key"))
    )
    y_test = deserialize_df(
        ti.xcom_pull(task_ids=preprocess_target_task_id, key=prep_label_test_key)
    )

    save_data(X_test, y_test, kwargs.get("out_dir", ""), test_fname)
    # test_out_name = os.path.join(kwargs.get("out_dir", ""), test_fname)
    # pd.concat([y_test, X_test], axis=1).to_csv(test_out_name, index_label=index_column)


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
