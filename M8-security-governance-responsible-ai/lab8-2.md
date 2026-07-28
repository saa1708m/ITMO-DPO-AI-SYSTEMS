# Лабораторная работа 8.2. Анализ bias и аудит модели

## 1. Цель работы

Цель лабораторной работы — изучить методы выявления, измерения и документирования bias в моделях машинного обучения, а также освоить практику проведения аудита модели с использованием инструментов **Fairlearn** и/или **AIF360**.

В рамках работы необходимо:

- обучить базовую ML-модель на датасете, содержащем чувствительные признаки;
- выявить потенциальный bias модели относительно выбранных групп;
- рассчитать метрики качества и fairness-метрики;
- провести сравнение качества модели для разных групп пользователей;
- применить один или несколько методов снижения bias;
- подготовить отчёт об аудите модели в формате **Model Card**.

---

## 2. Проверяемый результат обучения

Индикатор LC-5.5, средний уровень: реализует полную ролевую модель доступа; документирует модели (model cards); проводит аудит.

---

## 3. Постановка задания

### 3.1. Исходный сценарий

Рассматривается ML-система, принимающая решение, потенциально влияющее на пользователей. Например:

- одобрение кредита;
- скоринг кандидатов при найме;
- прогноз дохода;
- медицинская классификация;
- оценка риска дефолта;
- модерация заявок;
- предсказание вероятности оттока клиента.

Модель обучается на исторических данных. В данных могут присутствовать чувствительные признаки, например:

- пол;
- возраст;
- раса или этническая группа;
- семейное положение;
- регион;
- инвалидность;
- уровень дохода;
- образование.

Необходимо провести аудит модели и определить, проявляет ли модель смещение по отношению к отдельным группам.

---

### 3.2. Общая задача

Необходимо реализовать полный цикл аудита bias:

1. Выбрать датасет.
2. Определить целевую переменную.
3. Определить один или несколько чувствительных признаков.
4. Провести первичный анализ данных.
5. Обучить baseline-модель.
6. Оценить качество модели в целом.
7. Оценить качество модели по группам.
8. Рассчитать fairness-метрики.
9. Сделать вывод о наличии или отсутствии bias.
10. Применить метод снижения bias.
11. Повторно оценить модель.
12. Сравнить результаты до и после mitigation.
13. Подготовить Model Card.

---

### 3.3. Рекомендуемые датасеты

Можно использовать один из следующих датасетов:

| Датасет | Источник | Возможная задача | Чувствительные признаки |
|---|---|---|---|
| Adult Census Income | UCI / OpenML | Предсказание дохода `>50K` | `sex`, `race`, `age` |
| German Credit | UCI / AIF360 | Кредитный скоринг | `sex`, `age` |
| COMPAS | ProPublica / AIF360 | Риск рецидива | `race`, `sex` |
| Bank Marketing | UCI | Отклик на банковский продукт | `age`, `marital` |
| Titanic | Kaggle / OpenML | Выживание пассажира | `sex`, `age`, `class` |
| Medical Appointment No Shows | Kaggle | Неявка на приём | `age`, `gender` |

Допускается использование собственного датасета при условии, что:

- в нём есть бинарная или многоклассовая целевая переменная;
- присутствует хотя бы один чувствительный признак;
- можно обоснованно анализировать fairness модели.

---

### 3.4. Требования к модели

Необходимо обучить минимум одну baseline-модель.

Допустимые модели:

- Logistic Regression;
- Decision Tree;
- Random Forest;
- Gradient Boosting;
- XGBoost / LightGBM / CatBoost;
- любая другая модель классификации.

Минимально необходимо:

- разделить данные на train/test;
- выполнить preprocessing;
- обучить модель;
- получить предсказания;
- рассчитать метрики качества;
- рассчитать fairness-метрики.

---

### 3.5. Выбор чувствительных признаков

Необходимо выбрать минимум один sensitive attribute.

Примеры:

```text
sex: Male / Female
race: White / Non-white
age: age >= 25 / age < 25
```

Для каждого sensitive attribute необходимо определить:

