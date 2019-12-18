FROM jupyter/scipy-notebook:latest

USER root

RUN apt-get update && apt-get install -y ffmpeg sox
RUN pip install virtualenv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pyporwave.py .
ENTRYPOINT ["python3", "pyporwave.py"]
