FROM python:3.10-slim

WORKDIR /app

COPY api/requirements.txt requirements.txt

RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY api api
COPY utils utils

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5003"]
