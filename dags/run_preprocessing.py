import os
import shutil
from datetime import datetime
from constants import *
import pandas as pd
from utilities.data import (
    get_classes,
    lower_strings,
)
from utilities.feature_selection import select_categorical_features
from utilities.preprocess import get_feature_preprocessor, label_encode
from airflow import DAG
from airflow.operators.python import get_current_context
from airflow.operators.python_operator import PythonOperator
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
    catchup=False,  # to not auto run dag
)


def get_file_name(dir_path: str, file_path: str):
    return f"{dir_path}/{file_path.split('/')[-1]}"


def get_out_path(out_dir: str, file_name: str):
    return "{}/{}/{}".format(project_root, out_dir, file_name)


def get_xcom_values(task_ids):
    return get_current_context()["ti"].xcom_pull(task_ids=task_ids)


def create_temp_dir():
    temp_dir_name = f"{project_root}/temp_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    os.makedirs(temp_dir_name)

    return temp_dir_name


def read_data():
    data = pd.read_csv(data_path)

    data.drop(columns=drop_col, inplace=True)
    # convert column names to lower case (easier to work with)
    data.columns = lower_strings(data.columns)

    temp_file_path = get_file_name(get_xcom_values(temp_dir_task_id), data_path)
    data.to_csv(temp_file_path, index=False)

    return temp_file_path


def split_data():
    temp_dir_name = get_xcom_values(temp_dir_task_id)
    temp_file_path = get_xcom_values(read_data_task_id)
    data = pd.read_csv(temp_file_path)

    train, test = train_test_split(
        data,
        test_size=test_size,
        random_state=seed,
        stratify=data[target_col],
    )

    temp_train_path = get_file_name(temp_dir_name, train_fname)
    temp_test_path = get_file_name(temp_dir_name, test_fname)
    train.to_csv(temp_train_path, index=False)
    test.to_csv(temp_test_path, index=False)

    return {"train": temp_train_path, "test": temp_test_path}


def select_features():
    temp_train_path = get_xcom_values(split_data_task_id)["train"]
    train = pd.read_csv(temp_train_path, index_col=index_column)

    features, target = train.drop(columns=[target_col]), train[target_col]
    cat_cols = features.select_dtypes(include=["object"]).columns.tolist()

    return select_categorical_features(features, target, cat_cols)


def create_output_dir(out_dir: str):
    os.makedirs("{}/{}".format(project_root, out_dir), exist_ok=True)


def create_preprocessor(out_dir: str, std=True):
    cat_features = get_xcom_values(select_features_task_id)
    split_path = get_xcom_values(split_data_task_id)
    train = pd.read_csv(split_path["train"], index_col=[index_column])

    num_cols = (
        train.drop(columns=[target_col])
        .select_dtypes(exclude=["object"])
        .columns.tolist()
    )
    preprocessor, col_names = get_feature_preprocessor(
        train, cat_features, num_cols, std
    )

    with open(get_out_path(out_dir, preprocessor_fname), "wb") as out_file:
        pickle.dump(preprocessor, out_file)

    return col_names


def preprocess(out_dir: str, create_prep_task_id: str):
    index_cols = [index_column]
    split_path = get_xcom_values(split_data_task_id)
    col_names = get_xcom_values(create_prep_task_id)

    train = pd.read_csv(split_path["train"], index_col=index_cols)
    test = pd.read_csv(split_path["test"], index_col=index_cols)

    train_out = pd.DataFrame(train.index.values, columns=index_cols)
    test_out = pd.DataFrame(test.index.values, columns=index_cols)

    classes = get_classes(train, target_col)
    train_out[target_col] = label_encode(train[target_col], classes).values
    test_out[target_col] = label_encode(test[target_col], classes).values

    with open(get_out_path(out_dir, preprocessor_fname), "rb") as in_file:
        preprocessor = pickle.load(in_file)

    train_out[col_names] = preprocessor.transform(train)
    test_out[col_names] = preprocessor.transform(test)

    train_out.to_csv(get_out_path(out_dir, train_fname), index=False)
    test_out.to_csv(get_out_path(out_dir, test_fname), index=False)


def remove_temp_dir():
    temp_dir_name = get_xcom_values(temp_dir_task_id)
    shutil.rmtree(temp_dir_name)


dag = DAG(
    "preprocessing_dag",
    default_args=default_args,
)

create_temp_dir_task = PythonOperator(
    task_id=temp_dir_task_id, python_callable=create_temp_dir, dag=dag
)

read_data_task = PythonOperator(
    task_id=read_data_task_id, python_callable=read_data, dag=dag
)

split_data_task = PythonOperator(
    task_id=split_data_task_id, python_callable=split_data, dag=dag
)

select_features_task = PythonOperator(
    task_id=select_features_task_id, python_callable=select_features, dag=dag
)

