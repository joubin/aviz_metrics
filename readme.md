# Prometheus Exporter for Air Visual Device

Assuming you have an Air Visual Device, this will allow you to read the current sensor measurements. 

On the settings, in the PRO Screen, get the password provided. For more info see https://github.com/bachya/pyairvisual?tab=readme-ov-file#installation


## Running in Docker

Create a `.env` file with the following contents:

```
AIR_QUALITY_NODE_PASSWORD:asdasd
AIR_QUALITY_NODE_IP_ADDRESS:192.168.1.76
```

docker run -d --name airvisual-exporter --env-file.env -p 8000:8000