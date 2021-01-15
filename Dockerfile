FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get install default-libmysqlclient-dev
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
