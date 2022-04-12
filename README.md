# Churn prediction

## General info

- Repo for storing source code of churn prediction end-to-end machine learning project which involves process from data exploration, data preprocessing, model training, parameter tuning to model inference
- This project is a portfolio project of owner and is not associated with any courses or institutions

## Process

### Exploration

Firstly, column type and values are validated using data description then there are target distribution analysis, numerical and categorical feature distribution analysis where features values are separated by target class. Lastly, there is correlation analysis to analyse relationship between each feature and target. See [exploration notebook](https://github.com/ppkgtmm/hello-hello/blob/main/exploration.ipynb) to know about what has been found

### Preprocessing

- Apache Airflow was used to build data preprocessing pipeline (DAG) as illustrated in the image below
  <img width=900 src="https://user-images.githubusercontent.com/57994731/162579282-daf97e8c-e9d8-4f4c-8b2f-912ae1f21570.png" />

- In the DAG diagram above, data is loaded from disk and split into train and test sets. Since target preprocessing is the same regardless of feature preprocessing method, target is preprocessed before the split in diagram. As well, categorical features are selected before preprocessing then there is a split in diagram to preprocess features using different scalers in parallel. Finally, there is a task for freeing up the space used by xcom.
