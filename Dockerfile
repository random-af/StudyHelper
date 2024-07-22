FROM python:3.10.9-slim-buster

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /

RUN source set_iam_token.sh

# add cron for updating iam_token

CMD ["python", "/src/bot/main.py"]