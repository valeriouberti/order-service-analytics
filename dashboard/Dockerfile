FROM python:3.11
LABEL authors="valeriouberti"

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app

EXPOSE 8000

CMD ["gunicorn", "app:server", "--host", "0.0.0.0", "--port", "8000"]
