# Лабораторная работа 8.1. Управление секретами и доступами


## 1. Цель работы

Цель лабораторной работы — изучить и практически отработать подходы к безопасному управлению секретами и доступами в инфраструктуре ML-платформы.

В рамках работы необходимо:

- настроить хранение секретов в **HashiCorp Vault**;
- настроить использование **GitHub Secrets** в CI/CD-пайплайне;
- реализовать разграничение доступов с помощью **RBAC**;
- применить принцип **минимально необходимых привилегий**;
- проверить корректность настроенных прав доступа для различных компонентов ML-платформы.

---

## 2. Проверяемый результат обучения

Индикатор LC-5.5, базовый уровень: управляет секретами (Vault, GitHub Secrets); настраивает базовый RBAC.

---

## 3. Постановка задания

### 3.1. Исходная ситуация

Рассматривается учебная ML-платформа, состоящая из следующих компонентов:

- GitHub-репозиторий с кодом ML-проекта;
- GitHub Actions для CI/CD;
- HashiCorp Vault для централизованного хранения секретов;
- Kubernetes-кластер для запуска компонентов платформы;
- MLflow Tracking Server;
- объектное хранилище S3/MinIO для датасетов, моделей и артефактов;
- сервис обучения модели;
- сервис инференса модели;
- контейнерный registry.

Необходимо настроить управление секретами и доступами так, чтобы каждый пользователь и каждый компонент ML-платформы имел только те права, которые необходимы для выполнения своих задач.

---

### 3.2. Роли и компоненты

В лабораторной работе необходимо рассмотреть следующие роли и сервисные аккаунты:

| Субъект | Назначение |
|---|---|
| `data-scientist` | Запуск экспериментов, просмотр результатов, работа с MLflow |
| `ml-engineer` | Подготовка пайплайнов обучения и деплоя моделей |
| `ci-cd` | Выполнение CI/CD-пайплайна из GitHub Actions |
| `mlflow-sa` | Сервисный аккаунт MLflow |
| `training-job-sa` | Сервисный аккаунт job обучения модели |
| `model-serving-sa` | Сервисный аккаунт сервиса инференса |
| `admin` | Администрирование Vault и Kubernetes namespace |

---

### 3.3. Общая задача

Необходимо реализовать конфигурацию, в которой:

1. Секреты не хранятся в Git-репозитории.
2. Секреты ML-платформы хранятся в Vault.
3. GitHub Actions получает необходимые параметры через GitHub Secrets.
4. GitHub Actions получает runtime-секреты из Vault.
5. Kubernetes RBAC ограничивает доступ сервисных аккаунтов.
6. Компоненты ML-платформы имеют разные права доступа.
7. Проверены успешные и запрещенные сценарии доступа.

---

### 3.4. Минимальный набор секретов

Необходимо создать секреты для следующих компонентов:

| Secret path в Vault | Назначение |
|---|---|
| `secret/ml-platform/mlflow` | Доступ к MLflow Tracking Server |
| `secret/ml-platform/s3-readonly` | Read-only доступ к S3/MinIO |
| `secret/ml-platform/s3-readwrite` | Read/write доступ к S3/MinIO |
| `secret/ml-platform/postgres` | Доступ к базе данных MLflow |
| `secret/ml-platform/model-registry` | Доступ к model registry |
| `secret/ml-platform/model-serving` | Секреты сервиса инференса |

Пример содержимого секрета:

```json
{
  "MLFLOW_TRACKING_URI": "http://mlflow.ml-platform.local",
  "MLFLOW_TRACKING_USERNAME": "ml_user",
  "MLFLOW_TRACKING_PASSWORD": "example-password"
}
```

> Важно: запрещается использовать реальные production-секреты, токены, пароли и ключи.

---

### 3.5. Настройка Vault

Необходимо выполнить следующие действия:

1. Запустить HashiCorp Vault локально или в контейнере.
2. Включить KV Secrets Engine.
3. Создать набор секретов для компонентов ML-платформы.
4. Создать политики доступа Vault.
5. Создать токены или настроить способ аутентификации для ролей.
6. Проверить доступы для разных ролей.

Пример политик:

| Vault policy | Разрешения |
|---|---|
| `data-scientist-policy` | Чтение MLflow и read-only S3 |
| `ml-engineer-policy` | Чтение MLflow, S3 read/write, model registry |
| `ci-cd-policy` | Чтение секретов, необходимых для сборки и деплоя |
| `mlflow-policy` | Чтение секрета БД и S3 |
| `model-serving-policy` | Чтение только секретов serving-сервиса |
| `admin-policy` | Полный доступ к секретам ML-платформы |

