# Transport Service

## Требования
- `Python 3.12+`
- `PostgreSQL 16+`
- `venv` или другое виртуальное окружение


## Переменные окружения
Сервис читает настройки из `.env`. Для локального запуска достаточно таких переменных:

```env
DB_TRANSPORT_SERVICE_HOST=127.0.0.1
DB_TRANSPORT_SERVICE_PORT=5432
DB_TRANSPORT_SERVICE_NAME=transport_db
DB_TRANSPORT_SERVICE_USER=platform
DB_TRANSPORT_SERVICE_PASS=12345
DEBUG=false
```

Дополнительные переменные окружения будут добавляться по мере реализации функциональности сервиса.

## Локальный запуск

1. Клонируйте репозиторий и перейдите в директорию проекта:
```bash
cd transport-service
```

2. Создайте и активируйте виртуальное окружение.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта и укажите необходимые настройки.

5. Запустите сервис:

   ```bash
   uvicorn main:app --reload
   ```

## Проверка

После запуска сервис доступен по адресам:
- [http://127.0.0.1:8000api/transports/./](http://127.0.0.1:8000/api/transports/) — корневой маршрут, если он реализован.
- [http://127.0.0.1:8000/api/transports/docs](http://127.0.0.1:8000/api/transports/docs) — документация Swagger UI.
- [http://127.0.0.1:8000/api/transports/openapi.json](http://127.0.0.1:8000/api/transports/openapi.json) — схема OpenAPI.


## Миграции базы данных
Для управления миграциями используется Alembic.

### Создание миграции
После изменения моделей SQLAlchemy создай миграцию:
```bash
alembic revision --autogenerate -m "описание изменений"
```

### Применение миграций
Применить все миграции к базе данных:
```bash
alembic upgrade head
```

### Откат последней миграции
```bash
alembic downgrade -1
```

### Просмотр текущей версии
```bash
alembic current
```

### Просмотр истории миграций
```bash
alembic history
```

Перед созданием миграций убедись, что база данных доступна, а переменные окружения для подключения настроены.


## Тесты

Установка тестовых зависимостей:
```bash
pip install -r requirements.test.txt
```

Запуск тестов:
```bash
pytest
```
