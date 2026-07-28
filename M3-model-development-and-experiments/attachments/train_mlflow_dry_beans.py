from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

# Мы находимся в каталоге M3-model-development-and-experiments/attachments
ATTACH_DIR = Path(__file__).resolve().parent
REPO_ROOT = ATTACH_DIR.parents[1]

DATA_PATH = (
    REPO_ROOT
    / "resources"
    / "datasets"
    / "module_03"
    / "dry_bean_learning.csv"
)
TARGET = "bean_variety"  # как в README датасета module_03[page:1]


def main():
    # 1. Загрузка данных
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # 2. Запуск MLflow-эксперимента
    with mlflow.start_run():
        n_estimators = 100
        max_depth = None
        class_weight = "balanced"

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            class_weight=class_weight,
            random_state=42,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        macro_f1 = f1_score(y_test, preds, average="macro")

        # 3. Логирование параметров и метрик
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("class_weight", class_weight)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("macro_f1", macro_f1)

        # 4. Логирование модели
        mlflow.sklearn.log_model(model, "model")

        print(f"accuracy={acc:.3f}, macro_f1={macro_f1:.3f}")


if __name__ == "__main__":
    main()
