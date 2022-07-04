FROM python:3.7-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
ENV unix_socket /var/run/mysqld/mysqld2.sock

RUN apt update && apt install build-essential -y
RUN pip install -r requirements.txt

COPY sensor_client .

CMD ["python", "sensor_client.py"]
