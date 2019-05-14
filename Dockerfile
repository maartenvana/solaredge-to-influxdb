FROM python:alpine3.8

WORKDIR /app
COPY app/requirements.txt /app
RUN pip3 install -r requirements.txt

ENV INVERTER_HOST=
ENV INFLUXDB_HOST=
ENV INFLUXDB_PORT=
ENV INFLUXDB_USERNAME=
ENV INFLUXDB_PASSWORD=
ENV INFLUXDB_DATABASE=
ENV SEND_DATA_INTERVAL=60

COPY app/ /app

ENTRYPOINT [ "python", "./solaredge_to_influxdb.py"]