| Параметр | Описание |
|---|---|
| Sensitive attribute | Название чувствительного признака |
| Privileged group | Группа, исторически или контекстно имеющая преимущество |
| Unprivileged group | Группа, потенциально находящаяся в менее выгодном положении |
| Обоснование выбора | Почему этот признак важен для аудита |

Пример:

| Sensitive attribute | Privileged group | Unprivileged group | Обоснование |
|---|---|---|---|
| `sex` | `Male` | `Female` | Возможный риск гендерного bias при кредитном скоринге |
| `age` | `age >= 25` | `age < 25` | Возможная дискриминация молодых заявителей |

---

## 4. Практическая часть

### 4.1. Этап 1 — Подготовка окружения

Необходимо подготовить Python-окружение.

Рекомендуемые библиотеки:

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
fairlearn
aif360
jupyter
```

Пример установки:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn fairlearn jupyter
```

Для AIF360:

```bash
pip install aif360
```

Дополнительно можно использовать:

```bash
pip install shap xgboost lightgbm imbalanced-learn
```

---

### 4.2. Этап 2 — Загрузка и описание данных

Необходимо:

1. Загрузить датасет.
2. Описать источник данных.
3. Описать целевую переменную.
4. Описать признаки.
5. Найти пропуски и выбросы.
6. Определить sensitive attribute.
7. Разделить пользователей на группы.

В отчете необходимо привести:

- размер датасета;
- количество признаков;
- тип задачи;
- распределение целевой переменной;
- распределение чувствительного признака;
- распределение целевой переменной по группам.

Пример анализа:

```python
df["sex"].value_counts(normalize=True)
df.groupby("sex")["target"].mean()
```

---

### 4.3. Этап 3 — Предобработка данных

Необходимо выполнить предобработку:

- обработать пропущенные значения;
- закодировать категориальные признаки;
- масштабировать числовые признаки при необходимости;
- разделить данные на train/test;
- отделить sensitive attribute для fairness-анализа.

Пример:

```python
from sklearn.model_selection import train_test_split

X = df.drop(columns=["target"])
y = df["target"]
sensitive_features = df["sex"]

X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
    X,
    y,
    sensitive_features,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

Важно: необходимо явно указать, используется ли sensitive attribute как входной признак модели.  
Если sensitive attribute исключается из признаков, необходимо объяснить, почему bias всё равно может сохраняться через proxy features.

---

### 4.4. Этап 4 — Обучение baseline-модели

Необходимо обучить базовую модель.

Пример:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]
```

Необходимо рассчитать стандартные метрики:

| Метрика | Назначение |
|---|---|
| Accuracy | Общая доля верных ответов |
| Precision | Точность положительного класса |
| Recall | Полнота положительного класса |
| F1-score | Баланс precision и recall |
| ROC-AUC | Качество ранжирования |
| Confusion matrix | Ошибки FP/FN |

---

### 4.5. Этап 5 — Групповой анализ качества

Необходимо рассчитать качество модели отдельно для каждой группы.

Пример групп:

```text
Male / Female
White / Non-white
Age >= 25 / Age < 25
```

Для каждой группы необходимо посчитать:

- количество объектов;
- selection rate;
- accuracy;
- precision;
- recall;
- FPR;
- FNR;
- TPR;
- TNR;
- confusion matrix.

Пример с Fairlearn:

```python
from fairlearn.metrics import MetricFrame
from sklearn.metrics import accuracy_score, precision_score, recall_score

metrics = {
    "accuracy": accuracy_score,
    "precision": precision_score,
    "recall": recall_score
}

metric_frame = MetricFrame(
    metrics=metrics,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=s_test
)

print(metric_frame.overall)
print(metric_frame.by_group)
```

---

### 4.6. Этап 6 — Расчёт fairness-метрик

Необходимо рассчитать fairness-метрики минимум по одному sensitive attribute.

#### Обязательные fairness-метрики

| Метрика | Что показывает |
|---|---|
| Selection Rate | Доля положительных решений в группе |
| Demographic Parity Difference | Разница selection rate между группами |
| Demographic Parity Ratio | Отношение selection rate между группами |
| Equalized Odds Difference | Разница ошибок и true positive rate между группами |
| Equal Opportunity Difference | Разница TPR между группами |
| False Positive Rate Difference | Разница FPR между группами |
| False Negative Rate Difference | Разница FNR между группами |

