from typing import List
from enum import Enum
from constants import classes

from pydantic import BaseModel
from . import PredictionInput

predictionEnum = Enum("predictionEnum", {str(k): v for k, v in enumerate(classes)})


class PredictionOutput(PredictionInput):
    prediction: predictionEnum


class Predictions(BaseModel):
    predictions: List[PredictionOutput]