Пример политики для `model-serving`:

```hcl
path "secret/data/ml-platform/model-serving" {
  capabilities = ["read"]
}

path "secret/data/ml-platform/model-registry" {
  capabilities = ["read"]
}
```

Пример политики для `ci-cd`:

```hcl
path "secret/data/ml-platform/mlflow" {
  capabilities = ["read"]
}

path "secret/data/ml-platform/s3-readwrite" {
  capabilities = ["read"]
}

path "secret/data/ml-platform/model-registry" {
  capabilities = ["read"]
}
```

Необходимо проверить, что:

- `model-serving` не может читать секреты PostgreSQL;
- `data-scientist` не может читать `s3-readwrite`;
- `ci-cd` не имеет полного административного доступа;
- `admin` имеет полный доступ.

---

### 3.6. Настройка GitHub Secrets

В GitHub-репозитории необходимо создать secrets, которые используются GitHub Actions.

Минимальный набор:

| GitHub Secret | Назначение |
|---|---|
| `VAULT_ADDR` | Адрес Vault |
| `VAULT_TOKEN` | Токен доступа к Vault |
| `KUBE_CONFIG` | Конфигурация доступа к Kubernetes |
| `DOCKER_REGISTRY_USERNAME` | Логин для container registry |
| `DOCKER_REGISTRY_PASSWORD` | Пароль или token для container registry |

Допустимые варианты интеграции:

1. **Базовый вариант** — хранение `VAULT_TOKEN` в GitHub Secrets.
2. **Продвинутый вариант** — настройка GitHub OIDC для аутентификации в Vault без долгоживущего токена.

В отчете необходимо объяснить риски хранения `VAULT_TOKEN` в GitHub Secrets и предложить более безопасную альтернативу.

---

### 3.7. Настройка GitHub Actions workflow

Необходимо создать workflow, который выполняет следующие шаги:

1. Получает код из репозитория.
2. Получает параметры из GitHub Secrets.
3. Подключается к Vault.
4. Извлекает необходимые секреты.
5. Выполняет тестовую CI/CD-задачу.
6. Не выводит значения секретов в логи.

Пример workflow:

```yaml
name: ML Platform CI

on:
  push:
    branches:
      - main

jobs:
  ci:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Read secrets from Vault
        uses: hashicorp/vault-action@v3
        with:
          url: ${{ secrets.VAULT_ADDR }}
          token: ${{ secrets.VAULT_TOKEN }}
          secrets: |
            secret/data/ml-platform/mlflow MLFLOW_TRACKING_URI | MLFLOW_TRACKING_URI ;
            secret/data/ml-platform/s3-readwrite AWS_ACCESS_KEY_ID | AWS_ACCESS_KEY_ID ;
            secret/data/ml-platform/s3-readwrite AWS_SECRET_ACCESS_KEY | AWS_SECRET_ACCESS_KEY ;

      - name: Check required environment variables
        run: |
          echo "Checking required variables"
          test -n "$MLFLOW_TRACKING_URI"
          test -n "$AWS_ACCESS_KEY_ID"
          test -n "$AWS_SECRET_ACCESS_KEY"
          echo "Secrets are available, values are not printed"
```

Запрещается использовать команды вида:

```bash
echo $AWS_SECRET_ACCESS_KEY
echo $MLFLOW_TRACKING_PASSWORD
```

---

### 3.8. Настройка Kubernetes RBAC

Необходимо создать отдельный namespace:

```bash
kubectl create namespace ml-platform
```

Необходимо создать service accounts:

```text
mlflow-sa
training-job-sa
model-serving-sa
ci-cd-deployer-sa
```

Пример распределения прав:

| Service Account | Разрешения |
|---|---|
| `mlflow-sa` | Чтение секретов MLflow, PostgreSQL, S3 |
| `training-job-sa` | Создание/чтение Pod и Job, доступ к S3 read/write |
| `model-serving-sa` | Чтение ConfigMap и только serving-секрета |
| `ci-cd-deployer-sa` | Создание и обновление Deployment, Service, ConfigMap |
| `data-scientist` | Просмотр Pod, Job, логов без доступа к Secrets |

Пример `Role` для model serving:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ml-platform
  name: model-serving-role
rules:
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps"]
    verbs: ["get", "list", "watch"]

  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["model-serving-secret"]
    verbs: ["get"]
