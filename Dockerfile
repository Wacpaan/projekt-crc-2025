# Use a lightweight Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files and .env
COPY . .
COPY src/.env src/.env  

# Optional: show files for debugging
RUN ls -al /app/src

# Start the app
CMD ["python", "src/app.py"]
