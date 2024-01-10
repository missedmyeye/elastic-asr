FROM python:3.10

WORKDIR /app

# Copying 
COPY elastic-backend/requirements.txt .
COPY asr/cv-valid-dev.csv .

RUN pip install --no-cache-dir -r requirements.txt

COPY elastic-backend .

CMD ["python", "cv-index.py"]
