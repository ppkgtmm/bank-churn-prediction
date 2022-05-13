data_dir = "data"
data_file = "bank_churners.csv"
target_col = "attrition_flag"
index_col = "clientnum"
drop_col = [
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2",
]
coliner_col = ["avg_open_to_buy"]
seed = 42
test_size = 0.15
split_config = dict(test_size=test_size, random_state=seed)
save_config = dict(index=False)
read_config = dict(index_col=index_col)

temp_dir_task_id = "1.create_temp_dir"
read_data_task_id = "2.read_data"
std_dir_task_id = "3.create_std_dir"
select_features_task_id = "4.select_categorical_features"
minmax_dir_task_id = "5.create_minmax_dir"

create_prep_std_task_id = "6.create_preprocessor_std"
create_prep_minmax_task_id = "7.create_preprocessor_minmax"

preprocess_std_task_id = "8.preprocess_std"
preprocess_minmax_task_id = "9.preprocess_minmax"

remove_temp_dir_task_id = "10.remove_temp_dir"
cleanup_task_id = "11.clean_up"

sqlite_conn_id = "x_com_sqlite"
delete_xcom_sql = "DELETE FROM xcom where dag_id='{}'"

output_dir = "outputs"
std_dir = "std"
minmax_dir = "min_max"
preprocessor_fname = "preprocessor.pkl"
train_fname = "train.csv"
val_fname = "validation.csv"
test_fname = "test.csv"

dt_algo = "Decision Tree"
rf_algo = "Random Forest"
lr_algo = "Logistic Regression"
svm_algo = "Support Vector Machine"

report_cmap = "YlGnBu"

app_name = "Churn prediction with machine learning"
app_version = "1.0.2"
model_fname = "model.pkl"
classes = ["Not Churn", "Churn"]
