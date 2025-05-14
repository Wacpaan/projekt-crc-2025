# Używamy lekkiego obrazu Pythona
FROM python:3.11-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki do kontenera
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Domyślna komenda startowa
CMD ["python", "src/app.py"]

ENV ENV_FILE=/app/src/.env


# how to start
# docker build -t space-bot .
# docker run --env-file .env space-bot