FROM python:3.9-slim AS builder

WORKDIR /app

COPY . .

RUN pip install wheel gunicorn flask deep-translator 

EXPOSE 5001

CMD gunicorn --bind 0.0.0.0:5001 --workers=2 wsgi:app
