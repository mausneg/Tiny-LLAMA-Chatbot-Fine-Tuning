FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt


COPY app app

COPY saved_models/TinyLlama-1.1B-Chat-v1.1 saved_models/TinyLlama-1.1B-Chat-v1.1

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5003"]
