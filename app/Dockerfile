FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt

RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app app

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]