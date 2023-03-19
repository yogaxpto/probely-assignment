FROM python:3

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000