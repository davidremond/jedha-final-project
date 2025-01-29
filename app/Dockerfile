FROM python:3.13-slim

RUN apt update \
    && apt install build-essential gcc g++ python3-dev -y

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --prefer-binary

COPY ./src .

EXPOSE $DEFAULT_PORT

CMD ["streamlit", "run", "app.py", "--server.port=7860"]