import serial
import sys
import time
import re
from Adafruit_IO import MQTTClient

# Configuration for the serial port
SERIAL_PORT = "/dev/tty.usbmodem143301"
BAUD_RATE = 19200

# Adafruit IO Configuration
ADAFRUIT_IO_USERNAME = "Karlan"
ADAFRUIT_IO_KEY = "aio_uhaU93dETgrgVIdEIUYVZiu2w3E0"
IO_FEED = "Temperature"


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
                    parsed_data = parse_data(packet_data.replace("\n", ""))
                    if parsed_data:
                        print(f"Publishing {parsed_data} to {IO_FEED}.", end="\n\n")
                        client.publish(IO_FEED, parsed_data)
                    packet_data = ""
            time.sleep(1)  # Brief pause to avoid hogging CPU


def disconnected(client):
    """Disconnected function will be called when the client disconnects."""
    print("Disconnected from Adafruit IO!")
    sys.exit(1)


def parse_data(data):
    """Parse the serial data into a format suitable for publishing."""
    temp_pattern = r"Temp\s+([-\d.]+)\s*F"
    match = re.search(temp_pattern, data)

    if match:
        return float(match.group(1))

    return None


if __name__ == "__main__":
    # Create an MQTT client instance.
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    client.on_disconnect = disconnected

    # Connect to the Adafruit IO server.
    client.connect()

    # Run the MQTT client in the background to keep the connection open.
    client.loop_background()

    # Start reading from serial and publishing to Adafruit IO
    read_from_serial(SERIAL_PORT, client)
