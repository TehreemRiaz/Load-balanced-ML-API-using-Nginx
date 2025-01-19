FROM python:3.9-slim

WORKDIR /app/

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY ./iris_model.pkl ./iris_model.pkl
COPY ./app.py .
COPY ./templates ./templates 

EXPOSE 5004

CMD ["python", "app.py"]
