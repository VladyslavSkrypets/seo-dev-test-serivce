FROM python:3.9-slim-buster

ADD ./web /app/web

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade setuptools pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "web.main"]
