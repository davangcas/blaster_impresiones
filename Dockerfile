FROM python:3.11.4-alpine3.18

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && apk add --no-cache gcc musl-dev postgresql-dev libffi-dev

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . /app/

CMD ["sh", "app_init.sh"]
