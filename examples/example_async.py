################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              example_async.py                              ##
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
device over serial or TCP using Python Asynchronous I/O (asyncio) Library
"""

import asyncio
import argparse
import datetime
import logging

from advanced_navigation.an_devices.an_device_async import AnDevice
from advanced_navigation.an_devices import device_capabilities
from advanced_navigation.anpp_packets.an_packet_3 import DeviceInformationPacket, DeviceID
from advanced_navigation.anpp_packets.an_packet_13 import ExtendedDeviceInformationPacket
from advanced_navigation.anpp_packets.an_packet_20 import SystemStatePacket
from packet_printers import handle_raw_an_packet, print_packet

async def main():
    parser = argparse.ArgumentParser(description="Advanced Navigation Asynchronous Example")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--serial", "-s", type=str, help="Serial communication port (e.g. /dev/ttyUSB0 or COM3)")
    group.add_argument("--ip", "-i", type=str, help="Device IP address (Connect via TCP)")
    parser.add_argument("--baud_rate", "-b", type=int, default=115200, help="Baud rate for Serial connection")
    parser.add_argument("--port", "-p", type=int, default=16718, help="Device TCP port")
    args = parser.parse_args()

    device = AnDevice()
    device_id = DeviceID.unknown

    try:
        # Establish the connection asynchronously
        if args.ip is not None:
            print(f"Connecting via TCP to {args.ip}:{args.port}...")
            await device.connect_tcp(args.ip, args.port)
        else:
            print(f"Connecting via Serial to {args.serial} at {args.baud_rate} baud...")
            await device.connect_serial(args.serial, args.baud_rate)

        # Wait until the device responds to a ping
        print("Waiting for device to come online...")
        await device.wait_online()

        # Create log file for received binary data from device
        # "xb" mode opens the file for exclusive creation (fails if it already exists) in binary mode
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = open(f"DeviceLog_{now}.anpp", "xb")
        print(f"Recording raw binary data to DeviceLog_{now}.anpp")
        print("-" * 40)

        # Request Device Information to understand what hardware we are talking to
        device_information = await device.request(DeviceInformationPacket)
        if device_information is not None:
            device_id = device_information.device_id
            print_packet(device_information)
            print("-" * 40)

            # Example of using device capabilities
            # If the device supports subtypes, we can also request the Extended Device Information packet
            if device_capabilities.has_sub_type(device_id):
                extended_device_information = await device.request(ExtendedDeviceInformationPacket)
                if extended_device_information is not None:
                    print_packet(extended_device_information)
                    print("-" * 40)

        # --- Example Configuration (Optional) ---
        # If you want to send a configuration packet to the device, follow this example:
        # from advanced_navigation.anpp_packets.an_packet_184 import SensorRangesPacket, AccelerometerRange, GyroscopeRange, MagnetometerRange
        # config_packet = SensorRangesPacket()
        # config_packet.permanent = 1
        # config_packet.accelerometers_range = AccelerometerRange.accelerometer_range_4g
        # config_packet.gyroscopes_range = GyroscopeRange.gyroscope_range_500dps
        # config_packet.magnetometers_range = MagnetometerRange.magnetometer_range_8g
        # await device.send(config_packet)
        # ----------------------------------------

        print("Listening for packets... (Press Ctrl+C to stop)\n")
        print("-" * 40)

        # Example 1: Use a specific packet type listener
        # Here we listen to the SystemStatePacket (20) and process its data
        async def system_state_handler(packet: SystemStatePacket):
            print(f"[{datetime.datetime.now().isoformat()}] Received System State:")
            print(f"  Latitude:  {packet.latitude:.7f}")
            print(f"  Longitude: {packet.longitude:.7f}")
            print(f"  Height:    {packet.height:.3f}")
            print(f"  Heading:   {packet.orientation[2]:.3f}")
            print("-" * 40)

        device.register_callback(SystemStatePacket, system_state_handler)

        # Example 2: Use a raw packet listener
        # Use device.register_raw_callback() to receive all raw ANPackets.
        async def generic_packet_printer(an_packet):
            # Log the raw binary bytes to the file
            log_file.write(an_packet.bytes())
            
            # Print the packet properly using the decoder
            handle_raw_an_packet(an_packet, device_id)
            print("-" * 40)
            
        device.register_raw_callback(generic_packet_printer)

        # Keep the main loop alive infinitely
        # asyncio.Future() creates a future that is never resolved, pausing execution here indefinitely
        await asyncio.Future()

    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    finally:
        device.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
