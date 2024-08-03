FROM python:3.9-slim AS builder

WORKDIR /app

COPY . .

RUN pip install wheel gunicorn flask deep-translator 

#FROM builder

#WORKDIR /app

#COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

#COPY --from=builder /app/* .

EXPOSE 5001

CMD gunicorn --bind 0.0.0.0:5001 --workers=2 wsgi:app
