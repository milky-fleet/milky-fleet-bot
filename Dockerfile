FROM python:3.7-alpine

# Set WORKDIR
WORKDIR /usr/local/milky-fleet-bot

# Set env variables
ENV PYTHONUNBUFFERED 1
COPY . /usr/local/milky-fleet-bot

# Add runtime dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev libressl-dev\
    && pip install -r requirements.txt

CMD python bot.py
