FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код сервиса
COPY app_dry_beans.py ./app_dry_beans.py
COPY predict_dry_beans.py ./predict_dry_beans.py

# Модель по умолчанию ожидается как внешний том,
# смонтированный в /models (это можно описать в lab4-2)
ENV MODEL_PATH=/models/model.pkl

# Для совместимости с путями в predict_dry_beans
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app_dry_beans:app", "--host", "0.0.0.0", "--port", "8000"]
