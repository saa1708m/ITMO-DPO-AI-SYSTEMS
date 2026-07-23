# Python-библиотеки и программные средства

В этом разделе фиксируются библиотеки и инструменты Python, используемые в дисциплине: `pandas`, `scikit-learn`, `mlflow`, `fastapi`, `docker`, `evidently`, `prometheus-client`, `airflow` и другие средства, применяемые в лабораторных работах и проекте.

## Таблица библиотек и инструментов

| Название | Аннотация | Связанные КИМ | Доступ | Лицензия / условия | Дата проверки |
|----------|-----------|---------------|--------|--------------------|---------------|
| pandas | Библиотека для работы с табличными данными: чтение, преобразование, агрегация, подготовка признаков для последующей обработки и обучения моделей. | [M1-introduction-and-architecture](../../M1-introduction-and-architecture/README.md), [M2-data-management-and-versioning](../../M2-data-management-and-versioning/README.md), [M3-model-development-and-experiments](../../M3-model-development-and-experiments/README.md) | PyPI (`pip install pandas`) | BSD License | 2026-07-22 |
| scikit-learn | Набор классических алгоритмов машинного обучения и инструментов для оценивания моделей, подготовки признаков и построения baseline‑решений. | [M3-model-development-and-experiments](../../M3-model-development-and-experiments/README.md) | PyPI (`pip install scikit-learn`) | BSD License | 2026-07-22 |
| MLflow | Платформа для трекинга экспериментов, регистрации моделей и управления артефактами ML‑проектов. | [M3-model-development-and-experiments](../../M3-model-development-and-experiments/README.md), [Project](../../Project/README.md) | PyPI (`pip install mlflow`), официальный сайт MLflow | Apache 2.0 | 2026-07-22 |
| FastAPI | Фреймворк для построения API‑сервисов на Python, часто используемый для развёртывания ML‑моделей как сервисов. | [M4-containerization](../../M4-containerization/README.md), [M6-serving-and-scaling-ml](../../M6-serving-and-scaling-ml/README.md), [Project](../../Project/README.md) | PyPI (`pip install fastapi`) | MIT License | 2026-07-22 |
| Apache Airflow | Платформа для оркестрации конвейеров данных и ML‑проектов, применяемая в модулях по CI/CD и эксплуатации. | [M5-CICD-and-Orchestration](../../M5-CICD-and-Orchestration/README.md), [Project](../../Project/README.md) | PyPI (`pip install apache-airflow`), официальный сайт Apache Airflow | Apache 2.0 | 2026-07-22 |

## Требования к добавлению

Для каждой библиотеки или инструмента рекомендуется:

- фиксировать версию (или минимально поддерживаемую версию);
- указывать команду установки и основные зависимости;
- описывать назначение и типичные сценарии использования в дисциплине;
- указывать лицензию и совместимость с другими инструментами (например, поддерживаемые версии Python);
- приводить минимальный пример использования (ссылку на ноутбук, фрагмент кода или описание в материалах модуля).
