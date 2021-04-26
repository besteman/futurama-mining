FROM python:3.8.9-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY /alerts .

CMD [ "python3", "main.py"]