```

Пример `RoleBinding`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: model-serving-binding
  namespace: ml-platform
subjects:
  - kind: ServiceAccount
    name: model-serving-sa
    namespace: ml-platform
roleRef:
  kind: Role
  name: model-serving-role
  apiGroup: rbac.authorization.k8s.io
```

---

### 3.9. Проверка доступов

Необходимо проверить как разрешенные, так и запрещенные действия.

Примеры команд:

```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:ml-platform:model-serving-sa \
  -n ml-platform
```

```bash
kubectl auth can-i get secret/model-serving-secret \
  --as=system:serviceaccount:ml-platform:model-serving-sa \
  -n ml-platform
```

```bash
kubectl auth can-i get secret/mlflow-db-secret \
  --as=system:serviceaccount:ml-platform:model-serving-sa \
  -n ml-platform
```

```bash
kubectl auth can-i create deployments \
  --as=system:serviceaccount:ml-platform:ci-cd-deployer-sa \
  -n ml-platform
```

```bash
kubectl auth can-i delete secrets \
  --as=system:serviceaccount:ml-platform:ci-cd-deployer-sa \
  -n ml-platform
```

Ожидаемые результаты:

| Проверка | Ожидаемый результат |
|---|---|
| `model-serving-sa` читает `model-serving-secret` | yes |
| `model-serving-sa` читает `mlflow-db-secret` | no |
| `ci-cd-deployer-sa` создает Deployment | yes |
| `ci-cd-deployer-sa` удаляет Secrets | no |
| `data-scientist` читает логи Pod | yes |
| `data-scientist` читает Kubernetes Secrets | no |

---

## 4. Требуемые артефакты

По итогам лабораторной работы необходимо предоставить репозиторий со следующей структурой:

```text
.
├── .github/
│   └── workflows/
│       └── ml-ci.yml
│
├── vault/
│   ├── policies/
│   │   ├── data-scientist-policy.hcl
│   │   ├── ml-engineer-policy.hcl
│   │   ├── ci-cd-policy.hcl
│   │   ├── mlflow-policy.hcl
│   │   └── model-serving-policy.hcl
│   ├── setup-vault.sh
│   ├── test-vault-access.sh
│   └── README.md
│
├── k8s/
│   ├── namespace.yaml
│   ├── service-accounts.yaml
│   ├── roles.yaml
│   ├── role-bindings.yaml
│   ├── test-rbac.sh
│   └── README.md
│
├── app/
│   ├── Dockerfile
│   └── main.py
│
└── README.md
```

Обязательные артефакты:

1. `README.md` с инструкцией по запуску.
2. Vault policies в формате `.hcl`.
3. Скрипт настройки Vault.
4. Скрипт проверки доступов Vault.
5. GitHub Actions workflow.
6. Kubernetes YAML-манифесты.
7. Скрипт проверки Kubernetes RBAC.
8. Таблица ролей и доступов.
9. Отчет по лабораторной работе.

---

## 5. Требования к отчету

Отчет должен содержать следующие разделы.

---

### 5.1. Титульная информация

В отчете необходимо указать:

- название лабораторной работы;
- ФИО студента;
- группу;
- дату выполнения;
- ссылку на GitHub-репозиторий.

---

### 5.2. Описание архитектуры

Необходимо описать архитектуру решения:

- какие компоненты используются;
- где хранятся секреты;
- как GitHub Actions получает доступ к Vault;
- как компоненты ML-платформы получают доступ к секретам;
- как Kubernetes RBAC ограничивает права сервисных аккаунтов.

Пример схемы:

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    | uses GitHub Secrets
    v
HashiCorp Vault
    |
    | provides runtime secrets
    v
Kubernetes / ML Platform
    |
    +--> MLflow
    +--> Training Job
    +--> Model Serving
    +--> S3 / MinIO
