source ${PWD}/venv/bin/activate

# pip3 install pip setuptools wheel
# python3 setup.py bdist_wheel

# pip3 install --force-reinstal dist/utilities-0.0.0-py3-none-any.whl

mkdir -p ${PWD}/dags/

export AIRFLOW_HOME=~/airflow
export AIRFLOW__CORE__DAGS_FOLDER="${PWD}/dags"