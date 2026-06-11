# Smart Task Planner

Клиентский веб-сайт и API для AI-планировщика задач на FastAPI + SQLite.

## Что внутри

- Современный адаптивный клиентский сайт на HTML/CSS/JavaScript
- Создание, просмотр, поиск, фильтрация и удаление задач
- Статистика по задачам: количество, минуты, сложные задачи, фокус дня
- Быстрые шаблоны задач
- AI-категоризация и оценка времени на backend
- Swagger/OpenAPI документация
- Pytest-тесты

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска откройте:

- Сайт: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs

## Тесты

```bash
pytest
```
