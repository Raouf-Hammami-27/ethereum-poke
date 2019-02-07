FROM python:3.6

MAINTAINER Raouf Hammami <raouf.hammami@digit-u.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir /smartContract

WORKDIR /smartContract

ADD . /smartContract/

RUN pip3 install -r requirements-dev.txt