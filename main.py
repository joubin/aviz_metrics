import asyncio

from aiohttp import ClientSession

from pyairvisual.node import NodeSamba
from prometheus_client import start_http_server, Gauge

from prometheus_client import start_http_server, Gauge
import time
import os
address = os.getenv("AIR_QUALITY_NODE_IP_ADDRESS")
print(address)

token = os.getenv("AIR_QUALITY_NODE_PASSWORD")
refresh_rate = int(os.getenv("AIR_QUALITY_REFRESH_REATE", 60))
metrics_port = int(os.getenv('AIR_QUALITY_METRICS_PORT', 8000))

gauge_co2 = Gauge('air_quality_co2', 'CO2 levels in ppm')
gauge_humidity = Gauge('air_quality_humidity', 'Humidity level in percentage')
gauge_pm2_5 = Gauge('air_quality_pm2_5', 'PM2.5 level in µg/m³')
gauge_temperature_C = Gauge('air_quality_temperature_celsius', 'Temperature in Celsius')
gauge_temperature_F = Gauge('air_quality_temperature_fahrenheit', 'Temperature in Fahrenheit')
gauge_voc = Gauge('air_quality_voc', 'VOC levels')
gauge_battery = Gauge('air_quality_device_battery', 'Battery level in percentage')
gauge_wifi_strength = Gauge('air_quality_device_wifi_strength', 'WiFi signal strength')

# Start Prometheus server
start_http_server(8000)

# Update Prometheus metrics with data
def update_metrics(data):
    def test_before_update(g:Gauge, d:dict, key:str):
        if key in d.keys():
            g.set(float(d.get(key)))
        else:
            print(f"Missing Key {key} in {d}")
    measurements = data.get('measurements', {})
    status = data.get('status', {})
    # Update each gauge with current data
    test_before_update(g=gauge_co2, d=measurements, key='co2')
    test_before_update(g=gauge_humidity, d=measurements, key='humidity')
    test_before_update(g=gauge_pm2_5, d=measurements, key='pm2_5')
    test_before_update(g=gauge_temperature_C, d=measurements, key='temperature_C')
    test_before_update(g=gauge_temperature_F, d=measurements, key='temperature_F')
    test_before_update(g=gauge_voc, d=measurements, key='voc')



async def main() -> None:
    """Run!"""
    while True:
        print("Updating metrics...")
        time.sleep(refresh_rate)
        async with NodeSamba(address, token).async_connect(timeout=60) as node:
            update_metrics(await node.async_get_latest_measurements())
        # Can take some optional parameters:
        #   1. include_trends: include trends (defaults to True)
        # #   2. measurements_to_use: the number of measurements to use when calculating
        # #      trends (defaults to -1, which means "use all measurements")
        # history = await node.async_get_history()
        # with open("data.json", mode="w") as output:
        #     import json
        #     json.dump(history, output)


asyncio.run(main())