Пример с Fairlearn:

```python
from fairlearn.metrics import (
    selection_rate,
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference
)

print("Selection rate:", selection_rate(y_test, y_pred))
print(
    "Demographic parity difference:",
    demographic_parity_difference(y_test, y_pred, sensitive_features=s_test)
)
print(
    "Demographic parity ratio:",
    demographic_parity_ratio(y_test, y_pred, sensitive_features=s_test)
)
print(
    "Equalized odds difference:",
    equalized_odds_difference(y_test, y_pred, sensitive_features=s_test)
)
```

---

### 4.7. Этап 7 — Интерпретация fairness-метрик

Необходимо интерпретировать полученные значения.

Пример вопросов для анализа:

1. У какой группы выше selection rate?
2. У какой группы выше false negative rate?
3. У какой группы выше false positive rate?
4. Есть ли существенная разница в recall между группами?
5. Можно ли говорить о наличии disparate impact?
6. Совпадает ли хорошее общее качество модели с хорошим качеством по группам?
7. Есть ли группы, для которых модель работает хуже?
8. Какие признаки могут быть proxy features для sensitive attribute?

Пример интерпретации:

```text
Общая accuracy модели составляет 0.84, однако recall для группы Female равен 0.62,
а для группы Male — 0.81. Это означает, что модель значительно чаще пропускает
положительный класс для группы Female. Такая разница может указывать на наличие
bias и требует дополнительного анализа.
```

---

### 4.8. Этап 8 — Mitigation bias

Необходимо применить минимум один метод снижения bias.

Допустимые подходы:

#### Pre-processing

- Reweighing;
- Disparate Impact Remover;
- балансировка данных;
- удаление или трансформация proxy features.

#### In-processing

- Fairlearn ExponentiatedGradient;
- GridSearch с fairness constraints;
- adversarial debiasing.

#### Post-processing

- Threshold Optimizer;
- Calibrated Equalized Odds;
- изменение threshold по группам.

Пример с Fairlearn `ThresholdOptimizer`:

```python
from fairlearn.postprocessing import ThresholdOptimizer

postprocess_est = ThresholdOptimizer(
    estimator=model,
    constraints="demographic_parity",
    predict_method="predict_proba"
)

postprocess_est.fit(
    X_train,
    y_train,
    sensitive_features=s_train
)

y_pred_mitigated = postprocess_est.predict(
    X_test,
    sensitive_features=s_test
)
```

Пример с Fairlearn `ExponentiatedGradient`:

```python
from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from sklearn.linear_model import LogisticRegression

estimator = LogisticRegression(max_iter=1000)

mitigator = ExponentiatedGradient(
    estimator=estimator,
    constraints=DemographicParity()
)

mitigator.fit(
    X_train,
    y_train,
    sensitive_features=s_train
)

y_pred_mitigated = mitigator.predict(X_test)
```

---

### 4.9. Этап 9 — Сравнение модели до и после mitigation

Необходимо сравнить baseline-модель и mitigated-модель.

Пример таблицы:

| Метрика | Baseline | After mitigation | Изменение |
|---|---:|---:|---:|
| Accuracy | 0.84 | 0.81 | -0.03 |
| Precision | 0.78 | 0.75 | -0.03 |
| Recall | 0.69 | 0.72 | +0.03 |
| F1-score | 0.73 | 0.73 | 0.00 |
| Demographic Parity Difference | 0.22 | 0.08 | -0.14 |
| Equalized Odds Difference | 0.18 | 0.10 | -0.08 |

Необходимо сделать вывод:

- улучшилась ли fairness;
- насколько снизилось качество модели;
- приемлем ли компромисс между quality и fairness;
- какие риски остались;
- можно ли использовать модель в реальной системе.

---

### 4.10. Этап 10 — Подготовка Model Card

Необходимо подготовить отчёт об аудите модели в формате **Model Card**.

Model Card должен содержать:

