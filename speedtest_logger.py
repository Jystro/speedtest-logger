from datetime import datetime
import time
import speedtest
from os import getenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

influxdb_url = "http://localhost:8086"#getenv('INFLUXDB_HOST')
influxdb_bucket = "speedtest"#getenv('INFLUXDB_BUCKET')
influxdb_organization = "org"#getenv('INFLUXDB_ORGANIZATION')
influxdb_token = ""#getenv('INFLUXDB_TOKEN')

influxdb = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_organization)
influxdb_write = influxdb.write_api(write_options=SYNCHRONOUS)

def measure():
	print("Measuring...")
	current_time = datetime.utcnow().isoformat()
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

	return


if __name__ == "__main__":
	for x in range(1):
		measure()

		#time.sleep(60 * 60)