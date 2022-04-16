FROM ubuntu:20.04

ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y && apt install -y python3-pip postgresql alembic gcc libpq-dev

RUN python3 -m pip install --upgrade pip

COPY ./requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["/bin/bash", "-c", "./start.sh"]
