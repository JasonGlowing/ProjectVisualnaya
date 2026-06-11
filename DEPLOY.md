# Деплой frontend + backend

## Вариант: GitHub Pages + Render

GitHub Pages запускает только статические файлы. Backend FastAPI нужно разместить отдельно, например на Render, Railway, Fly.io или VPS.

### 1. Backend на Render

1. Создай GitHub-репозиторий и загрузи весь проект.
2. На Render создай **New Web Service** из этого репозитория.
3. Build command:
   `pip install -r requirements.txt`
4. Start command:
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment variable:
   `FRONTEND_ORIGINS=https://YOUR-GITHUB-USERNAME.github.io`
6. После деплоя скопируй backend URL, например:
   `https://smart-task-planner-api.onrender.com`

### 2. Frontend на GitHub Pages

1. В папке `github-pages-frontend` открой `config.js`.
2. Замени URL на backend URL из Render:
   `window.API_BASE_URL = 'https://smart-task-planner-api.onrender.com';`
3. Загрузи содержимое папки `github-pages-frontend` в отдельный репозиторий или в ветку Pages.
4. GitHub: **Settings → Pages → Deploy from a branch → main / root**.

### 3. Проверка

Открой GitHub Pages URL. Добавление, загрузка и удаление задач должны идти через backend API.
