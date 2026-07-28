# Руководство преподавателя: развёртывание окружения дисциплины

## 1. Клонирование репозитория

```bash
git clone https://github.com/username/ITMO-DPO-AI-SYSTEMS-main.git
cd ITMO-DPO-AI-SYSTEMS-main
```

## 2. Базовое окружение Python

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
pip install pandas scikit-learn joblib mlflow fastapi uvicorn pydantic
```

Зависимости покрывают все модули. Для Airflow и Prometheus используется Docker.

## 3. Модули 2–3: ноутбуки и скрипты

- [`M2-data-management-and-versioning/attachments/eda_beijing.ipynb`](M2-data-management-and-versioning/attachments/eda_beijing.ipynb) — EDA-ноутбук (запуск: `jupyter notebook` или VS Code);
- [`M2-data-management-and-versioning/attachments/preprocess_beijing.py`](M2-data-management-and-versioning/attachments/preprocess_beijing.py) — скрипт предобработки данных;
- [`M2-data-management-and-versioning/attachments/dvc.yaml`](M2-data-management-and-versioning/attachments/dvc.yaml) — DVC-пайплайн (установите DVC: `pip install dvc`);
- [`M3-model-development-and-experiments/attachments/train_mlflow_dry_beans.py`](M3-model-development-and-experiments/attachments/train_mlflow_dry_beans.py) — тренировка с MLflow-трекингом.

**Датасеты**: [`resources/datasets/module_02/`](resources/datasets/module_02/) (beijing_air_quality), [`resources/datasets/module_03/`](resources/datasets/module_03/) (dry_bean).

## 4. Модули 4–5: Docker-окружение

```bash
cd M4-containerization/attachments

# Запуск MinIO, MLflow, inference-сервиса
docker compose up -d

# Проверка:
# - MinIO web: http://localhost:9001
# - MLflow UI: http://localhost:5000
# - API (dry beans): http://localhost:8000/docs
```

**Важно**: модель, обученная в модуле 3, должна лежать по пути `M3-model-development-and-experiments/attachments/models/model.pkl` — docker-compose монтирует эту директорию в контейнер.

**Для модуля 5**: CI/CD-пример ([`github-actions-ci-example.yml`](M5-CICD-and-Orchestration/attachments/github-actions-ci-example.yml)) работает в GitHub Actions «из коробки». Airflow DAG ([`airflow_retraining_dag.py`](M5-CICD-and-Orchestration/attachments/airflow_retraining_dag.py)) запускается через:

```bash
docker run -d --name airflow -p 8080:8080 \
  -v $(pwd)/M5-CICD-and-Orchestration/attachments:/opt/airflow/dags \
  apache/airflow:latest standalone
```

## 5. Модули 6–7: serving и мониторинг

**Модуль 6** — Jupyter-ноутбуки для локального запуска:
- [`lab_6_1_rest_api_model.ipynb`](M6-serving-and-scaling-ml/attachments/lab_6_1_rest_api_model.ipynb) — REST API для модели;
- [`lab_6_2_kubernetes_canary.ipynb`](M6-serving-and-scaling-ml/attachments/lab_6_2_kubernetes_canary.ipynb) — canary-деплой в Kubernetes (предполагается minikube или kind).

```bash
# Для canary-сценария потребуется локальный Kubernetes:
minikube start --cpus 4 --memory 8g
# или
kind create cluster
```

**Модуль 7** — мониторинг через Prometheus + Grafana (файлы в [`M7-monitoring-and-observability/attachments/`](M7-monitoring-and-observability/attachments/)):

```bash
docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/M7-monitoring-and-observability/attachments/prometheus_dry_beans.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest

docker run -d --name grafana -p 3000:3000 \
  -v $(pwd)/M7-monitoring-and-observability/attachments/grafana_dry_beans_dashboard.json:/etc/grafana/provisioning/dashboards/dashboard.json \
  grafana/grafana:latest
```

Датасет для анализа дрейфа: [`resources/datasets/module_07/`](resources/datasets/module_07/).

## 6. Модуль 8: безопасность и governance

- [`lab_8_1_secrets_rbac.ipynb`](M8-security-governance-responsible-ai/attachments/lab_8_1_secrets_rbac.ipynb) — пример управления секретами и RBAC (для HashiCorp Vault используйте dev-режим):
  ```bash
  docker run -d --name vault -p 8200:8200 \
    -e VAULT_DEV_ROOT_TOKEN_ID=root \
    vault:latest
  ```
- [`lab_8_2_bias_audit.ipynb`](M8-security-governance-responsible-ai/attachments/lab_8_2_bias_audit.ipynb) — аудит смещений модели (не требует внешних сервисов).

## 7. Быстрая проверка

```bash
# Убедитесь, что все порты свободны:
# MinIO 9000/9001 | MLflow 5000 | API 8000 | Prometheus 9090 | Grafana 3000 | Vault 8200
# Запустите базовый EDA-скрипт:
python M2-data-management-and-versioning/attachments/preprocess_beijing.py
# Проверьте API (после docker compose up):
curl http://localhost:8000/docs
```
