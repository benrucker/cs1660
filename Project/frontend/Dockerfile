FROM python:3.10.0-alpine
COPY app.py /home/app/app.py
WORKDIR /home/app/
CMD exec /bin/sh -c "trap : TERM INT; sleep 9999999999d & wait"
