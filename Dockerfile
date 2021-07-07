FROM python:3.8.9-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=flaskr
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=$PORT

RUN flask init-db

CMD [ "flask", "run", "--host=0.0.0.0"]