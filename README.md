# solaredge-to-influxdb
This projects makes it easy to capture output from a Solar Edge inverter and send it to influxdb

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=maartenvana_solaredge-to-influxdb&metric=alert_status)](https://sonarcloud.io/dashboard?id=maartenvana_solaredge-to-influxdb)
![Docker Pulls](https://img.shields.io/docker/pulls/maartenvana/solaredge-to-influxdb)

# Building the container
```
docker build -t solaredge-to-influxdb .
```

# Running the container
If everything is set correctly the script will push data every 60 seconds (by default) to influxdb
```
docker run -d \
    --name solaredge-to-influxdb \
    --restart=always \
    -e "INVERTER_HOST=" \
    -e "INFLUXDB_HOST=" \
    -e "INFLUXDB_PORT=" \
    -e "INFLUXDB_USERNAME=" \
    -e "INFLUXDB_PASSWORD=" \
    -e "INFLUXDB_DATABASE=" \
    solaredge-to-influxdb
```

# Additional environment variables
Set a custom interval for sending data to influx db (in seconds)
```
SEND_DATA_INTERVAL=60
```

# Special thanks
[Original script](https://gitlab.com/snippets/1853864#L9) created by Pim van den Berg [@pomni](https://gitlab.com/pommi) 