1. Название модели.
2. Назначение модели.
3. Владельца или автора модели.
4. Версию модели.
5. Датасет и источник данных.
6. Описание целевой переменной.
7. Описание sensitive attributes.
8. Используемые признаки.
9. Исключенные признаки.
10. Метрики качества.
11. Fairness-метрики.
12. Результаты анализа по группам.
13. Ограничения модели.
14. Этические риски.
15. Рекомендации по применению.
16. Запрещенные сценарии использования.
17. Меры по снижению bias.
18. План мониторинга модели.

---

## 5. Требуемые артефакты

По итогам выполнения лабораторной работы необходимо предоставить репозиторий со следующей примерной структурой:

```text
.
├── data/
│   ├── README.md
│   └── sample_data.csv
│
├── notebooks/
│   └── bias_audit.ipynb
│
├── src/
│   ├── preprocess.py
│   ├── train.py
│   ├── evaluate.py
│   └── fairness_metrics.py
│
├── reports/
│   ├── model_card.md
│   ├── bias_audit_report.md
│   └── figures/
│       ├── target_distribution.png
│       ├── group_distribution.png
│       ├── fairness_metrics_baseline.png
│       └── fairness_metrics_mitigated.png
│
├── requirements.txt
└── README.md
```

Обязательные артефакты:

1. Jupyter Notebook или Python-скрипты с полным pipeline.
2. Описание датасета и источника данных.
3. Код предобработки данных.
4. Код обучения baseline-модели.
5. Код расчёта метрик качества.
6. Код расчёта fairness-метрик.
7. Групповой анализ качества модели.
8. Реализация минимум одного метода mitigation bias.
9. Сравнение модели до и после mitigation.
10. Отчёт об аудите bias.
11. Model Card в формате Markdown.
12. `requirements.txt` или `environment.yml`.
13. Инструкция по воспроизведению эксперимента.

---

## 6. Требования к отчету

Отчет должен быть оформлен в формате Markdown, PDF или Jupyter Notebook.

---

### 6.1. Титульная информация

В отчете необходимо указать:

- название лабораторной работы;
- ФИО студента;
- группу;
- дату выполнения;
- ссылку на репозиторий;
- используемый датасет;
- используемую библиотеку: Fairlearn, AIF360 или обе.

---

### 6.2. Описание задачи

Необходимо описать:

- предметную область;
- какую задачу решает модель;
- почему задача может быть чувствительной с точки зрения fairness;
- какие решения принимает модель;
- на кого могут повлиять ошибки модели;
- какие последствия могут иметь false positive и false negative.

Пример:

```text
Модель решает задачу кредитного скоринга. Положительный класс означает одобрение
заявки. False negative может привести к необоснованному отказу добросовестному
клиенту, а false positive — к финансовым потерям организации.
```

---

### 6.3. Описание данных

Необходимо привести:

| Раздел | Что должно быть описано |
|---|---|
| Источник данных | Откуда получен датасет |
| Размер данных | Количество строк и признаков |
| Целевая переменная | Что предсказывает модель |
| Признаки | Основные группы признаков |
| Sensitive attributes | Какие признаки выбраны для fairness-аудита |
| Пропуски | Как обработаны missing values |
| Дисбаланс классов | Есть ли перекос целевой переменной |
| Дисбаланс групп | Есть ли перекос sensitive groups |

Необходимо добавить минимум 2–3 визуализации:

- распределение целевой переменной;
- распределение sensitive attribute;
- доля положительного класса по группам;
- при необходимости — heatmap корреляций.

---

### 6.4. Описание baseline-модели

Необходимо указать:

- выбранный алгоритм;
- почему выбран этот алгоритм;
- какие признаки использовались;
- какие признаки были исключены;
- параметры модели;
- способ разделения train/test;
- метрики качества.

Пример таблицы:

| Метрика | Значение |
|---|---:|
| Accuracy | 0.84 |
| Precision | 0.79 |
| Recall | 0.71 |
| F1-score | 0.75 |
| ROC-AUC | 0.86 |

---

### 6.5. Групповой анализ

Необходимо представить качество модели по группам.

Пример таблицы:

| Группа | Count | Selection Rate | Accuracy | Precision | Recall | FPR | FNR |
|---|---:|---:|---:|---:|---:|---:|---:|
| Privileged | 1200 | 0.42 | 0.86 | 0.81 | 0.78 | 0.12 | 0.22 |
| Unprivileged | 800 | 0.27 | 0.79 | 0.74 | 0.61 | 0.10 | 0.39 |

