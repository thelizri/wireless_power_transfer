import serial
import sys
import time
import re
import requests
from Adafruit_IO import MQTTClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration for the serial port
SERIAL_PORT = "/dev/tty.usbmodem143301"
BAUD_RATE = 19200

# Adafruit IO Configuration
ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME")
ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY")

# URL to our own API
REST_API_URL = os.getenv("REST_API_URL")

last_push_to_adafruit_io_time = 0


def can_push_to_adafruit():
    """Check if we can push to Adafruit IO."""
    global last_push_to_adafruit_io_time
    current_time = time.time()  # Get the current time in seconds since the Epoch
    if (
        current_time - last_push_to_adafruit_io_time >= 10
    ):  # Check if 3 or more seconds have passed
        last_push_to_adafruit_io_time = current_time  # Update the last push time
        return True
    return False


def push_to_adafruit(data):
    """Push the data to Adafruit IO."""
    if can_push_to_adafruit():
        client.publish("packet_number", data["packet_number"])
        client.publish("temperature", data["temperature"])
        client.publish("light", data["light"])
        client.publish("humidity", data["humidity"])


def push_to_rest_api(data):
    """Push the data to REST API."""
    response = requests.post(REST_API_URL, json=data)
    if response.status_code != 201:
        raise Exception("Failed to post data to the API." + response.text)


def read_from_serial(port, client):
    """Open the serial port, continuously read, parse data, and publish to Adafruit IO."""
    packet_data = ""  # Initialize an empty string to accumulate packet data
    with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
        while True:
            line = ser.readline().decode("utf-8")
            if line.strip():  # If the line is not just whitespace
                packet_data += line  # Accumulate the line
                # Check if we have both lines of a packet
                if packet_data.count("\n") >= 2:
                    print("Data:\n" + packet_data, end="\n")
                    data = parse_data(packet_data.replace("\n", ""))
                    push_to_rest_api(data)
                    push_to_adafruit(data)
                    packet_data = ""
            time.sleep(0.01)  # Brief pause to avoid hogging CPU


def disconnected(client):
    """Disconnected function will be called when the client disconnects."""
    print("Disconnected from Adafruit IO!")
    sys.exit(1)


def parse_data(data):
    """Parse the serial data into a format suitable for publishing."""
    # Pattern for temperature
    temp_pattern = r"Temp\s+([-\d.]+)\s*F"
    temp_match = re.search(temp_pattern, data)
    temperature = temp_match.group(1) if temp_match else None

    # Pattern for light
    light_pattern = r"Light\s+(\d+)\s*lx"
    light_match = re.search(light_pattern, data)
    light = light_match.group(1) if light_match else None

    # Pattern for humidity
    humidity_pattern = r"Humidity\s+(\d+)\s*%"
    humidity_match = re.search(humidity_pattern, data)
    humidity = humidity_match.group(1) if humidity_match else None

    # Pattern for packet number
    packet_pattern = r"Packet\s+#\s+(\d+)"
    packet_match = re.search(packet_pattern, data)
    packet_number = packet_match.group(1) if packet_match else None

    # Pattern for node number
    node_pattern = r"Node\s*(\d+)"
    node_match = re.search(node_pattern, data)
    node = node_match.group(1) if node_match else -1

    return {
        "node": node,
        "packet_number": packet_number,
        "temperature": temperature,
        "light": light,
        "humidity": humidity,
    }


if __name__ == "__main__":
    # Create an MQTT client instance.
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    client.on_disconnect = disconnected

    # Connect to the Adafruit IO server.
    client.connect()

    # Run the MQTT client in the background to keep the connection open.
    client.loop_background()

    last_push_to_adafruit_io_time = time.time()  # Initialize the last push time

    # Start reading from serial and publishing to Adafruit IO
    read_from_serial(SERIAL_PORT, client)
