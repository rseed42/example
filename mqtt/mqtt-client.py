#!/usr/bin/python3
import paho.mqtt.client as mqtt
# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
# Client parameters
CLIENT_ID = 'python-paho-test-client'
PROTOCOL_VERSION = mqtt.MQTTv311

# Connection parameters
# BROKER_URI = 'iot.eclipse.org'
BROKER_URI = 'broker.hivemq.com'

# Connection error codes
# 0: Connection successful
# 1: Connection refused – incorrect protocol version
# 2: Connection refused – invalid client identifier
# 3: Connection refused – server unavailable
# 4: Connection refused – bad username or password
# 5: Connection refused – not authorised
# 6-255: Currently unused.

# Data parameters
# Multi-level wild card:
# TOPIC_NAME = '#'
# Single level wild card:
TOPIC_NAME = '/test/#'

# ------------------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    print('-- connect --')
    if rc == 0:
        print('Connected Established: {0}'.format(rc))
        client.subscribe(TOPIC_NAME)
    else:
        print('Connection failed: {0}'.format(rc))


def on_message(client, userdata, msg):
    try:
        print(msg.topic)
        print(msg.payload.decode('utf-8', 'ignore'))
    except UnicodeDecodeError:
        pass

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Instantiate mqtt client object
    client = mqtt.Client(
        CLIENT_ID,
        clean_session=True,
        userdata=None,
        protocol=mqtt.MQTTv311,
        transport='tcp'
    )
    # Establish a connection
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_URI)

    # Run the script
    client.loop_forever()