Необходимо объяснить:

- есть ли разница в метриках;
- какие группы получают меньше положительных решений;
- какие группы чаще получают ошибки;
- какие ошибки являются наиболее критичными для задачи.

---

### 6.6. Fairness-метрики

Необходимо привести значения fairness-метрик.

Пример таблицы:

| Fairness-метрика | Значение | Интерпретация |
|---|---:|---|
| Demographic Parity Difference | 0.15 | Есть различие в доле положительных решений |
| Demographic Parity Ratio | 0.64 | Возможный disparate impact |
| Equalized Odds Difference | 0.18 | Ошибки распределены неравномерно |
| Equal Opportunity Difference | 0.17 | Различается TPR между группами |
| FNR Difference | 0.16 | Одна группа чаще получает false negative |

Необходимо дать содержательную интерпретацию каждой рассчитанной метрики.

---

### 6.7. Анализ причин bias

Необходимо рассмотреть возможные причины bias:

- исторический bias в данных;
- дисбаланс классов;
- дисбаланс групп;
- proxy features;
- bias при сборе данных;
- label bias;
- sample selection bias;
- различие качества данных по группам;
- некорректный threshold классификации;
- недостаточная представленность группы.

Необходимо привести не менее 3 возможных причин, релевантных выбранному датасету.

---

### 6.8. Mitigation bias

Необходимо описать выбранный метод снижения bias:

| Раздел | Что указать |
|---|---|
| Метод | Например, ThresholdOptimizer или Reweighing |
| Тип метода | Pre-processing / In-processing / Post-processing |
| Почему выбран | Обоснование выбора |
| Как применен | Краткое описание реализации |
| Ограничения | Какие недостатки есть у метода |

---

### 6.9. Сравнение до и после mitigation

Необходимо представить сравнительную таблицу:

| Метрика | Baseline | Mitigated | Комментарий |
|---|---:|---:|---|
| Accuracy |  |  |  |
| Precision |  |  |  |
| Recall |  |  |  |
| F1-score |  |  |  |
| Demographic Parity Difference |  |  |  |
| Demographic Parity Ratio |  |  |  |
| Equalized Odds Difference |  |  |  |
| Equal Opportunity Difference |  |  |  |

Необходимо сделать вывод:

- удалось ли снизить bias;
- какие fairness-метрики улучшились;
- какие метрики качества ухудшились;
- является ли компромисс приемлемым;
- какие дополнительные меры можно предложить.

---

### 6.10. Model Card

В отчете должен быть отдельный раздел **Model Card** или отдельный файл `model_card.md`.

Рекомендуемая структура Model Card:

```markdown
# Model Card

## Model Details

- Model name:
- Version:
- Date:
- Author:
- Model type:
- Library / framework:

## Intended Use

- Primary intended use:
- Intended users:
- Out-of-scope use cases:

## Training Data

- Dataset name:
- Dataset source:
- Dataset size:
- Data collection period:
- Sensitive attributes:
- Known limitations:

## Evaluation Data

- Test split:
- Evaluation method:
- Groups evaluated:

## Metrics

### Overall Performance

| Metric | Value |
|---|---:|
| Accuracy | |
| Precision | |
| Recall | |
| F1-score | |
| ROC-AUC | |

### Fairness Metrics

| Metric | Value |
|---|---:|
| Demographic Parity Difference | |
| Demographic Parity Ratio | |
| Equalized Odds Difference | |
| Equal Opportunity Difference | |

## Evaluation by Group

| Group | Count | Selection Rate | Accuracy | Precision | Recall | FPR | FNR |
|---|---:|---:|---:|---:|---:|---:|---:|

## Ethical Considerations

- Potential harms:
- Groups at risk:
- Bias detected:
- Mitigation applied:

## Limitations

- Data limitations:
- Model limitations:
- Fairness limitations:
- Deployment limitations:

## Recommendations

- Recommended use:
- Monitoring requirements:
- Human oversight:
- Retraining requirements:

## Prohibited Uses

- 
```

