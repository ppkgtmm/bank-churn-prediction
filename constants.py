data_path = "data/bank_churners.csv"
target_col = "attrition_flag"
index_col = "CLIENTNUM"
drop_col = [
    "Avg_Open_To_Buy",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2",
]

json_orient = "split"
seed = 42
test_size = 0.15

read_data_task_id = "read_data"
split_data_task_id = "split_data"
select_features_task_id = "select_categorical_features"

preprocess_std_task_id = "preprocess_std"
preprocess_minmax_task_id = "preprocess_minmax"
preprocess_target_task_id = "preprocess_target"

std_dir_task_id = "create_std_dir"
minmax_dir_task_id = "create_minmax_dir"

std_save_task_id = "save_std_data"
minmax_save_task_id = "save_minmax_data"

delete_xcom_task_id = "clean_up"

sqlite_conn_id = "x_com_sqlite"
delete_xcom_sql = "delete from xcom where dag_id='{}'"

train_set_key = "train_set"
test_set_key = "test_set"
prep_std_train_key = "train_X_std"
prep_std_test_key = "test_X_std"
prep_mm_train_key = "train_X_mm"
prep_mm_test_key = "test_X_mm"
prep_label_train_key = "train_y"
prep_label_test_key = "test_y"
columns_key_std = "columns_std"
columns_key_mm = "columns_mm"

std_out_dir = "outputs/std"
minmax_out_dir = "outputs/min_max"

preprocessor_fname = "preprocessor.pkl"
train_fname = "train.csv"
test_fname = "test.csv"

dt_algo = "Decision Tree"
rf_algo = "Random Forest"
lr_algo = "Logistic Regression"
svm_algo = "Support Vector Machine"
