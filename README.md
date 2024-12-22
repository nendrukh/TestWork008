## Financial transaction analysis microservice

### Что делает сервис?
Сервис принимает транзакции, сохраняет в базу и отправляет задачу в очередь на обновление
статистики по транзакциям.

### Стек технологий
* FastAPI
* SQLAlchemy
* PostgreSQL
* Adminer
* Redis
* Celery
* Flower
* Pydantic
* Docker
* Docker-compose
* Pytest

### Запуск сервиса

* Запустить docker compose
```shell
docker-compose up --build
```

### Методы сервиса

* Добавление транзации

Транзакции добавляются через следующий POST запрос:
```shell
curl -H 'Content-Type: application/json' -H 'Authorization: ApiKey qwerty12345' -d '{
  "transaction_id": "99343",
  "user_id": "user_001",
  "amount": 523.50,
  "currency": "USD",
  "timestamp": "2024-12-12T12:00:00"
}' http://localhost:8000/transactions
```

Ответ от сервера:
```json
{
  "message":"Transaction received",
  "task_id":"8eec2704-bb17-4e40-9b30-f262337ac118"
}
```

* Удаление всех транзакций

По запросу DELETE удаляются все транзакции из базы и закешированные данные
```shell
curl -X 'DELETE' -H 'Authorization: ApiKey qwerty12345' http://localhost:8000/transactions
```

Ответ от сервера:
```json
{
  "message":"Transactions and cached statistics deleted"
}
```

* Получение статистики по транзакциям

Для получения статистики по транзакциям отправляется GET запрос
```shell
curl -H 'Authorization: ApiKey qwerty12345' http://localhost:8000/statistics
```

Ответ от сервера:
```json
{
    "total_transactions": 3,
    "average_transaction_amount": 684.5,
    "top_transactions": [
        {
            "transaction_id": "1",
            "amount": 1345.5
        },
        {
            "transaction_id": "6",
            "amount": 523.5
        },
        {
            "transaction_id": "2",
            "amount": 184.5
        }
    ]
}
```

### Документация api
Доступна по ссылке:
```
http://localhost:8000/docs
```
Или:
```
http://localhost:8000/redoc
```

### Мониторинг
* Также добавлен мониторинг за базой через сервис adminer:
```
http://localhost:8080/
```
System: PostgreSQL

Server: postgres

Username: some_user

Password: qwerty_pass

Database: some_db

* Для мониторинга за задачами есть Flower:
```
http://localhost:5555/
```

### Тесты

Тесты можно запустить в запущенном контейнере:
```
docker-compose exec web_app python -m pytest
```