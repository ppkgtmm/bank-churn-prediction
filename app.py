import json
from os.path import join
import pandas as pd
from typing import List
import pickle
from fastapi import FastAPI
from constants import (
    app_name,
    app_version,
    output_dir,
    std_dir,
    preprocessor_fname,
    model_fname,
    classes,
)
from schemas import PredictionInput, Predictions
from utilities import decode_label


app = FastAPI()
std_dir_path = join(output_dir, std_dir)

with open(join(std_dir_path, preprocessor_fname), "rb") as fp:
    preprocessor = pickle.load(fp)

with open(join(output_dir, model_fname), "rb") as fp:
    model = pickle.load(fp)


@app.get("/info")
def get_app_info():
    return {"app_name": app_name, "version": app_version}


@app.post("/predict")
def read_item(prediction_inputs: List[PredictionInput]) -> Predictions:
    df = pd.DataFrame([data.__dict__ for data in prediction_inputs])
    raw_predictions = model.predict(preprocessor.transform(df))
    df["prediction"] = decode_label(pd.Series(raw_predictions), classes)
    return json.loads(df.to_json(orient="records"))
