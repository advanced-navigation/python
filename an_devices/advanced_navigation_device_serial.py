################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                        advanced_navigation_device_serial.py                ##
##                     Copyright 2023, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2023 Advanced Navigation                                       #
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

import os
import serial
import serial.serialutil as serialutil
from abc import ABC, abstractmethod

from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANDecoder
from anpp_packets.an_packet_1 import RequestPacket


class AdvancedNavigationDeviceSerial(ABC):
    def __init__(self, port, baud):
        self.decoder = ANDecoder()
        self.ser = None

        if isinstance(port, str):
            self.port = port
        else:
            raise ValueError(f"Port:{port} is not valid")

        if int(baud) in self.valid_baud_rates:
            self.baud = baud
        else:
            raise ValueError(f"Baud Rate:{baud} is not valid")

    @property
    @abstractmethod
    def valid_baud_rates(self):
        """Child class needs to declare this property"""
        pass

    # Serial Communications
    def start(self):
        # Checks if operating system is Windows or Linux
        if (os.name == "nt") or (os.name == "posix"):
            # Connects to serial port
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                bytesize=serialutil.EIGHTBITS,
                parity=serialutil.PARITY_NONE,
                stopbits=serialutil.STOPBITS_ONE,
                timeout=None,
                xonxoff=False,
                rtscts=False,
                write_timeout=None,
                dsrdtr=False,
                inter_byte_timeout=None,
            )
        else:
            print(
                "Packet_example currently only supports Windows and Linux operating systems."
            )
            exit()

    def close(self):
        self.ser.close()

    def is_open(self):
        return self.ser.is_open

    def flush(self):
        self.ser.flush()

    def in_waiting(self):
        return self.ser.in_waiting

    def read(self, bytes_in_buffer):
        return self.ser.read(bytes_in_buffer)

    # Device and Configuration Information
    @abstractmethod
    def return_device_information_and_configuration_packets(self):
        """Child class needs to implement this method to return
        the device information and configuration packets as a list"""
        pass

    def get_device_and_configuration_information(self):
        packets = self.return_device_information_and_configuration_packets()
        if len(packets) != 0:
            self.request_packet(packets)
        else:
            print("Warning: No Device Information or Configuration packets defined.")

    # System Packets
    def request_packet(self, packet_id: PacketID):
        print(f"Requesting PacketIDs: {packet_id}")
        self.ser.write(RequestPacket(packet_id).encode().bytes())
