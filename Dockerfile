FROM python:3.11-bullseye
ENV PYTHONUNBUFFERED 1
ADD . /ces
WORKDIR /ces
RUN apt-get update && \
  apt-get install libpq-dev -y && \
  python -m pip --no-cache install -U pip && \
  pip install PyJWT && \  # Adicione esta linha para instalar o PyJWT
  python -m pip --no-cache install -r requirements.txt

EXPOSE 8001
