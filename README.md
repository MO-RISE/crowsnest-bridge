# crowsnest-bridge-mqtt

Two-way bridging of messages between two crowsnest mqtt brokers using MQTTv5.

Automatically built as a docker image. Available [here](https://github.com/MO-RISE/crowsnest-bridge-mqtt/pkgs/container/crowsnest-bridge-mqtt)

## Example docker-compose setup

<details>
  <summary>docker-compose.yml</summary>
  
```yaml
version: "3"

services:

    crowsnest-bridge-mqtt:
        image: ghcr.io/mo-rise/crowsnest-bridge-mqtt
        restart: unless-stopped
        environment:
            - MQTT_SOURCE_HOST=localhost
            - MQTT_SOURCE_PORT=1883
            - MQTT_REMOTE_HOST=broker.test.com
            - MQTT_REMOTE_PORT=443
            - MQTT_REMOTE_TRANSPORT=websockets
            - MQTT_REMOTE_TLS=true
            - MQTT_REMOTE_USER=<username>
            - MQTT_REMOTE_PASSWORD=<password>
```
</details>

## Development
Requires:
* python >= 3.8
* docker and docker-compose
* vscode (optional, but very handy) (with python and docker extensions)

Install the python requirements in a virtual environment:
```cmd
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
```

### Run linters
```cmd
black app tests
pylint app
```

### Run testsuite
```cmd
pytest tests/
```
