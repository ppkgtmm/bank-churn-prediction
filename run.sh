#!/bin/sh

GREEN="\033[0;32m"
RED="\033[0;31m"
CLEAR="\033[0m"

usage() {  
    echo "usage: ./run.sh command"  
    echo "where command is one of init, notebook"
} 

activate() {
    source venv/bin/activate
}

init() {
    python3 -m venv venv
    activate
    pip3 install -r requirements.txt

    AIRFLOW_VERSION=2.7.0
    PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

    pip3 install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

    export AIRFLOW_HOME=${PWD}/airflow
    airflow db init

    PYTHONPATH=${PWD} python3 data/scripts/split_data.py

    pip3 install notebook
}

setup() {
    activate
    mkdir -p ${PWD}/dags/
    export AIRFLOW_HOME=${PWD}/airflow
    export AIRFLOW__CORE__DAGS_FOLDER="${PWD}/dags"
    export PYTHONPATH=${PWD}
}

notebook() {
    setup
    jupyter notebook
}

if [ "$1" == "init" ]
then 
    init
elif [ "$1" == "notebook" ]
then 
    notebook
else
    usage
    echo "${RED}error : invalid argument${CLEAR}"
    exit 1
fi
