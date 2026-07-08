FROM python:3.12-slim

# Put code in /opt/app so it doesn't get shadowed if a volume is mounted at /app
WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the data directory exists for the SQLite database
RUN mkdir -p /app/data

CMD ["python", "run.py"]
