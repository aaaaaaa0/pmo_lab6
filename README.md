### 1. Полная пересборка и запуск сервисов

```bash
docker-compose down -v
```
*Останавливает и удаляет все контейнеры, сети и тома, созданные Compose. Флаг `-v` удаляет том с данными PostgreSQL, обеспечивая чистое состояние.*

```bash
docker-compose build --no-cache
```
*Пересобирает образы сервисов без использования кэша, гарантируя установку свежих зависимостей.*

```bash
docker-compose up -d
```
*Запускает контейнеры в фоновом режиме согласно описанию в `docker-compose.yml`.*


### 2. Проверка работоспособности API

```bash
docker-compose exec api pytest
```
*Выполняет тесты внутри контейнера `api`. Тесты проверяют корректность предобработки данных и успешность предсказаний.*


```bash
docker-compose exec api python -c "from app.main import app; from fastapi.testclient import TestClient; client = TestClient(app); response = client.post('/predict', json={'Pclass':1, 'Sex':'female', 'Age':30, 'SibSp':0, 'Parch':0, 'Fare':100, 'Embarked':'C', 'Name':'Test, Mrs. John'}); print(response.status_code, response.text)"
```
*Имитирует запрос к API через тестовый клиент FastAPI, не требуя внешнего сетевого доступа.*

### 3. Просмотр логов

```bash
docker-compose logs api
```
*Показывает логи контейнера `api`, включая вывод Uvicorn и возможные ошибки приложения.*


### 4. Ручное управление контейнером без Compose

```bash
docker build -t fast_api:latest .
```
*Собирает Docker-образ из текущей директории и помечает его тегом `fast_api:latest`.*

```bash
docker run -d -p 9005:8000 --name fast_api_container fast_api:latest
```
*Запускает контейнер из образа `fast_api:latest` в фоновом режиме. Порт 8000 контейнера пробрасывается на порт 9005 хоста.*

```bash
docker stop fast_api_container
```
*Останавливает работающий контейнер `fast_api_container`.*

```bash
docker rm fast_api_container
```
*Удаляет остановленный контейнер `fast_api_container`.*


### 5. Доступ к документации

После запуска сервисов документация Swagger UI доступна в браузере по адресу:  
**http://localhost:8000/docs**  
*Позволяет интерактивно отправлять запросы и просматривать описание API.*

