from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

# Предполагаем, что код репозитория смонтирован в /opt/airflow/dags/repo
REPO_ROOT = "/opt/airflow/dags/repo"

default_args = {
    "owner": "mlops-student",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="dry_beans_retraining_pipeline",
    default_args=default_args,
    description="Учебный DAG для переобучения модели (модули 2 и 3)",
    start_date=datetime(2026, 1, 1),
    schedule="@weekly",
    catchup=False,
    tags=["mlops", "demo", "module5"],
) as dag:
    preprocess = BashOperator(
        task_id="preprocess_beijing",
        bash_command=(
            f"cd {REPO_ROOT}/M2-data-management-and-versioning/attachments && "
            "python scripts/preprocess_beijing.py"
        ),
    )

    train_model = BashOperator(
        task_id="train_dry_beans_model",
        bash_command=(
            f"cd {REPO_ROOT}/M3-model-development-and-experiments/attachments && "
            "python train_mlflow_dry_beans.py"
        ),
    )

    # Здесь можно добавить шаги валидации, деплоя и т.д.
    # Например, простой echo как заглушка для последующих модулей:
    validate = BashOperator(
        task_id="validate_and_register",
        bash_command="echo 'Validate metrics and register model version'",
    )

    preprocess >> train_model >> validate
