# churn prediction

Make sure to be inside project directory in your terminal

**Initialization**

1. Install [Python 3.9](https://www.python.org/downloads/)
2. Run the following to grant execute permission to helper script

```sh
chmod +x ./run.sh
```

3. Run helper script to initialize project

```sh
./run.sh init
```

**Data Exploration & Model Training**

1. Run command below to start jupyter notebook server

```
./run.sh notebook
```

2. Navigate to `notebooks` folder in the browser tab automatically opened by jupyter
3. Open notebook file and run cells (control + Enter) starting from the top

**Data Preprocessing**

1. Open 2 terminal windows / tabs
2. In the first terminal, run below to start airflow scheduler

```sh
./run.sh scheduler
```

3. In the second terminal, run following to to start airflow web server

```sh
./run.sh airflow
```

4. Navigate to airflow web UI at `http://localhost:8080/`, input `admin` for both text boxes
5. Search for `preprocessing_dag` which might take a while to appear and then click at the DAG name
6. Click play button on the right of the screen to run the DAG (results will be saved to outputs folder in project directory)

**Model Inference**

1. Run command below to start model API server

```sh
./run.sh api
```

API explorer (Swagger UI) is available at `http://localhost:8000/docs`

2. Launch frontend for interaction with model

```sh
./run.sh ui
```
**Final Output**
![image](https://github.com/ppkgtmm/churn-prediction/blob/main/images/front-end.png?raw=true)

**References**

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
- [how-to-manage-airflow-connections](https://airflow.apache.org/docs/apache-airflow/2.2.4/howto/connection.html)
