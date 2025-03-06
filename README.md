
1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/MatthewIvanov/converter_app.git
   cd converter_app



### 🔧 Установка и запуск с Docker


1. **Создайте файл `.env-non-dev`** на основе закомментированного шаблона в файле `.env-non-dev`:
    ```plaintext
    postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}
    ...
    ```

2. **Соберите и запустите контейнеры**:
    ```bash
    docker-compose up --build
    ```
3. **Затем прописать в командой строке**:
    ```bash
    docker exec -it converter_app-converter-1 alembic upgrade head
    ```
4. **Откройте приложение** в браузере:
    - Документация Swagger: [http://localhost:7777/docs](http://localhost:7777/docs)


### Главный сценарий по конвертации:
1. **POST/api/exchange/offer-info - получить информацию о сделке** 
2. **POST/api/exchange/confirmation - подтверждение сделки**
3. **GET/api/exchange/offer-list - получить список всех сделок**
4. **GET/api/exchange/in-pending - сделки в обработке**

В самих ручках описаны поля на вход.