create_std_dir_task = PythonOperator(
    task_id=std_dir_task_id,
    python_callable=create_output_dir,
    op_args=[std_out_dir],
    dag=dag,
)

create_minmax_dir_task = PythonOperator(
    task_id=minmax_dir_task_id,
    python_callable=create_output_dir,
    op_args=[minmax_out_dir],
    dag=dag,
)

create_prep_std_task = PythonOperator(
    task_id=create_prep_std_task_id,
    python_callable=create_preprocessor,
    op_args=[std_out_dir],
    dag=dag,
)

create_prep_minmax_task = PythonOperator(
    task_id=create_prep_minmax_task_id,
    python_callable=create_preprocessor,
    op_args=[minmax_out_dir],
    op_kwargs={"std": False},
    dag=dag,
)

preprocess_std_task = PythonOperator(
    task_id=preprocess_std_task_id,
    python_callable=preprocess,
    op_args=[std_out_dir, create_prep_std_task_id],
    dag=dag,
)

preprocess_minmax_task = PythonOperator(
    task_id=preprocess_minmax_task_id,
    python_callable=preprocess,
    op_args=[minmax_out_dir, create_prep_minmax_task_id],
    dag=dag,
)

remove_temp_dir_task = PythonOperator(
    task_id=remove_temp_dir_task_id, python_callable=remove_temp_dir, dag=dag
)

cleanup_task = SqliteOperator(
    task_id=cleanup_task_id,
    sqlite_conn_id=sqlite_conn_id,
    sql=delete_xcom_sql.format(dag.dag_id),
    dag=dag,
)

create_temp_dir_task >> read_data_task >> split_data_task
split_data_task >> [select_features_task, create_std_dir_task, create_minmax_dir_task]
create_std_dir_task >> create_prep_std_task >> preprocess_std_task
create_minmax_dir_task >> create_prep_minmax_task >> preprocess_minmax_task
[preprocess_std_task, preprocess_minmax_task] >> remove_temp_dir_task >> cleanup_task


# with DAG(
#     "preprocessing_dag",
#     default_args=default_args,
#     catchup=False,  # to not auto run dag
# ) as dag:
#     create_temp_dir_task = BashOperator(
#         task_id=temp_dir_task_id,
#         bash_command="mkdir -p {}/temp_{}".format(
#             project_root, datetime.now().strftime("%Y%m%d%H%M%S")
#         ),
#     )
#     read_data_task = PythonOperator(
#         task_id=read_data_task_id,
#         python_callable=read_data_wrapper,
#     )
#     split_data_task = PythonOperator(
#         task_id=split_data_task_id, python_callable=split_data_wrapper
#     )
#     select_features_task = PythonOperator(
#         task_id=select_features_task_id,
#         python_callable=select_categorical_features_wrapper,
#     )
#     create_dir_std_task = BashOperator(
#         task_id=std_dir_task_id,
#         bash_command="cd {} && mkdir -p {}".format(project_root, std_out_dir),
#     )
#     create_dir_mm_task = BashOperator(
#         task_id=minmax_dir_task_id,
#         bash_command="cd {} && mkdir -p {}".format(project_root, minmax_out_dir),
#     )
#     preprocess_std_task = PythonOperator(
#         task_id=preprocess_std_task_id,
#         python_callable=preprocess_feature_wrapper,
#         op_kwargs=std_kwargs,
#     )
#     preprocess_minmax_task = PythonOperator(
#         task_id=preprocess_minmax_task_id,
#         python_callable=preprocess_feature_wrapper,
#         op_kwargs=dict(std=False, **mm_kwargs),
#     )
#     preprocess_target_task = PythonOperator(
#         task_id=preprocess_target_task_id,
#         python_callable=preprocess_target_wrapper,
#     )
#     save_std_task = PythonOperator(
#         task_id=std_save_task_id,
#         python_callable=save_data_wrapper,
#         op_kwargs=dict(feat_prep_task_id=preprocess_std_task_id, **std_kwargs),
#     )
#     save_minmax_task = PythonOperator(
#         task_id=minmax_save_task_id,
#         python_callable=save_data_wrapper,
#         op_kwargs=dict(feat_prep_task_id=preprocess_minmax_task_id, **mm_kwargs),
#     )
#     # need to add sqlite connection in airflow UI (host = path to db file)
#     delete_xcom_task = SqliteOperator(
#         task_id=delete_xcom_task_id,
#         sqlite_conn_id=sqlite_conn_id,
#         sql=delete_xcom_sql.format(dag.dag_id),
#     )

#     (
#         read_data_task
#         >> split_data_task
#         >> preprocess_target_task
#         >> select_features_task
#         >> [create_dir_std_task, create_dir_mm_task]
#     )
#     create_dir_std_task >> preprocess_std_task >> save_std_task
#     create_dir_mm_task >> preprocess_minmax_task >> save_minmax_task
#     [save_std_task, save_minmax_task] >> delete_xcom_task
