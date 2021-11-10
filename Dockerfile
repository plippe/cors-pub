FROM python:3.10-alpine

ENV PYTHONUNBUFFERED True
ENV PIPENV_VENV_IN_PROJECT 1

RUN pip3 install pipenv

COPY Pipfile.lock ./

RUN pipenv sync

COPY . ./

ENTRYPOINT pipenv run gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