---

### 6.11. Выводы

В выводах необходимо ответить:

1. Был ли обнаружен bias?
2. По каким группам он проявился?
3. Какие fairness-метрики это показывают?
4. Какой метод mitigation был применен?
5. Улучшилась ли fairness после mitigation?
6. Как изменилось качество модели?
7. Можно ли использовать модель в реальной системе?
8. Какие дополнительные меры необходимы перед production deployment?

---

## 7. Критерии оценивания

Максимальная оценка — **100 баллов**.

| Критерий | Баллы |
|---|---:|
| Описана задача, датасет и sensitive attributes | 10 |
| Выполнен EDA и анализ распределений по группам | 10 |
| Реализована предобработка данных | 10 |
| Обучена baseline-модель | 10 |
| Рассчитаны стандартные метрики качества | 10 |
| Выполнен групповой анализ качества модели | 10 |
| Рассчитаны fairness-метрики через Fairlearn и/или AIF360 | 15 |
| Проведена интерпретация bias и анализ причин | 10 |
| Применен метод mitigation bias | 10 |
| Подготовлен Model Card | 10 |
| Сделаны содержательные выводы и рекомендации | 5 |

> Если сумма превышает 100 из-за детализации, итоговая оценка нормируется до 100 баллов.

---

### 7.1. Дополнительные баллы

Дополнительно можно получить до **15 баллов**.

| Улучшение | Баллы |
|---|---:|
| Использование одновременно Fairlearn и AIF360 | до 4 |
| Анализ нескольких sensitive attributes | до 3 |
| Анализ intersectional fairness, например `sex + race` | до 3 |
| Сравнение нескольких mitigation-методов | до 3 |
| Добавление SHAP/feature importance для анализа proxy features | до 2 |

---

### 7.2. Штрафы

| Нарушение | Штраф |
|---|---:|
| Sensitive attribute не выбран или не обоснован | -15 |
| Нет группового анализа качества модели | -20 |
| Нет fairness-метрик | -25 |
| Нет интерпретации результатов | -15 |
| Нет mitigation bias | -15 |
| Нет Model Card | -20 |
| Отчет содержит только код без выводов | -20 |
| Невозможно воспроизвести эксперимент | -15 |
| Используются некорректные или неподходящие метрики | -10 |
| Выводы не соответствуют полученным результатам | -10 |

---

## 8. Вопросы для защиты

### 8.1. Общие вопросы

1. Что такое bias в машинном обучении?
2. Чем bias в данных отличается от bias модели?
3. Что такое fairness в ML?
4. Почему fairness особенно важна для кредитного скоринга, найма и медицины?
5. Что такое sensitive attribute?
6. Что такое privileged group?
7. Что такое unprivileged group?
8. Что такое proxy feature?
9. Почему удаление sensitive attribute не всегда устраняет bias?
10. Какие последствия может иметь biased-модель?

---

### 8.2. Вопросы по данным

1. Какой датасет был выбран и почему?
2. Какая целевая переменная использовалась?
3. Какие sensitive attributes были выбраны?
4. Как были определены privileged и unprivileged groups?
5. Есть ли дисбаланс классов в датасете?
6. Есть ли дисбаланс групп в датасете?
7. Как распределяется целевая переменная по группам?
8. Какие признаки могут быть proxy features?
9. Как были обработаны пропуски?
10. Как train/test split может повлиять на fairness-анализ?

---

### 8.3. Вопросы по метрикам качества

1. Какие метрики качества модели были рассчитаны?
2. Почему accuracy может быть недостаточной метрикой?
3. Что показывает precision?
4. Что показывает recall?
5. Что такое false positive?
6. Что такое false negative?
7. Какие ошибки более критичны в выбранной задаче?
8. Почему нужно считать метрики отдельно по группам?
9. Может ли модель иметь высокую accuracy и при этом быть unfair?
10. Как интерпретировать confusion matrix по группам?

---

### 8.4. Вопросы по fairness-метрикам

