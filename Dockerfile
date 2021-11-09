FROM python:3.10-alpine

ENV PYTHONUNBUFFERED True
ENV PIPENV_VENV_IN_PROJECT 1

RUN pip3 install pipenv

COPY Pipfile.lock ./

RUN pipenv sync

COPY . ./

ENTRYPOINT PORT=${PORT} pipenv run python app.py
