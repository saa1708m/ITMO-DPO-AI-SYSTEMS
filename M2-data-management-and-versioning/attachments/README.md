# M2 code examples

Каталог содержит демонстрационные материалы для модуля 2 «Управление данными и их версионирование».

## Состав

- `eda_beijing.ipynb` — учебный ноутбук для EDA по датасету [resources/datasets/module_02/beijing_air_quality_learning.csv](resources/datasets/module_02/beijing_air_quality_learning.csv);
- `dvc.yaml` — пример описания шага preprocessing в DVC;
- `scripts/preprocess_beijing.py` — пример простого preprocessing-скрипта.

## Назначение

Материалы используются как шаблоны для:

- разведочного анализа качества данных (пропуски, выбросы, распределения);
- проверки целостности временного ряда и станций;
- фиксации шагов обработки в DVC;
- построения воспроизводимого data pipeline для задач прогноза   `pm2_5_ug_m3`.
