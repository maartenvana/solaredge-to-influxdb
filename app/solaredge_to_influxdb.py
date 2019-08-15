#!/usr/bin/env python3

# Original source: https://gitlab.com/snippets/1853864#L9
import datetime
import os
import time
from solaredge_local import SolarEdge
from google.protobuf.json_format import MessageToDict
from influxdb import InfluxDBClient

print("Inverter is located at: " + os.environ['INVERTER_HOST'])
print("Writing to influx database \"" + os.environ['INFLUXDB_DATABASE'] + "\" at " + os.environ['INFLUXDB_HOST'] + ":" + os.environ['INFLUXDB_PORT'])

se_client = SolarEdge("http://" + os.environ['INVERTER_HOST'])
influx_client = InfluxDBClient(os.environ['INFLUXDB_HOST'], os.environ['INFLUXDB_PORT'], os.environ['INFLUXDB_USERNAME'], os.environ['INFLUXDB_PASSWORD'], os.environ['INFLUXDB_DATABASE'])

def influx(fields):
    json_body = [
        {
            "measurement": "solaredge",
            "time": datetime.datetime.utcnow().replace(microsecond=0).isoformat(),
            "fields": fields,
        }
    ]
    try:
        influx_client.write_points(json_body)
    except Exception as e:
        log('Failed to write to influxdb: ', e)

def get_solaredge_status_data():
    try:
        status = se_client.get_status()
        return MessageToDict(status)
    except Exception as e:
        log('Failed to get status from SolarEdge inverter: ', e)
        return

def construct_measurements(data):
    measurements = {
        "energy_total": data["energy"]["total"],
        "energy_today": data["energy"].get("today", 0.0),
        "energy_thisyear": data["energy"].get("thisYear", 0.0),
        "energy_thismonth": data["energy"].get("thisMonth", 0.0),
        "frequency": data["frequencyHz"],
        "optimizers_online": data["optimizersStatus"].get("online", 0),
        "optimizers_total": data["optimizersStatus"].get("total", 0),
        "inverter_temperature": data["inverters"]["primary"]["temperature"].get("value", 0),
        "inverter_voltage": data["inverters"]["primary"].get("voltage", 0.0),
        "power_limit": data.get("powerLimit", 0.0),
        "power_watt": data.get("powerWatt", 0.0),
        "voltage": data["voltage"],
    }
    return measurements

def log(message, exception):
    if exception is None:
        print("[" + str(datetime.datetime.utcnow())+ "] " + message)
    else:
        print("[" + str(datetime.datetime.utcnow())+ "] " + message, exception)

while True:
    se_status_data = get_solaredge_status_data()
    if se_status_data is None:
        log("SolarEdge status data is None", None)
        time.sleep(10)
        continue
    se_measurements = construct_measurements(se_status_data)
    influx(se_measurements)
    log("Sent data to influxdb", None)
    time.sleep(int(os.environ['SEND_DATA_INTERVAL']))