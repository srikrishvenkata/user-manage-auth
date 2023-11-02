FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install redis pymongo flask

COPY . .

ENV FLASK_APP=server.py
ENV MONGODB_HOST=192.168.0.105
ENV MONGODB_PORT=27017
ENV REDIS_HOST=192.168.0.105
ENV REDIS_PORT=6379
CMD [ "flask", "run", "--host=0.0.0.0"]