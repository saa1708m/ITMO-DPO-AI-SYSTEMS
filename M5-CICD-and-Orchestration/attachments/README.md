# M5 code examples

Каталог `attachments` содержит демонстрационные примеры для модуля 5 «CI/CD и оркестрация ML-пайплайнов».

## Состав

- `github-actions-ci-example.yml` — пример CI-пайплайна GitHub Actions для запуска проверок и обучения модели;
- `airflow_retraining_dag.py` — пример DAG для периодического переобучения модели (preprocessing данных и обучение).

## Связанные модули и скрипты

Примеры опираются на код и данные из других модулей:

- модуль 2: `../../M2-data-management-and-versioning/attachments/preprocess_beijing.py` (подготовка данных по датасету `../../resources/datasets/module_02/`);
- модуль 3: `../../M3-model-development-and-experiments/attachments/train_mlflow_dry_beans.py` (обучение модели по датасету `../../resources/datasets/module_03/`).

Примеры можно адаптировать под собственный репозиторий студента, сохраняя общую структуру шагов и зависимостей.
