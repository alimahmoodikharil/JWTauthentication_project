FROM python:latest

ENV DONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code/
