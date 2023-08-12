FROM python:3.11

ADD . /app

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt