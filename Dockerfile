FROM python:3.11-bullseye
ENV PYTHONUNBUFFERED 1
ADD . /CES
WORKDIR /CES
RUN apt-get update && \
  apt-get install libpq-dev -y && \
  python -m pip --no-cache install -U pip && \
  #    python -m pip --no-cache install Cython && \
  #    python -m pip --no-cache install numpy && \
  python -m pip --no-cache install -r requirements.txt

EXPOSE 8001
