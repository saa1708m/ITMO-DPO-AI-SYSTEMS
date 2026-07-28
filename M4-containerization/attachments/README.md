# M4 code examples

Каталог `attachments` содержит демонстрационный пример для модуля 4 «Контейнеризация ML-приложений».

## Состав

- `app_dry_beans.py` — FastAPI inference-сервис для модели, обученной в модуле 3 на датасете [../../resources/datasets/module_03/](../../resources/datasets/module_03/) (`dry_bean_learning.csv`);
- `predict_dry_beans.py` — вспомогательные функции загрузки модели и расчёта предсказания;
- `Dockerfile.app` — пример Dockerfile для упаковки сервиса в контейнер.

## Зависимости

Ожидается, что в каталоге `../../M3-model-development-and-experiments/attachments/models/model.pkl` уже лежит сериализованная sklearn-модель, обученная скриптом модуля 3.

В Dockerfile этот файл может быть смонтирован как внешний volume или скопирован на этапе сборки образа.
