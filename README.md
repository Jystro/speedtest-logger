## Basic speed logger using speedtest-cli and Influxdb

A basic Docker logger that uses speedtest-cli module for Python and Influxdb to monitor your internet speed periodically

## Usage

Just clone the repository with git and set the environmental variables before using docker-compose to start the stack. As an alternative, edit `docker-compose.yml` to manually set the env variables

You can then go to https://yourIP:8086 and login to edit the dashboard

## Dashboard

![Dashboard](img/dashboard.png)
<br/><br/><br/><br/>
The JSON file to upload to produce this dashboard is available [here](https://github.com/Jystro/speedtest-logger/blob/main/speed-logger.json)

Otherwise, the dashboard is produced using the following Flux query for the graph:

```flux
from(bucket: "speedtest")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "download" or r._measurement == "upload" or r._measurement == "ping" and r._field == "value")
  |> map(
    fn: (r) => ({r with
      _value: if r._measurement == "ping" then r._value
      else r._value / 1048576.0
      })
  )
  |> group(columns: ["_measurement"])
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

<br/>

And this query for the gauges:

```Flux
from(bucket: "speedtest")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "download" and r._field == "value")
  |> map(fn: (r) => ({r with _value: r._value / 1048576.0}))
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "last")
```

<br/><br/>
Change `r["_measurement"]` according to the measurement

Remove the line

```
  |> map(fn: (r) => ({r with _value: r._value / 1048576.0}))
```

for the ping
