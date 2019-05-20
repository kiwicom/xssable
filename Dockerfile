FROM python:3.7.2-alpine3.8

WORKDIR /app
COPY requirements.txt /app/

RUN \
    apk add --no-cache gcc musl-dev libffi libffi-dev && \
    pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "app.py"]
