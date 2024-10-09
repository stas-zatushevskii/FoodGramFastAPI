FROM python:3.10-alpine

RUN apk add --no-cache build-base

RUN pip3 install asyncpg

WORKDIR code
COPY requirements.txt .

RUN python3 -m pip install --upgrade pip \
    && pip3 install setuptools \
    && pip3 install -r /code/requirements.txt --no-cache-dir
COPY . .
CMD gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000