FROM python:3.10.0-alpine

COPY ./requirements.txt /app/requirements.txt

EXPOSE 5000

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "app.py" ]