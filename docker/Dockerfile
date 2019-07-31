FROM python:3.7-alpine3.10

ENV PYTHONUNBUFFERED 1

# Install Python requirements.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./start /start
RUN chmod +x /start

WORKDIR /app
