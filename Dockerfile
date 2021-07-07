FROM python:3.8.9-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=flaskr
ENV FLASK_ENV=production

RUN flask init-db

CMD [ "waitress-serve", "--call", "'app/flaskr:create_app'"]