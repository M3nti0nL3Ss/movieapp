FROM python:3.10.14-alpine3.20
LABEL maintainer="m3nti0nl3ss"

ENV PYTHONUNBUFFERED 1

ARG DEV=false
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY . /backend
WORKDIR /backend
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt;\
    fi && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user 

ENV PATH="/py/bin:$PATH"

USER django-user
