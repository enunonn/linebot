FROM python:3.9-slim-buster

RUN mkdir /backend
COPY . /backend
WORKDIR /backend

RUN apt-get -y update
RUN apt-get -y upgrade

RUN pip install -r requirements.txt

CMD ["python", "server.py"]