```

---

### 5.3. Описание секретов

Необходимо привести таблицу секретов:

| Секрет | Где хранится | Кто имеет доступ | Назначение |
|---|---|---|---|
| MLflow credentials | Vault | `data-scientist`, `ml-engineer`, `ci-cd` | Работа с MLflow |
| S3 read-only key | Vault | `data-scientist`, `model-serving` | Чтение артефактов |
| S3 read-write key | Vault | `training-job-sa`, `ci-cd` | Запись моделей и артефактов |
| PostgreSQL password | Vault | `mlflow-sa` | Работа MLflow с БД |
| Registry token | GitHub Secrets / Vault | `ci-cd` | Push Docker image |

---

### 5.4. Настройка Vault

В отчете необходимо привести:

- команды запуска Vault;
- команды включения KV Secrets Engine;
- команды создания секретов;
- Vault policies;
- команды создания токенов или настройки auth method;
- результаты проверки доступов.

Пример проверки:

```bash
vault kv get secret/ml-platform/mlflow
vault kv get secret/ml-platform/postgres
```

---

### 5.5. Настройка GitHub Secrets

Необходимо описать:

- какие GitHub Secrets были созданы;
- для чего используется каждый secret;
- какие secrets нужны только для CI/CD;
- почему эти значения нельзя хранить в коде;
- какие ограничения имеет GitHub Secrets;
- какие риски остаются.

---

### 5.6. Настройка GitHub Actions

Необходимо приложить:

- файл workflow;
- описание шагов pipeline;
- результат успешного запуска;
- подтверждение, что секреты не выводятся в логи;
- описание того, какие секреты workflow получает из GitHub Secrets, а какие — из Vault.

---

### 5.7. Настройка Kubernetes RBAC

Необходимо привести:

- список namespace;
- список service accounts;
- список Role и RoleBinding;
- YAML-манифесты или ссылки на них;
- таблицу прав доступа.

Пример таблицы:

| Субъект | Pods | Jobs | Deployments | Services | ConfigMaps | Secrets |
|---|---|---|---|---|---|---|
| `data-scientist` | get/list/logs | get/list | no | no | get/list | no |
| `training-job-sa` | get/list/create | get/list/create | no | no | get/list | limited |
| `model-serving-sa` | get/list | no | no | get/list | get/list | only `model-serving-secret` |
| `ci-cd-deployer-sa` | get/list | no | create/update | create/update | create/update | no |
| `mlflow-sa` | get/list | no | no | get/list | get/list | limited |

---

### 5.8. Проверка корректности доступов

В отчете необходимо показать:

- успешные проверки доступа;
- отрицательные проверки доступа;
- вывод команд `kubectl auth can-i`;
- вывод команд проверки Vault policies.

Пример:

```text
model-serving-sa can get model-serving-secret: yes
model-serving-sa can get mlflow-db-secret: no
ci-cd-deployer-sa can create deployments: yes
ci-cd-deployer-sa can delete secrets: no
data-scientist can get pods/log: yes
data-scientist can get secrets: no
```

---

### 5.9. Анализ безопасности

Необходимо ответить на вопросы:

1. Какие секреты используются в ML-платформе?
2. Где они хранятся?
3. Кто имеет к ним доступ?
4. Какие права были ограничены?
5. Какие риски остаются?
6. Что произойдет при утечке `VAULT_TOKEN`?
7. Почему опасно выдавать `cluster-admin` для CI/CD?
8. Какие меры можно применить для повышения безопасности?

Возможные улучшения:

- использовать GitHub OIDC вместо статического `VAULT_TOKEN`;
- включить Vault audit logging;
- настроить короткий TTL для Vault token;
- использовать dynamic secrets;
- включить автоматическую ротацию секретов;
- использовать External Secrets Operator;
- использовать Sealed Secrets;
- разделить окружения `dev`, `stage`, `prod`;
- настроить protected environments в GitHub;
- ограничить доступы по branch protection rules.

---

## 6. Критерии оценивания

Максимальная оценка — **100 баллов**.

| Критерий | Баллы |
|---|---:|
| Описана архитектура решения | 10 |
| Развернут и настроен HashiCorp Vault | 10 |
| Созданы секреты для компонентов ML-платформы | 10 |
| Настроены корректные Vault policies | 15 |
| Настроены GitHub Secrets | 10 |
| Реализован GitHub Actions workflow с использованием Vault/GitHub Secrets | 10 |
| Настроены Kubernetes ServiceAccount, Role и RoleBinding | 15 |
| Проверены положительные и отрицательные сценарии доступа | 10 |
| Подготовлена таблица ролей и доступов | 5 |
| Выполнен анализ рисков и предложены улучшения | 5 |

---

### 6.1. Дополнительные баллы

Дополнительно можно получить до **15 баллов**.

| Улучшение | Баллы |
|---|---:|
| Использование GitHub OIDC вместо статического Vault token | до 5 |
| Настройка Vault audit logging | до 3 |
| Использование External Secrets Operator | до 4 |
| Разделение секретов для `dev`, `stage`, `prod` | до 3 |

---

### 6.2. Штрафы

| Нарушение | Штраф |
|---|---:|
| Секреты опубликованы в Git-репозитории | -30 |
| Секреты выводятся в логах GitHub Actions | -20 |
| Всем ролям выданы административные права | -20 |
| Отсутствуют отрицательные проверки доступа | -10 |
| Отчет не позволяет воспроизвести работу | -15 |
| Использованы реальные production-секреты | -30 |
| Отсутствует анализ рисков | -10 |

---

## 7. Вопросы для защиты

### 7.1. Общие вопросы

1. Что такое secret management?
2. Почему нельзя хранить секреты в Git-репозитории?
3. Чем секрет отличается от обычной конфигурации?
4. Какие типы секретов используются в ML-платформах?
5. Что такое принцип минимально необходимых привилегий?
6. Что такое RBAC?
7. Почему важно разделять роли пользователей и сервисов?
8. Какие риски возникают при использовании одного общего токена?
9. Почему CI/CD-пайплайн является чувствительным компонентом инфраструктуры?
10. Что такое компрометация секрета?

---

### 7.2. Вопросы по HashiCorp Vault

1. Для чего используется HashiCorp Vault?
2. Что такое KV Secrets Engine?
3. Чем отличается KV v1 от KV v2?
4. Что такое Vault policy?
5. Какие capabilities могут быть указаны в Vault policy?
6. Что означает capability `read`?
7. Что означает capability `list`?
8. Почему не следует выдавать `sudo` или полный доступ всем ролям?
9. Что такое Vault token?
10. Что такое TTL токена?
11. Как можно отозвать Vault token?
12. Что такое dynamic secrets?
13. Чем статические секреты отличаются от динамических?
14. Для чего используется Vault audit log?
15. Как GitHub Actions может аутентифицироваться в Vault через OIDC?

---

### 7.3. Вопросы по GitHub Secrets

1. Для чего используются GitHub Secrets?
2. Как обратиться к GitHub Secret в workflow?
3. Почему нельзя выводить secret в лог?
4. Какие секреты целесообразно хранить в GitHub Secrets?
5. Какие секреты лучше хранить в Vault?
6. Чем repository secrets отличаются от environment secrets?
7. Что такое GitHub protected environments?
8. Как можно ограничить использование secret только для production environment?
9. Почему хранение долгоживущего `VAULT_TOKEN` в GitHub Secrets небезопасно?
10. Какие преимущества дает OIDC-интеграция GitHub Actions и Vault?

---

### 7.4. Вопросы по Kubernetes RBAC

1. Что такое ServiceAccount в Kubernetes?
2. Чем ServiceAccount отличается от User?
3. Что такое Role?
4. Что такое ClusterRole?
5. Чем Role отличается от ClusterRole?
6. Что такое RoleBinding?
7. Что такое ClusterRoleBinding?
8. Как ограничить права только одним namespace?
9. Как разрешить доступ только к одному Secret?
10. Для чего используется поле `resourceNames`?
11. Что делает команда `kubectl auth can-i`?
12. Почему CI/CD не должен иметь права `cluster-admin`?
13. Какие права нужны сервису model serving?
14. Какие права нужны training job?
15. Какие права нужны Data Scientist в production-среде?

---

### 7.5. Вопросы по безопасности ML-платформы

1. Какие секреты обычно используются в MLflow?
2. Какие секреты нужны для доступа к S3/MinIO?
3. Почему доступ к S3 должен быть разделен на read-only и read-write?
4. Какие риски возникают при утечке ключа доступа к model registry?
5. Почему сервис инференса не должен иметь доступ к секретам обучения?
6. Почему Data Scientist не должен иметь прямой доступ к production secrets?
7. Какие последствия может иметь утечка токена CI/CD?
8. Как организовать ротацию секретов?
9. Как разделить доступы между `dev`, `stage` и `prod`?
10. Как можно улучшить безопасность предложенной схемы?

---

## 8. Рекомендуемый итоговый результат

В результате выполнения лабораторной работы должна быть получена воспроизводимая конфигурация, в которой:

1. Секреты не хранятся в коде.
2. GitHub Secrets используются только для CI/CD-параметров и bootstrap-доступа.
3. Vault используется как централизованное хранилище секретов.
4. Для разных ролей настроены разные Vault policies.
5. Kubernetes RBAC ограничивает доступ сервисных аккаунтов.
6. CI/CD-пайплайн получает только необходимые права.
7. Model serving не имеет доступа к секретам обучения и БД.
8. Data Scientist не имеет доступа к production-секретам.
9. Проверены положительные и отрицательные сценарии доступа.
10. В отчете описаны риски и предложены меры повышения безопасности.