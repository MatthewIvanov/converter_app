
FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd

RUN mkdir /converter
WORKDIR /converter


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh


RUN chmod +x ./app/docker/app.sh


CMD ["/wait-for-db.sh", "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
