# Simple Smart Task Planner

Очень простой backend-проект для задания **Smart Task Planner**.

Проект специально упрощен: вся логика находится в одном файле `main.py`.

## Что есть в проекте

- FastAPI backend
- SQLite база данных
- создание задач
- просмотр задач
- отметка задачи как выполненной
- удаление задачи
- простая "AI"-категоризация по ключевым словам
- простая оценка времени выполнения
- Swagger-документация

## Структура

```text
simple-smart-task-planner/
├─ main.py
├─ requirements.txt
├─ README.md
└─ AI_ASSISTANT_LOG.md
```

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn main:app --reload
```

## Открыть API

После запуска открой в браузере:

```text
http://127.0.0.1:8000/docs
```

## Пример создания задачи

В Swagger открой:

```text
POST /tasks
```

Body:

```json
{
  "title": "Учить FastAPI",
  "description": "Пройти урок по FastAPI и сделать конспект",
  "complexity": "medium"
}
```

Ответ будет примерно такой:

```json
{
  "id": 1,
  "title": "Учить FastAPI",
  "description": "Пройти урок по FastAPI и сделать конспект",
  "category": "обучение",
  "estimated_minutes": 30,
  "complexity": "medium",
  "completed": false
}
```

## Важно

В этом упрощенном проекте нет настоящего OpenAI API.  
Вместо него используется простая имитация AI-логики через функции:

- `guess_category()`
- `estimate_minutes()`

Это сделано, чтобы проект легко запускался без API-ключей.
