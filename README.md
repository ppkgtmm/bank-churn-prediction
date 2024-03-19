# churn prediction

Make sure to be inside project directory in your terminal

## initialization

1. install [python 3.9](https://www.python.org/downloads/)

2. run the following to grant helper script execution

```sh
chmod +x ./run.sh
```

3. run helper script to initialize project

```sh
./run.sh init
```

## data exploration

1. run command below to start jupyter notebook server

```
./run.sh notebook
```

2. navigate to `notebooks` folder in the browser tab automatically opened by jupyter

3. open `exploration.ipynb` file and run cells (control + enter) starting from the top



## data preprocessing

1. open 2 terminal windows or tabs

2. in the first terminal, run below to start airflow scheduler

```sh
./run.sh scheduler
```

3. in the second terminal, run following to start airflow web server

```sh
./run.sh airflow
```

4. navigate to airflow web UI at http://localhost:8080/, input `admin` for both text boxes

5. search for `preprocessing_dag` which might take a while to appear and then click at the DAG name

6. click play button on the right of the screen to run the DAG

results will be saved to outputs folder in project directory



## model training

1. run command below to start jupyter notebook server

```
./run.sh notebook
```

2. navigate to `notebooks` folder in the browser tab automatically opened by jupyter

3. open `modeling.ipynb` file and run cells (control + enter) starting from the top



## model inference

1. run command below to start model api server

```sh
./run.sh api
```

api explorer (Swagger UI) will be available at http://localhost:8000/docs

2. launch frontend for interaction with model

```sh
./run.sh ui
```



## references

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
