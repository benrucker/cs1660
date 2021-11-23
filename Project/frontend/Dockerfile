FROM python:3.10.0-alpine
COPY app.py /home/app/app.py
COPY requirements.txt /home/app/requirements.txt
WORKDIR /home/app/
RUN pip install -r requirements.txt
CMD exec /bin/sh -c "trap : TERM INT; sleep 9999999999d & wait"
