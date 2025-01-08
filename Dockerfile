FROM python:3.9-slim-buster

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["fastapi", "run", "main.py", "--host", "127.0.0.1", "--port", "8080"]