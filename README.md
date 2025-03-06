
1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/MatthewIvanov/converter_app.git
   cd converter_app



### 🔧 Установка и запуск с  Docker



1. **Соберите и запустите контейнеры**:
    ```bash
    docker-compose up --build
    ```
2. **Затем прописать в командой строке**:
    ```bash
    docker exec -it converter_app-converter-1 alembic upgrade head
    ```
3. **Откройте приложение** в браузере:
    - Документация Swagger: [http://localhost:7777/docs](http://localhost:7777/docs)


### Главный сценарий по конвертации:
**GET/api/get_rates - получить информацию о курсах**

1. **POST/api/exchange/offer-info - получить информацию о сделке** 
2. **POST/api/exchange/confirmation - подтверждение сделки**
3. **GET/api/exchange/offer-list - получить список всех сделок**
4. **GET/api/exchange/in-pending - сделки в обработке**

В самих ручках описаны поля на вход.
