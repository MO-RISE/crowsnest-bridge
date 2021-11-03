"""Main entrypoint for this application"""
from time import sleep
from environs import Env
from paho.mqtt.client import Client, MQTTv5
from paho.mqtt.subscribeoptions import SubscribeOptions

env = Env()

## Source config
MQTT_SOURCE_HOST = env("MQTT_SOURCE_HOST")
MQTT_SOURCE_PORT = env.int("MQTT_SOURCE_PORT", 1883)
MQTT_SOURCE_CLIENT_ID = env("MQTT_SOURCE_CLIENT_ID", "")
MQTT_SOURCE_TRANSPORT = env(
    "MQTT_SOURCE_TRANSPORT", "tcp", validate=lambda s: s in ("tcp", "websockets")
)
MQTT_SOURCE_TLS = env.bool("MQTT_SOURCE_TLS", False)
MQTT_SOURCE_USER = env("MQTT_SOURCE_USER", None)
MQTT_SOURCE_PASSWORD = env("MQTT_SOURCE_PASSWORD", None)

## Remote config
MQTT_REMOTE_HOST = env("MQTT_REMOTE_HOST")
MQTT_REMOTE_PORT = env.int("MQTT_REMOTE_PORT", 1883)
MQTT_REMOTE_CLIENT_ID = env("MQTT_REMOTE_CLIENT_ID", "")
MQTT_REMOTE_TRANSPORT = env(
    "MQTT_REMOTE_TRANSPORT", "tcp", validate=lambda s: s in ("tcp", "websockets")
)
MQTT_REMOTE_TLS = env.bool("MQTT_REMOTE_TLS", False)
MQTT_REMOTE_USER = env("MQTT_REMOTE_USER", None)
MQTT_REMOTE_PASSWORD = env("MQTT_REMOTE_PASSWORD", None)

# Bridging config
MQTT_TOPICS = env.list("MQTT_TOPICS", [])

# Source setup
source = Client(
    client_id=MQTT_SOURCE_CLIENT_ID, transport=MQTT_SOURCE_TRANSPORT, protocol=MQTTv5
)
source.username_pw_set(MQTT_SOURCE_USER, MQTT_SOURCE_PASSWORD)
if MQTT_SOURCE_TLS:
    source.tls_set()


# Remote setup
remote = Client(
    client_id=MQTT_REMOTE_CLIENT_ID, transport=MQTT_REMOTE_TRANSPORT, protocol=MQTTv5
)
remote.username_pw_set(MQTT_REMOTE_USER, MQTT_REMOTE_PASSWORD)
if MQTT_REMOTE_TLS:
    remote.tls_set()


SUBSCRIBE_OPTIONS = SubscribeOptions(
    qos=0,
    noLocal=True,
    retainAsPublished=False,
    retainHandling=SubscribeOptions.RETAIN_SEND_ON_SUBSCRIBE,
)


def publish_to_source(client, userdata, message):  # pylint: disable=unused-argument
    """Publish to source broker"""
    source.publish(message.topic, message.qos, message.retain)


remote.on_message = publish_to_source


def publish_to_remote(client, userdata, message):  # pylint: disable=unused-argument
    """Publish to remote broker"""
    remote.publish(message.topic, message.qos, message.retain)


source.on_message = publish_to_remote


def on_connect(
    client, userdata, flags, reason_code, properties=None
):  # pylint: disable=unused-argument
    """Subscribe on connect"""
    for topic in MQTT_TOPICS:
        client.subscribe(topic, options=SUBSCRIBE_OPTIONS, properties=None)


source.on_connect = on_connect
remote.on_connect = on_connect


# Do connection
remote.connect(MQTT_SOURCE_HOST, MQTT_SOURCE_PORT)
source.connect(MQTT_SOURCE_HOST, MQTT_SOURCE_PORT)

# Start loops
remote.loop_start()
source.loop_start()

# Just idle, this service is data-driven
while True:
    sleep(1)
