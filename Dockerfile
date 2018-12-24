FROM python:3.6-alpine
MAINTAINER intelivix

ENV PIPENV_VENV_IN_PROJECT=1

RUN apk update \
        && apk add --no-cache git openssh-client \
        && pip install pipenv \
        && addgroup -S -g 1001 app \
        && adduser -S -D -h /app -u 1001 -G app app

RUN mkdir /app/src
COPY . /app/src/
RUN chown -R app.app /app/
WORKDIR /app/src
RUN pipenv install --deploy --ignore-pipfile
USER app

CMD ["/app/src/.venv/bin/python", "-m", "workers"]
