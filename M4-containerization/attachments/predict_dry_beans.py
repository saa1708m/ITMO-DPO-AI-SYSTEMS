from pathlib import Path

import joblib
import pandas as pd

# Каталог attachments модуля 4
ATTACH_DIR = Path(__file__).resolve().parent
REPO_ROOT = ATTACH_DIR.parents[1]

# Путь к модели, экспортированной из модуля 3
MODEL_PATH = (
    REPO_ROOT
    / "M3-model-development-and-experiments"
    / "attachments"
    / "models"
    / "model.pkl"
)

_model = None


def load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Убедитесь, что в модуле 3 выполнен экспорт модели "
                "в каталог attachments/models."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_one(features: dict) -> dict:
    """
    Ожидает словарь с теми же признаками, что использовались при обучении
    модели на датасете dry beans (модуль 3).
    """
    model = load_model()
    frame = pd.DataFrame([features])
    pred = model.predict(frame)[0]
    proba = model.predict_proba(frame)[0]

    # Для наглядности возвращаем top-3 класса
    top3_idx = proba.argsort()[-3:][::-1]
    class_labels = model.classes_

    top3 = [
        {"class": str(class_labels[i]), "probability": float(proba[i])}
        for i in top3_idx
    ]

    return {
        "prediction": str(pred),
        "top3": top3,
    }
