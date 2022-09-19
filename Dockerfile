FROM ubuntu:latest
MAINTAINER Danil Kravcov 'dan.craw@yandex,ru'
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
