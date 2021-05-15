# syntax=docker/dockerfile:1
# alpine does not work for psycopg2-binary, need libpq-dev

# Build a django+gunicorn image with our app 
FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
# Copy everything except those in dockerignore
COPY . /code
RUN pip install -r prodreq.txt
