# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Debug: show files in /app and /app/src
RUN ls -al /app && ls -al /app/src

# Set default environment file path (optional)
ENV ENV_FILE=/app/src/.env

# Run your app
CMD ["python", "src/app.py"]
