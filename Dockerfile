#FROM python:slim-buster
FROM python:3.8.2-alpine

USER root

WORKDIR /root

#RUN apt-get update && apt-get install -y ffmpeg sox
RUN apk add --update --no-cache py3-numpy ffmpeg sox musl-dev linux-headers g++

#gcc

COPY requirements.txt /root/
RUN pip install -r requirements.txt

COPY pyporwave.py /root/
ENTRYPOINT ["python3", "pyporwave.py"]
