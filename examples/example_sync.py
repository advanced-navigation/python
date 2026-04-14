################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              example_sync.py                               ##
##                     Copyright 2026, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2026 Advanced Navigation                                       #
#                                                                              #
# Permission is hereby granted, free of charge, to any person obtaining        #
# a copy of this software and associated documentation files (the "Software"), #
# to deal in the Software without restriction, including without limitation    #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,     #
# and/or sell copies of the Software, and to permit persons to whom the        #
# Software is furnished to do so, subject to the following conditions:         #
#                                                                              #
# The above copyright notice and this permission notice shall be included      #
# in all copies or substantial portions of the Software.                       #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS      #
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER          #
# DEALINGS IN THE SOFTWARE.                                                    #
################################################################################

"""
This example shows how to send & receive ANPP packets with an Advanced Navigation 
device over serial or TCP using Python Synchronous I/O Library
"""

import time
import argparse
import socket
import datetime
import serial
import serial.serialutil as serialutil
import logging
from advanced_navigation.an_devices import device_capabilities
from advanced_navigation.anpp_packets.an_packet_protocol import ANDecoder
from advanced_navigation.anpp_packets.an_packet_1 import RequestPacket
from advanced_navigation.anpp_packets.an_packet_3 import DeviceInformationPacket, DeviceID
from advanced_navigation.anpp_packets.an_packet_13 import ExtendedDeviceInformationPacket
from packet_printers import handle_raw_an_packet, print_packet

def read_from_socket(sock: socket.socket) -> bytes:
    try:
        # sock.recv blocks until data is available or a timeout occurs.
        # Since we set conn.settimeout(1.0), this will raise an exception if no data 
        # is received within 1 second, returning empty bytes to continue the polling loop.
        return sock.recv(1024)
    except Exception:
        return b""

def read_from_serial(ser: serial.Serial) -> bytes:
    try:
        # ser.in_waiting returns the number of bytes currently in the input buffer.
        # Reading only the available bytes prevents blocking indefinitely on ser.read()
        if ser.in_waiting > 0:
            return ser.read(ser.in_waiting)
        return b""
    except Exception:
        return b""

def main():
    parser = argparse.ArgumentParser(description="Advanced Navigation Synchronous Example")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--serial", "-s", type=str, help="Serial communication port (e.g. /dev/ttyUSB0 or COM3)")
    group.add_argument("--ip", "-i", type=str, help="Device IP address (Connect via TCP)")
    parser.add_argument("--baud_rate", "-b", type=int, default=115200, help="Baud rate for Serial connection")
    parser.add_argument("--port", "-p", type=int, default=16718, help="Device TCP port")
    args = parser.parse_args()

    decoder = ANDecoder()
    device_id = DeviceID.unknown
    conn = None
    is_tcp = False

    try:
        # Establish the connection
        if args.ip is not None:
            print(f"Connecting via TCP to {args.ip}:{args.port}...")
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(1.0)
            conn.connect((args.ip, args.port))
            is_tcp = True
        else:
            print(f"Connecting via Serial to {args.serial} at {args.baud_rate} baud...")
            conn = serial.Serial(
                port=args.serial,
                baudrate=args.baud_rate,
                bytesize=serialutil.EIGHTBITS,
                parity=serialutil.PARITY_NONE,
                stopbits=serialutil.STOPBITS_ONE,
                timeout=1.0,
            )

        print("Connection established. Requesting Device Information...")

        # Create log file for received binary data from device
        # "xb" mode opens the file for exclusive creation (fails if it already exists) in binary mode
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = open(f"DeviceLog_{now}.anpp", "xb")
        print(f"Recording raw binary data to DeviceLog_{now}.anpp")

        # Request Device Information to understand what hardware we are talking to
        # In synchronous mode, we manually craft a RequestPacket to ask for it
        request = RequestPacket()
        request.requested_packets = [DeviceInformationPacket.ID]
        
        def send_request():
            if is_tcp and isinstance(conn, socket.socket):
                conn.sendall(request.encode().bytes())
            elif not is_tcp and isinstance(conn, serial.Serial):
                conn.write(request.encode().bytes())
                
        send_request()
        last_request_time = time.time()

        # --- Example Configuration (Optional) ---
        # If you want to send a configuration packet to the device, follow this example:
        # from advanced_navigation.anpp_packets.an_packet_184 import SensorRangesPacket, AccelerometerRange, GyroscopeRange, MagnetometerRange
        # config_packet = SensorRangesPacket()
        # config_packet.permanent = 1
        # config_packet.accelerometers_range = AccelerometerRange.accelerometer_range_4g
        # config_packet.gyroscopes_range = GyroscopeRange.gyroscope_range_500dps
        # config_packet.magnetometers_range = MagnetometerRange.magnetometer_range_8g
        # if is_tcp:
        #     conn.sendall(config_packet.encode().bytes())
        # else:
        #     conn.write(config_packet.encode().bytes())
        # ----------------------------------------

        # Enter polling loop
        print("Listening for packets... (Press Ctrl+C to exit)\n")
        print("-" * 40)
        
        while True:
            # Periodically retry asking for device information if we haven't received it
            if device_id == DeviceID.unknown and time.time() - last_request_time > 1.0:
                send_request()
                last_request_time = time.time()

            # Read chunks of bytes
            if is_tcp and isinstance(conn, socket.socket):
                raw_data = read_from_socket(conn)
            elif not is_tcp and isinstance(conn, serial.Serial):
                raw_data = read_from_serial(conn)
            else:
                raw_data = b""

            if raw_data:
                # Record in log file the raw binary of ANPP packets
                log_file.write(raw_data)
                
                # Add raw data to our decoder buffer
                decoder.add_data(raw_data)

            # Attempt to pop fully assembled ANPackets off the internal buffer
            # decoder.decode() returns None if there is not enough data yet to form a complete packet
            while True:
                an_packet = decoder.decode()
                if an_packet is None:
                    break

                # The first packet we get should be the DeviceInformationPacket
                if an_packet.id == DeviceInformationPacket.ID.value and device_id == DeviceID.unknown:
                    info_packet = DeviceInformationPacket()
                    if info_packet.decode(an_packet) == 0:
                        device_id = info_packet.device_id
                        print_packet(info_packet)
                        print("-" * 40)

                        # Example of using device capabilities
                        # If the device supports subtypes, we can also request the Extended Device Information packet
                        if device_capabilities.has_sub_type(device_id):
                            ext_req = RequestPacket()
                            ext_req.requested_packets = [ExtendedDeviceInformationPacket.ID]
                            if is_tcp and isinstance(conn, socket.socket):
                                conn.sendall(ext_req.encode().bytes())
                            elif not is_tcp and isinstance(conn, serial.Serial):
                                conn.write(ext_req.encode().bytes())
                    continue

                # Wait for the extended info packet if we requested it
                if an_packet.id == ExtendedDeviceInformationPacket.ID.value:
                    ext_info = ExtendedDeviceInformationPacket()
                    if ext_info.decode(an_packet) == 0:
                        print_packet(ext_info)
                        print("-" * 40)
                    continue

                # Pass everything else to the packet printer
                handle_raw_an_packet(an_packet, device_id)
                print("-" * 40)

    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
