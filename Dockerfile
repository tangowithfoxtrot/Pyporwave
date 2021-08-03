FROM python:slim-buster

USER root

WORKDIR /root

RUN apt-get update && apt-get install -y ffmpeg sox

COPY requirements.txt /root/
RUN pip install -r requirements.txt

COPY pyporwave.py /root/
ENTRYPOINT ["python3", "pyporwave.py"]

