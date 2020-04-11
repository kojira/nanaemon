FROM python:3.7

RUN mkdir /var/bot
WORKDIR /var/bot
ADD . /var/bot

RUN apt update -y
RUN apt install -y locales locales-all

ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

RUN pip install -r requirements.txt
