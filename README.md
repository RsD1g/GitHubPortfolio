# Portfolio Site

## Описание
Это портафолио, автоматически показывающее публичные репозитории GitHub пользователя с гибкой темой.

## Запуск

### 1. Подготовка .env
Скопируйте содержимое `.env.example` в `.env` и заполните:
- `GITHUB_TOKEN` – токен доступа к GitHub (для синхронизации)
- `GITHUB_USERNAME` – ваш логин GitHub
- `ADMIN_TOKEN` – токен для админской синхронизации
- `DATABASE_URL` – строка подключения к PostgreSQL
- `REDIS_URL` – строка подключения к Redis
- `CORS_ORIGINS` – списки URL фронтенда (по умолчанию `http://localhost:5173,http://localhost:8080`)
- `SYNC_HOUR_UTC` – час синхронизации (по умолчанию 4)

### 2. Запуск Docker
```bash
docker compose up --build -d
```

### 3. Проверка
- `curl http://localhost:8000/api/health` – должен вернуть `{"status":"ok"}`.
- `cd frontend && npm run build` – сборка без ошибок.

## Структура проекта
```
portfolio/
├── backend/
│   └── backend.py
├── frontend/
│   └── src/...
├── docker-compose.yml
├── .env.example
└── README.md
```

## Дальнейшие шаги
- Настроить GitHub Actions CI.
- Добавить тесты.
- Реализовать синхронизацию с GitHub.