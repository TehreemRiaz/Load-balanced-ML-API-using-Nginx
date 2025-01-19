# Use a lightweight Python base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python scripts into the container
WORKDIR /app
COPY load_test.py .
COPY monitor.py .

# Default command (can be overridden by docker-compose.yml)
CMD ["python", "monitor.py"]
