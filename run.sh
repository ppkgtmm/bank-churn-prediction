#!/bin/sh

RED="\033[0;31m"
CLEAR="\033[0m"

usage() {
    echo "usage: ./run.sh command"
    echo "where command is one of init, notebook, scheduler, airflow, api, ui"
}

prepenv() {
    source venv/bin/activate
    export AIRFLOW_HOME=${PWD}/airflow
    export AIRFLOW_ADMIN_USERNAME=admin
    export AIRFLOW_ADMIN_PASSWORD=admin
    export AIRFLOW__CORE__DAGS_FOLDER="${PWD}/dags"
    export PYTHONPATH=${PWD}
}

init() {
    python3.9 -m venv venv
    prepenv
    pip3 install -r requirements.txt

    AIRFLOW_VERSION=2.7.0
    PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

    pip3 install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
    pip3 install notebook

    airflow db init
    airflow users create --username ${AIRFLOW_ADMIN_USERNAME} --password ${AIRFLOW_ADMIN_PASSWORD} --firstname First --lastname Last --role Admin --email admin@example.com

    python3 data/scripts/split_data.py
}

setup() {
    prepenv
    mkdir -p ${AIRFLOW__CORE__DAGS_FOLDER}
}

notebook() {
    setup
    jupyter notebook
}

airflow_scheduler() {
    setup
    airflow scheduler
}

airflow_webserver() {
    setup
    airflow connections add "x_com_sqlite" --conn-uri "sqlite://${AIRFLOW_HOME}/airflow.db"
    airflow webserver -p 8080
}

api() {
    setup
    uvicorn app.api:app --reload
}

frontend() {
    setup
    streamlit run app/frontend.py
}

if [ "$1" == "init" ]
then
    init
elif [ "$1" == "notebook" ]
then
    notebook
elif [ "$1" == "scheduler" ]
then
    airflow_scheduler
elif [ "$1" == "airflow" ]
then
    airflow_webserver
elif [ "$1" == "api" ]
then
    api
elif [ "$1" == "ui" ]
then
    frontend
else
    usage
    echo "${RED}error : invalid argument${CLEAR}"
    exit 1
fi
