# Контрольная работа №4

Проект закрывает задания КР №4:

- **9.1** — Alembic + миграции БД для `Product`.
- **10.1** — пользовательские исключения `CustomExceptionA`, `CustomExceptionB` и обработчики ошибок.
- **10.2** — Pydantic-валидация входных данных и кастомный обработчик ошибок валидации.
- **11.1 / 11.2** — модульные и асинхронные тесты через `pytest`, `pytest-asyncio`, `httpx.AsyncClient`, `ASGITransport`, `Faker`.

## 1. Установка

```bash
python -m venv venv
```

Windows PowerShell:

```bash
venv\Scripts\activate
```

Git Bash:

```bash
source venv/Scripts/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## 2. Миграции Alembic

Применить миграции:

```bash
alembic upgrade head
```

Проверить историю миграций:

```bash
alembic history
```

Текущая версия БД:

```bash
alembic current
```

В проекте уже есть 2 миграции:

1. `0001_create_products.py` - создаёт таблицу `products` с полями `id`, `title`, `price`, `count`.
2. `0002_add_product_description.py` - добавляет поле `description NOT NULL`.

## 3. Запуск приложения

```bash
uvicorn app.main:app --reload
```

После запуска открыть:

```text
http://127.0.0.1:8000/docs
```

## 4. Проверка основной функциональности

### Создать продукт

POST `/products`

```json
{
  "title": "Keyboard",
  "price": 120.5,
  "count": 3,
  "description": "Mechanical keyboard"
}
```

Ожидаемый результат: `201 Created`.

### Получить продукт

GET `/products/1`

Ожидаемый результат: `200 OK`.

Если продукта нет, будет кастомная ошибка `CUSTOM_B`.

### Проверка CustomExceptionA

GET `/errors/check-age/16`

Ожидаемый результат: `400 Bad Request`.

### Проверка CustomExceptionB

GET `/errors/resource/999`

Ожидаемый результат: `404 Not Found`.

### Проверка Pydantic-валидации

POST `/validate-user`

Валидный пример:

```json
{
  "username": "student",
  "age": 20,
  "email": "student@mirea.ru",
  "password": "password123",
  "phone": "+79990000000"
}
```

Невалидный пример:

```json
{
  "username": "student",
  "age": 15,
  "email": "bad-email",
  "password": "123"
}
```

Ожидаемый результат: `422 Unprocessable Entity` с кастомным JSON-ответом.
