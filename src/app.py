from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "student_model.pkl"
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Student ML Prediction API", version="1.0.0")


class PredictionRequest(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(request: PredictionRequest):
    if len(request.features) != 15:
        raise HTTPException(
            status_code=400,
            detail=f"Expected 15 features, received {len(request.features)}",
        )

    X = np.asarray(request.features, dtype=float).reshape(1, -1)
    prediction = float(model.predict(X)[0])
    return {"predicted_final_grade": prediction}
