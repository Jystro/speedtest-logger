FROM alpine

COPY requirements.txt speedtest_logger.py /app/

WORKDIR /app

RUN apk add --update --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python

RUN pip install -r requirements.txt

#CMD ["ping", "localhost"]
CMD ["python", "speedtest_logger.py"]