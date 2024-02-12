"""
Based on `mqtt_shared_feeds.py` example from repository: https://github.com/adafruit/Adafruit_IO_Python
"""

# Import standard python modules.
import sys
import time
import random

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_USERNAME = "Karlan"
ADAFRUIT_IO_KEY = "fakeapikey"
IO_FEED = "Test"


def disconnected(client):
    """Disconnected function will be called when the client disconnects."""
    print("Disconnected from Adafruit IO!")
    sys.exit(1)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_disconnect = disconnected

# Connect to the Adafruit IO server.
client.connect()

client.loop_background()
print("Publishing a new message every 10 seconds (press Ctrl-C to quit)...")

while True:
    value = random.randint(0, 100)
    print("Publishing {0} to {1}.".format(value, IO_FEED))
    client.publish(IO_FEED, value)
    time.sleep(10)
