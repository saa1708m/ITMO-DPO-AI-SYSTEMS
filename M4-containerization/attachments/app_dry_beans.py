from fastapi import FastAPI
from pydantic import BaseModel

from predict_dry_beans import predict_one

app = FastAPI(
    title="Dry Beans Inference Service",
    version="1.0.0",
    description=(
        "Учебный FastAPI-сервис для модуля 4. "
        "Использует модель, обученную в модуле 3 "
        "на датасете dry beans."
    ),
)


class InferenceRequest(BaseModel):
    # Здесь приведи набор признаков к той схеме, которая у тебя
    # реально используется в модуле 3. Ниже — пример для dry beans.
    area: float
    perimeter: float
    major_axis_length: float
    minor_axis_length: float
    eccentricity: float
    convex_area: float
    extent: float
    solidity: float
    roundness: float
    aspect_ratio: float
    compactness: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: InferenceRequest):
    result = predict_one(request.model_dump())
    return result
