FROM python:3.9.6-buster

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/