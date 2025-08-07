FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD sh -c "python manage.py makemigrations && \
           python manage.py migrate && \
           python manage.py runserver 0.0.0.0:8000"