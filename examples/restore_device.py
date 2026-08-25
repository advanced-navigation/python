################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              restore_device.py                             ##
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
Recovery script for a device that is inaccessible due to a misconfiguration.

This attempts to connect to a device's bootloader by waiting for you to
power-cycle the device. When the bootloader briefly appears at 115200 baud it is
caught, then a factory restore packet is sent to reset the device's internal config.

WARNING: This will completely wipe all configuration on the device. Make sure you have
any offsets etc. saved somewhere.
"""

import argparse
import asyncio
import logging
import sys

from advanced_navigation.an_devices.an_device_async import AnDevice
from advanced_navigation.anpp_packets.an_packet_0 import AcknowledgeResult
from advanced_navigation.anpp_packets.an_packet_2 import BootMode, BootModePacket
from advanced_navigation.anpp_packets.an_packet_4 import RestoreFactorySettingsPacket
from advanced_navigation.anpp_packets.an_packet_49 import RunningTimePacket


async def main():
    parser = argparse.ArgumentParser(description="Recover from baud rate lock-out")
    parser.add_argument(
        "--com_port", type=str, default="/dev/ttyUSB0", help="Serial communication port"
    )
    args = parser.parse_args()

    device = AnDevice()
    try:
        await device.connect_serial(args.com_port, 115200)

        for _ in range(3):
            packet = await device.request(RunningTimePacket)
            if packet is not None:
                print(
                    "Device found in application on baudrate: 115200, try sending the factory restore packet or connecting via manager."
                )
                sys.exit(0)

        print("Please power-cycle the device...")
        print("(You may need to do this twice in quick succession)")
        packet = BootModePacket()
        packet.boot_mode = BootMode.bootloader
        ack = None
        while ack is None or ack.acknowledge_result != AcknowledgeResult.success:
            ack = await device.send(packet, timeout=0.2)
        print("Bootloader caught.\n")

        print("Restoring baud rates...")
        packet = RestoreFactorySettingsPacket()
        for _ in range(3):
            ack = await device.send(packet, timeout=3)
            if ack is not None and ack.acknowledge_result == AcknowledgeResult.success:
                print("Baud rates successfully restored.\n")
                break
        else:
            print("Failed to restore baud rates 3 times.")
            sys.exit(1)

        await asyncio.sleep(2)

        packet = BootModePacket()
        packet.boot_mode = BootMode.main_program
        ack = await device.send(packet)
        if ack is not None and ack.acknowledge_result == AcknowledgeResult.success:
            print("Automatically triggered a restart, please wait...")
        else:
            print(
                "Failed to automatically trigger a restart. Please power-cycle the device once."
            )
        print("(Restart may take up to 30 seconds)")

        packet = None
        while packet is None:
            packet = await device.request(RunningTimePacket)
        print("Device has restarted on new baud rate: 115200.")

    finally:
        device.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())
