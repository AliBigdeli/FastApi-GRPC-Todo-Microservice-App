FROM python:3.10-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --upgrade pip  && \
    pip install --no-cache-dir -r requirements.txt

COPY ./main.py .