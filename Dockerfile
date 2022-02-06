FROM python:3.8.2-alpine

USER root

WORKDIR /root

RUN apk add --update --no-cache py3-numpy ffmpeg sox musl-dev linux-headers g++

COPY requirements.txt /root/
RUN pip install -r requirements.txt

COPY pyporwave.py /root/
ENTRYPOINT ["python3", "pyporwave.py"]
