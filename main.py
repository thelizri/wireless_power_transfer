import serial
import sys
import time
import re
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

last_push_time = 0


def can_push_to_api():
    global last_push_time
    current_time = time.time()  # Get the current time in seconds since the Epoch
    if current_time - last_push_time >= 10:  # Check if 3 or more seconds have passed
        last_push_time = current_time  # Update the last push time
        return True
    return False


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
                    if can_push_to_api():
                        parse_data(packet_data.replace("\n", ""))
                    packet_data = ""
            time.sleep(0.05)  # Brief pause to avoid hogging CPU


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
    if temperature:
        client.publish("Temperature", temperature)

    # Pattern for light
    light_pattern = r"Light\s+(\d+)\s*lx"
    light_match = re.search(light_pattern, data)
    light = light_match.group(1) if light_match else None
    if light:
        client.publish("Light", light)

    # Pattern for humidity
    humidity_pattern = r"Humidity\s+(\d+)\s*%"
    humidity_match = re.search(humidity_pattern, data)
    humidity = humidity_match.group(1) if humidity_match else None
    if humidity:
        client.publish("Humidity", humidity)

    # Pattern for packet number
    packet_pattern = r"Packet\s+#\s+(\d+)"
    packet_match = re.search(packet_pattern, data)
    packet_number = packet_match.group(1) if packet_match else None
    if packet_number:
        client.publish("Packet Number", packet_number)


if __name__ == "__main__":
    # Create an MQTT client instance.
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    client.on_disconnect = disconnected

    # Connect to the Adafruit IO server.
    client.connect()

    # Run the MQTT client in the background to keep the connection open.
    client.loop_background()

    last_push_time = time.time()  # Initialize the last push time
    print(ADAFRUIT_IO_KEY)

    # Start reading from serial and publishing to Adafruit IO
    read_from_serial(SERIAL_PORT, client)
