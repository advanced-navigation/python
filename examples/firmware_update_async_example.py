################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                      firmware_update_async_example.py                      ##
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
This example shows how to update the firmware on a Advanced Navigation device
over serial using Python Asynchronous I/O (asyncio) Library
"""

import asyncio
import argparse
import logging

from advanced_navigation.an_devices.an_device_async import AnDevice
from advanced_navigation.anpp_packets.an_packet_3 import DeviceInformationPacket
from advanced_navigation.anpp_packets.an_packet_2 import BootMode

async def main():
    parser = argparse.ArgumentParser(description="Air Data Unit V2 Example")
    parser.add_argument("--com_port",  type=str, default="/dev/ttyUSB0", help="Serial communication port")
    parser.add_argument("--baud_rate", type=int, default=115200, help="Baud rate")
    parser.add_argument("--file_path", type=str, help="Update to Firmware update file (.anfw)")
    args = parser.parse_args()

    device = AnDevice()
    
    try:
        await device.connect_serial(args.com_port, args.baud_rate)
        print(f"Opened {args.com_port} at {args.baud_rate} baud.")
        await device.wait_online()
        device_information = await device.request(DeviceInformationPacket)
        if device_information is not None:
            print("Connected to {} SN {:08x}{:08x}{:08x} SW {} HW {}".format(device_information.device_id,
                                                                            device_information.serial_number[0],  
                                                                            device_information.serial_number[1], 
                                                                            device_information.serial_number[2],
                                                                            device_information.software_version/1000,
                                                                            device_information.hardware_revision/1000))

        # Switch the device into bootloader mode, which is required before writing firmware
        await device.request_boot_mode(BootMode.bootloader)
        # Stream the .anfw firmware update file to the device
        await device.write_firmware(args.file_path)
        # Wait for the device to reboot and come back online after the update finishes
        await device.wait_online()

        device_information = await device.request(DeviceInformationPacket)
        if device_information is not None:
            print(f"Firmware Update Complete. SW Version {device_information.software_version/1000}")
    finally:
        device.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
