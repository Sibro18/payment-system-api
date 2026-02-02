# Payment System API

Документация по запуску проекта двумя способами:  
- через **Docker Compose**  
- **локально**, без Docker

Проект использует:
- Python 3.13.5
- Sanic
- PostgreSQL
- SQLAlchemy + Alembic
- Pydantic
- Docker / Docker Compose

---

# 📑 Оглавление

1. [Запуск через Docker Compose](#-запуск-через-docker-compose)
2. [Локальный запуск (без Docker)](#-локальный-запуск-без-docker)
3. [Тестовые сущности](#-тестовые-сущности-пользователь-админ-аккаунт)
4. [Примечания](#-примечания)
---
# 🚀 Запуск через Docker Compose

**Убедись, что Docker и Docker Compose установлены.**
**Убедись, что порт 5432 не занят**

**Выполни команду из корня проекта:** 
`docker-compose -f docker/docker-compose.yml up --build`

Docker автоматически:
- поднимет PostgreSQL
- выполнит `docker/init.sql` (создание пользователя и базы)
- применит Alembic‑миграции
- запустит API на `http://localhost:8000
---
# 🧩 Локальный запуск (без Docker)
## 1. Создать виртуальное окружение

### Windows:
*  `python -m venv .venv`
* `.\.venv\Scripts\activate`
### Linux/macOS:
* `python3 -m venv .venv`
* `source .venv/bin/activate`
## 2. Установить зависимости

`pip install -r requirements.txt`
## 3. Запустить PostgreSQL локально

### Любой способ:
- через pgAdmin  
- через локальный сервис PostgreSQL  
- через Docker:
`docker run --name local_pg -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:16`

## 4. Выполнить SQL‑инициализацию

Выполнить `docker/init.sql` в базе: `psql -U postgres -f docker/init.sql`
(или через pgAdmin)
## 5. Применить миграции Alembic

Из корня проекта: `alembic upgrade head`

## 6. Запустить приложение

`python src/app.py`
API будет доступно на: http://localhost:8000

---

# 🧪 Тестовые сущности (пользователь, админ, аккаунт)

Ниже приведены данные, которые используются для тестирования.

```json
{
  "user": {
    "id": "11111111-1111-1111-1111-111111111111",
    "email": "user@example.com",
    "full_name": "User",
    "password": "pwd_context.hash(\"1234567890\")",
    "is_admin": false,
    "created_at": "datetime.now()",
    "updated_at": null
  },
  "admin": {
    "id": "22222222-2222-2222-2222-222222222222",
    "email": "admin@example.com",
    "full_name": "Admin",
    "password": "pwd_context.hash(\"1234567890\")",
    "is_admin": true,
    "created_at": "datetime.now()",
    "updated_at": null
  },
  "user_account": {
    "id": "33333333-3333-3333-3333-333333333333",
    "user_id": "11111111-1111-1111-1111-111111111111",
    "balance": 0.00,
    "created_at": "datetime.now()",
    "updated_at": null
  }
}
```
---
# 📌 Примечания
- Пароли хэшируются через `pwd_context.hash(<string>)`
- UUID фиксированы для удобства тестирования
- При запуске через Docker база создаётся автоматически
- При локальном запуске необходимо вручную выполнить `docker/init.sql` и миграции

Для формирования подписи можно использовать python код:
```python
import hashlib
from uuid import UUID

SECRET_KEY_WEBHOOK = "gfdmhghif38yrf9ew0jkf32"

account_id = UUID("33333333-3333-3333-3333-333333333333")
amount = 100000
transaction_id = UUID("f21549cb-8d03-41e5-8c46-fe54f77d3767")
user_id = UUID("11111111-1111-1111-1111-111111111111")

data_string = f"{account_id}{amount}{transaction_id}{user_id}{SECRET_KEY_WEBHOOK}"
signature = hashlib.sha256(data_string.encode()).hexdigest()

print("DATA STRING:", data_string)
print("SIGNATURE:", signature)
```