1. Что такое selection rate?
2. Что такое demographic parity?
3. Что показывает demographic parity difference?
4. Что показывает demographic parity ratio?
5. Что такое disparate impact?
6. Что означает правило 80%?
7. Что такое equalized odds?
8. Чем equal opportunity отличается от equalized odds?
9. Что показывает difference в false positive rate?
10. Что показывает difference в false negative rate?
11. Почему разные fairness-метрики могут конфликтовать друг с другом?
12. Можно ли одновременно оптимизировать все fairness-метрики?
13. Как выбрать fairness-метрику для конкретной предметной области?
14. Почему fairness-метрики требуют контекстной интерпретации?
15. Какие fairness-метрики были наиболее важны в вашей работе?

---

### 8.5. Вопросы по Fairlearn и AIF360

1. Для чего используется Fairlearn?
2. Что такое `MetricFrame` в Fairlearn?
3. Как в Fairlearn передается sensitive attribute?
4. Какие fairness-метрики доступны в Fairlearn?
5. Для чего используется AIF360?
6. Что такое `BinaryLabelDataset` в AIF360?
7. Что такое Reweighing в AIF360?
8. Чем Fairlearn отличается от AIF360?
9. Какие преимущества и ограничения есть у Fairlearn?
10. Какие преимущества и ограничения есть у AIF360?

---

### 8.6. Вопросы по mitigation bias

1. Какие существуют типы mitigation bias?
2. Что такое pre-processing mitigation?
3. Что такое in-processing mitigation?
4. Что такое post-processing mitigation?
5. Как работает Reweighing?
6. Как работает Threshold Optimizer?
7. Как работает Exponentiated Gradient?
8. Какой метод mitigation был выбран в вашей работе?
9. Почему был выбран именно этот метод?
10. Как изменились fairness-метрики после mitigation?
11. Как изменились метрики качества после mitigation?
12. Что такое trade-off между quality и fairness?
13. Всегда ли снижение bias улучшает модель?
14. Какие риски остаются после mitigation?
15. Какие дополнительные методы mitigation можно было бы попробовать?

---

### 8.7. Вопросы по Model Card

1. Что такое Model Card?
2. Зачем нужен аудит модели?
3. Какие разделы должны быть в Model Card?
4. Кто является целевой аудиторией Model Card?
5. Чем Model Card отличается от обычного технического отчета?
6. Какие ограничения модели должны быть описаны?
7. Что такое intended use?
8. Что такое out-of-scope use?
9. Почему важно описывать ethical considerations?
10. Какие рекомендации по использованию модели были сформулированы?
11. Какие сценарии использования модели вы запретили?
12. Какие требования к мониторингу модели вы указали?
13. Почему Model Card нужно обновлять после переобучения модели?
14. Как Model Card помогает управлять рисками?
15. Как Model Card может использоваться при production deployment?

---

## 9. Рекомендуемый итоговый результат

В результате выполнения лабораторной работы должна быть получена воспроизводимая работа, в которой:

1. Выбран и описан датасет.
2. Определены sensitive attributes.
3. Обучена baseline-модель.
4. Рассчитаны стандартные метрики качества.
5. Выполнен групповой анализ качества модели.
6. Рассчитаны fairness-метрики.
7. Сделан вывод о наличии или отсутствии bias.
8. Применен метод mitigation bias.
9. Проведено сравнение модели до и после mitigation.
10. Подготовлен Model Card.
11. Сформулированы ограничения, риски и рекомендации по использованию модели.

---

## 10. Минимальный чек-лист выполнения

Перед сдачей лабораторной работы необходимо проверить:

- [ ] Датасет загружен и описан.
- [ ] Целевая переменная определена.
- [ ] Sensitive attribute выбран и обоснован.
- [ ] Выполнен EDA.
- [ ] Выполнена предобработка данных.
- [ ] Обучена baseline-модель.
- [ ] Рассчитаны accuracy, precision, recall, F1-score.
- [ ] Выполнен анализ качества по группам.
- [ ] Рассчитаны fairness-метрики.
- [ ] Интерпретированы результаты fairness-аудита.
- [ ] Применен mitigation bias.
- [ ] Выполнено сравнение до и после mitigation.
- [ ] Подготовлен `model_card.md`.
- [ ] Сделаны выводы и рекомендации.
- [ ] Эксперимент воспроизводится по инструкции из README.