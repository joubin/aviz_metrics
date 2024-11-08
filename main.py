import asyncio

from aiohttp import ClientSession

from pyairvisual.node import NodeSamba
from prometheus_client import start_http_server, Gauge

from prometheus_client import start_http_server, Gauge
import time
import os
address = os.getenv("AIR_QUALITY_NODE_IP_ADDRESS")
token = os.getenv("AIR_QUALITY_NODE_PASSWORD")
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
    measurements = data.get('measurements', {})
    status = data.get('status', {})
    
    # Update each gauge with current data
    gauge_co2.set(float(measurements.get('co2', 0)))
    gauge_humidity.set(float(measurements.get('humidity', 0)))
    gauge_pm2_5.set(float(measurements.get('pm2_5', 0)))
    gauge_temperature_C.set(float(measurements.get('temperature_C', 0)))
    gauge_temperature_F.set(float(measurements.get('temperature_F', 0)))
    gauge_voc.set(float(measurements.get('voc', 0)))
    gauge_battery.set(float(status.get('battery', 0)))
    gauge_wifi_strength.set(float(status.get('wifi_strength', 0)))



async def main() -> None:
    """Run!"""
    while True:
        print("Updating metrics...")
        async with NodeSamba(address, token) as node:
            measurements = await node.async_get_latest_measurements()
            update_metrics(measurements)
            time.sleep(60)
        # Can take some optional parameters:
        #   1. include_trends: include trends (defaults to True)
        # #   2. measurements_to_use: the number of measurements to use when calculating
        # #      trends (defaults to -1, which means "use all measurements")
        # history = await node.async_get_history()
        # with open("data.json", mode="w") as output:
        #     import json
        #     json.dump(history, output)


asyncio.run(main())