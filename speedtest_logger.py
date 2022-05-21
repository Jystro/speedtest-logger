from datetime import datetime
import time
import speedtest
from os import getenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

influxdb_url = "http://influxdb:8086"
influxdb_bucket = getenv('BUCKET')
influxdb_organization = getenv('ORG')
influxdb_token = getenv('TOKEN')

influxdb = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_organization)
influxdb_write = influxdb.write_api(write_options=SYNCHRONOUS)

def measure():
	print("Measuring...")
	test = speedtest.Speedtest()
	test.get_best_server()
	test.download()
	test.upload()

	print("Saving results...")
	res = test.results.dict()
	server = res.get("server")

	p = influxdb_client.Point("download").tag("lat", server.get("lat")).tag("lon", server.get("lon")).tag("id", server.get("id")).field("value", res.get("download"))
	influxdb_write.write(bucket=influxdb_bucket, org=influxdb_organization, record=p)
	p = influxdb_client.Point("upload").tag("lat", server.get("lat")).tag("lon", server.get("lon")).tag("id", server.get("id")).field("value", res.get("upload"))
	influxdb_write.write(bucket=influxdb_bucket, org=influxdb_organization, record=p)
	p = influxdb_client.Point("ping").tag("lat", server.get("lat")).tag("lon", server.get("lon")).tag("id", server.get("id")).field("value", res.get("ping"))
	influxdb_write.write(bucket=influxdb_bucket, org=influxdb_organization, record=p)
	p = influxdb_client.Point("server").tag("id", server.get("id")).field("lat", float(server.get("lat"))).field("lon", float(server.get("lon")))
	influxdb_write.write(bucket=influxdb_bucket, org=influxdb_organization, record=p)


if __name__ == "__main__":
	interval = int(getenv("INTERVAL"))
	while True:
		measure()
		time.sleep(interval)