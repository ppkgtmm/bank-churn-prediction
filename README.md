# churn prediction

Repo created to store source code of churn prediction end-to-end machine learning project which involves work from data exploration, data preprocessing, model training, parameter tuning to model inference

## Exploration

Firstly, column type and values are validated againts data description then target distribution was analysed. Subsequently, numerical and categorical feature distribution analysis by target class was done. Lastly, correlation was used to analyse relationship between each feature and target. See [exploration notebook](https://github.com/ppkgtmm/churn-prediction/blob/main/exploration.ipynb) to know more about the observations

## Preprocessing

Apache Airflow was used to build data processing pipeline (DAG) as illustrated in the image below

<img width=900 src="https://user-images.githubusercontent.com/57994731/168348130-19bf7d40-0140-4b78-bd15-00be5e3a6675.png" />

Initially, input data which has already been split during project set up was loaded. Then, categorical features to be used by model were selected using chi-square test of independence on training data at cutoff p-value of 0.05. Afterwards in parallel, each type of preprocessors to be validated were created and used to process the input datasets. Both preprocessors and processed data were then saved to subdirectories inside output folder for reuse. Lastly, a couple of tasks were executed for freeing up the disk space

## Modeling and tuning

Preprocessed data are used for training models using Decision Tree, Random Forest, Logistic Regression and Support Vector Machine algorithms. The results from modeling part can be found in [modeling notebook](https://github.com/ppkgtmm/hello-hello/blob/main/modeling.ipynb). Recall metric is used as model selection criteria to minimize false negatives i.e. minimize no. of churning customer being mistakenly predicted as not churning. As a result, Support Vector Machine algorithm with feature standardization preprocessing method (recall = 0.89 on churn class) was selected for random search tuning

<p align="center">
<img src="https://user-images.githubusercontent.com/57994731/168349011-5be9af25-51c3-4565-b256-469b3938cd26.png" />
</p>

## Inference

An API is developed to serve predictions from model based on input data provided to `/predict` endpoint. Sample input used here was originally labeled as existing customer; however, some of the customer characteristics are similar to attrited customer (see [exploration notebook](https://github.com/ppkgtmm/hello-hello/blob/main/exploration.ipynb) for more information). The tuned model categorized the customer as churning

```json
[
  {
    "gender": "M",
    "education_level": "Uneducated",
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

![image](https://user-images.githubusercontent.com/57994731/168351648-4669022d-1b5b-4a08-8600-9eee9c3c9f02.png)
![image](https://user-images.githubusercontent.com/57994731/168353360-47e23644-3c5f-4d08-9a2d-3c9101ac8694.png)

Front end which provides predictions for supplied input data file was also implemented
![image](https://user-images.githubusercontent.com/57994731/246894228-dfd0cfc4-33a1-41ec-be0c-73bbdd019ce3.png)

## Usage

Make sure you are in project directory inside your shell (bash prefered)

#### Set up

**Part 1** : Only required for the first time running this project

1. Run init script

```sh
. ./init.sh
```

2. Install jupyter notebook (useful for exploration and modeling part)

```sh
pip3 install notebook
```

**Part 2** : Required for every time you are running part of this project in a new shell

```sh
. ./setup.sh
```

#### Explore data or Train model

1. Start jupyter notebook server

```
jupyter notebook
```

2. Navigate to project folder in the browser tab automatically opened by jupyter
3. Open notebook file and run cells (control + Enter) starting from the top

#### Preprocess data

1. Open 2 terminal windows / tabs
2. In the both terminals, run **Part 2** of **Set up** step
3. In the first terminal, run below to start airflow web server

```sh
airflow webserver -p 8080
```

4. In the second terminal, run below to start airflow scheduler

```sh
airflow scheduler
```

5. Navigate to airflow web UI at `http://localhost:8080/`, search for `preprocessing_dag` and click at the DAG name
6. Click play button on the right of the screen to run the DAG (preprocessing results are saved to outputs folder in project directory)

#### Serve model

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
- [dynamically-create-an-enum-with-custom-values-in-python](https://stackoverflow.com/questions/33690064/dynamically-create-an-enum-with-custom-values-in-python)
