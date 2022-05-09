data_path = "data/bank_churners.csv"
target_col = "attrition_flag"
index_col = "CLIENTNUM"
drop_col = [
    "Avg_Open_To_Buy",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2",
]

seed = 42
test_size = 0.15

temp_dir_task_id = "1.create_temp_dir"
read_data_task_id = "2.read_data"
split_data_task_id = "3.split_data"

std_dir_task_id = "4.create_std_dir"
select_features_task_id = "5.select_categorical_features"
minmax_dir_task_id = "6.create_minmax_dir"

create_prep_std_task_id = "7.create_preprocessor_std"
create_prep_minmax_task_id = "8.create_preprocessor_minmax"

preprocess_std_task_id = "9.preprocess_std"
preprocess_minmax_task_id = "10.preprocess_minmax"

remove_temp_dir_task_id = "11.remove_temp_dir"
cleanup_task_id = "12.clean_up"

sqlite_conn_id = "x_com_sqlite"
delete_xcom_sql = "DELETE FROM xcom where dag_id='{}'"

std_out_dir = "outputs/std"
minmax_out_dir = "outputs/min_max"

preprocessor_fname = "preprocessor.pkl"
train_fname = "train.csv"
test_fname = "test.csv"

dt_algo = "Decision Tree"
rf_algo = "Random Forest"
lr_algo = "Logistic Regression"
svm_algo = "Support Vector Machine"

report_cmap = "YlGnBu"

app_name = "Churn prediction with machine learning"
app_version = "1.0.1"
model_out_path = "outputs/model.pkl"
classes = ["Not Churn", "Churn"]
