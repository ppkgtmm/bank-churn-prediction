# Churn prediction

## General info

- Repo for storing source code of churn prediction end-to-end machine learning project which involves process from data exploration, data preprocessing, model training, parameter tuning to model inference
- This project is a portfolio project of owner and is not associated with any courses or institutions

## Process

### Exploration

- Firstly, column type and values are validated using data description then there are target distribution analysis, numerical and categorical feature distribution analysis where features values are separated by target class. Lastly, there is correlation analysis to analyse relationship between each feature and target. See [exploration notebook](https://github.com/ppkgtmm/hello-hello/blob/main/exploration.ipynb) to know about what has been found

### Preprocessing

- Apache Airflow was used to build data preprocessing pipeline (DAG) as illustrated in the image below
  <img width=900 src="https://user-images.githubusercontent.com/57994731/162579282-daf97e8c-e9d8-4f4c-8b2f-912ae1f21570.png" />

- In the DAG diagram above, data is loaded from disk and split into train and test sets. Since target preprocessing is the same regardless of feature preprocessing method, target is preprocessed before the split in diagram. As well, categorical features are selected before preprocessing then there is a split in diagram to preprocess features using different scalers in parallel. Finally, there is a task for freeing up the space used by xcom.

### Modeling and tuning

- Preprocessed data are used for model training using Decision Tree, Random Forest, Logistic Regression and Support Vector Machine. Algorithm and preprocessing method (more specifically numeric feature scaler) that best perform on validation set are chosen for furthur tuning.
- The results from modeling part can be found in [modeling notebook](https://github.com/ppkgtmm/hello-hello/blob/main/modeling.ipynb). Recall metric is used as model selection criteria to minimize false negatives i.e. minimize no. of churning customer being mistakenly predicted as not churning. As a result, Support Vector Machine algorithm with feature standardization (recall = 0.9 on churn class) is selected for random search tuning

<p align="center">
<img src="https://user-images.githubusercontent.com/57994731/163005625-5492800c-2d43-49b8-b0ad-6ae3e20ffe23.png" />
</p>

### Inference

- An API is developed to serve predictions from model based on input data provided to `/predict` endpoint
- Sample input from data originally labeled as existing customer but some of the customer characteristics are similar to attrited customer (see [exploration notebook](https://github.com/ppkgtmm/hello-hello/blob/main/exploration.ipynb)). Consequently, the customer is categorized as churning

```json
[
  {
    "gender": "M",
    "customer_age": 57,
    "dependent_count": 3,
    "months_on_book": 38,
    "total_relationship_count": 5,
    "months_inactive_12_mon": 3,
    "contacts_count_12_mon": 3,
    "credit_limit": 2472,
    "total_revolving_bal": 2457,
    "total_amt_chng_q4_q1": 0.693,
    "total_trans_amt": 1392,
    "total_trans_ct": 33,
    "total_ct_chng_q4_q1": 0.737,
    "avg_utilization_ratio": 0.994,
    "prediction": "Churn"
  }
]
```

![image](https://user-images.githubusercontent.com/57994731/163004429-378bb741-8cd6-4dfb-87b7-bc77796d8dc2.png)
![image](https://user-images.githubusercontent.com/57994731/163004534-5885f183-27d1-4128-9816-b5f629c9d2ed.png)

## Run the project

- Make sure you are in project directory inside your shell (bash prefered)

### Initialization

#### Part 1

- Only required for the first time running this project

1. Run init script

```sh
. ./init.sh
```

2. Install jupyter notebook (useful for exploration and modeling part)

```sh
pip3 install notebook
```

#### Part 2

- Required for every time you are running part of this project in a new shell

```sh
. ./setup.sh
```

### Exploration or Modeling

1. Start jupyter notebook server

```
jupyter notebook
```

2. Navigate to project folder in the browser tab automatically opened by jupyter
3. Open notebook file and run cells (control + Enter) starting from the top

### Preprocessing

1. Open 2 terminal windows / tabs
2. In the both terminals, run **Part 2** of **Initialization** step
3. In the first terminal, run below to start airflow web server

```sh
airflow webserver -p 8080
```

4. In the second terminal, run below to start airflow scheduler

```sh
airflow scheduler
```

5. Navigate to airflow web UI at `http://localhost:8080/`, search for `preprocessing_dag` and click at the DAG name
6. Click play button on the right of the screen to run the DAG (preprocessing results are saved to outputs folder of project directory)

### Inference

```sh
uvicorn app:app --reload
```

- Running command above will start API server at `http://localhost:8000`
- API explorer (Swagger UI) is available at `http://localhost:8000/docs`

## References
- [credit-card-customers-churn-dataset](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers)
- [multicollinearity](https://en.wikipedia.org/wiki/Multicollinearity)
- [apache-airflow-quick-start](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html)
- [apache-airflow-modules-management](https://airflow.apache.org/docs/apache-airflow/stable/modules_management.html)
- [importing-local-module-python-script-in-airflow-dag](https://stackoverflow.com/questions/50150384/importing-local-module-python-script-in-airflow-dag)
- [pandas-dataframe-styling-color-palette](https://pandas.pydata.org/docs/user_guide/style.html)
- [sklearn-model-selection-randomized-search-cv](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html)
- [sklearn-metrics-make-scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html)
- [saving-and-loading-objects-and-using-pickle](https://stackoverflow.com/questions/4530611/saving-and-loading-objects-and-using-pickle)
- [fast-api-framework-tutorial](https://fastapi.tiangolo.com/)
- [pandas-dataframe-to-json](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html)
