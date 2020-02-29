FROM python:3.7.3
MAINTIANER Lucky Adogun

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /requirements.txt
COPY ./requirements-prod.txt /requirements-prod.txt
RUN pip install -r /requirements-prod.txt

RUN mkdir /project
WORKDIR /project
COPY . /project/ /project

RUN adduser -D user
USER user