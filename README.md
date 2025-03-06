
1. **Клонируйте репозиторий**
   ```bash
   git clone <ссылка на репозиторий>
   cd <имя_каталога_проекта>



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
    docker exec -it testerip-converter-1 alembic upgrade head
    ```
4. **Откройте приложение** в браузере:
    - Документация Swagger: [http://localhost:7777/docs](http://localhost:7777/docs)


Главный сценарий по конвертации:
1.POST/api/exchange/offer-info
2.POST/api/exchange/confirmation
3.GET/api/exchange/offer-list
4.GET/api/exchange/in-pending

В самих ручках описаны поля на вход.
