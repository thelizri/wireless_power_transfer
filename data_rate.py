import serial
import sys
import time
import re


# Configuration for the serial port
SERIAL_PORT = "COM3"
BAUD_RATE = 19200

def read_from_serial(port):
    """Open the serial port, continuously read, parse data, and publish to Adafruit IO."""
    packet_data = ""  # Initialize an empty string to accumulate packet data
    time_prev = 0
    time_current = time.time()
    time_array = []
    power_array = []    
    with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
        while True:
            line = ser.readline().decode("utf-8", errors='ignore')
            if line.strip():  # If the line is not just whitespace
                packet_data += line  # Accumulate the line
                # Check if we have both lines of a packet
                if packet_data.count("\n") >= 2:
                    time_prev, time_current = time_current, time.time()
                    time_delta = time_current - time_prev
                    time_array.append(time_delta)
                    power = parse_data(packet_data)
                    if power:
                        power_array.append(float(power))
                    print("Data:\n" + packet_data, end="\n")
                    print("Time delta: ", round(time_delta, 3), "s")
                    print("Frequency: ", round(1 / (time_delta), 3), "Hz")

                    if len(time_array) > 10:
                        print("---------------------------------------------")
                        print("\n Average frequency: ", round(1 / (sum(time_array) / len(time_array)), 3), "Hz\n")
                        print("Average power: ", round(sum(power_array) / len(power_array), 3), "mW\n")
                        print("---------------------------------------------")
                        time_array = []
                        power_array = []
                    packet_data = ""
            time.sleep(0.01)  # Brief pause to avoid hogging CPU

def parse_data(data):
    """Parse the serial data into a format suitable for averaging."""
    # Pattern for power
    power_pattern = r"RSSI\s+([-\d.]+)\s*mW"
    power_match = re.search(power_pattern, data)
    power = power_match.group(1) if power_match else None
    if power:
        return power


if __name__ == "__main__":
    # Start reading from serial
    read_from_serial(SERIAL_PORT)