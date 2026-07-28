from pathlib import Path
import pandas as pd


# Каталог m2
M2_DIR = Path(__file__).resolve().parents[1]
# Корень репозитория: resources/code-examples/m2 -> resources -> repo-root
REPO_ROOT = M2_DIR.parents[2]
DATA_PATH = REPO_ROOT / "datasets" / "module_02" / "beijing_air_quality_learning.csv"

OUT_DIR = M2_DIR / "data"
OUT_PATH = OUT_DIR / "beijing_air_quality_processed.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    # Базовые проверки/очистка как учебный пример:
    # - удаляем полные дубликаты
    # - приводим типы числовых признаков
    # - заполняем пропуски медианой для числовых столбцов
    df = df.drop_duplicates().copy()

    numeric_cols = [
        "pm2_5_ug_m3",
        "pm10_ug_m3",
        "so2_ug_m3",
        "no2_ug_m3",
        "co_ug_m3",
        "o3_ug_m3",
        "temperature_c",
        "pressure_hpa",
        "dew_point_c",
        "rain_mm",
        "wind_speed_m_s",
        "missing_measurements",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median(numeric_only=True))

    # Создаём выходной каталог и сохраняем витрину
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)


if __name__ == "__main__":
    main()
