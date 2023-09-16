import json
from os.path import join
import pandas as pd
from typing import List
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from constants import (
    app_name,
    app_version,
    output_dir,
    best_prep_dir,
    preprocessor_fname,
    model_fname,
    classes,
)
from app.schemas import PredictionInput, Predictions
from utilities import decode_label


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
best_prep_path = join(output_dir, best_prep_dir)
prep_path = join(best_prep_path, preprocessor_fname)
model_path = join(output_dir, model_fname)

preprocessor = joblib.load(prep_path)
model = joblib.load(model_path)


@app.get("/info")
def get_app_info():
    return {"app_name": app_name, "version": app_version}


@app.post("/predict")
def read_item(prediction_inputs: List[PredictionInput]) -> Predictions:
    df = pd.DataFrame([data.__dict__ for data in prediction_inputs])
    raw_predictions = model.predict(preprocessor.transform(df))
    df["prediction"] = decode_label(pd.Series(raw_predictions), classes)
    return json.loads(df.to_json(orient="records"))
