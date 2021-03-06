################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                        advanced_navigation_device.py                       ##
##                     Copyright 2021, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2021 Advanced Navigation                                       #
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
import datetime
import serial
import serial.serialutil as serialutil
from enum import Enum
from struct import pack, unpack
from dataclasses import dataclass, field
from ctypes.wintypes import DOUBLE
from anpp_packets.an_packet_protocol import AN_Decoder
from abc import ABC, abstractmethod
from anpp_packets.anpp_packets import ResetVerification, OdometerFlags, ExternalAirDataPacketFlags, PacketPeriod, GPIOOutputRate

valid_baud_rates = [2400, 4800, 9600, 19200, 38400, 57600,
                    115200, 230400, 250000, 460800, 500000,
                    800000, 921600, 1000000, 1250000, 2000000]

class AdvancedNavigationDevice(ABC):
    def __init__(self, port, baud, log = False):
        self.bytes_waiting = AN_Decoder()
        self.ser = None
        self.logFile = None

        if isinstance(port, str):
            self.port = port
        else:
            print(f"Port:{port} is not valid")

        if (int(baud) in valid_baud_rates):
            self.baud = baud
        else:
            print(f"Baud Rate:{baud} is not valid")

    # Serial Communications
    def start_serial(self):
        # Checks if operating system is Windows or Linux
        if ((os.name == 'nt') or (os.name == 'posix')):
            # Connects to serial port
            self.ser = serial.Serial(port=self.port,
                             baudrate=self.baud,
                             bytesize=serialutil.EIGHTBITS,
                             parity=serialutil.PARITY_NONE,
                             stopbits=serialutil.STOPBITS_ONE,
                             timeout=None,
                             xonxoff=False,
                             rtscts=False,
                             write_timeout=None,
                             dsrdtr=False,
                             inter_byte_timeout=None
                             )
        else:
            print(f"Packet_example currently only supports Windows and Linux operating systems.")
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
        """ Child class needs to implement this method to return
        the device information and configuration packets as a list """
        pass

    def get_device_and_configuration_information(self):
        for packet in self.return_device_information_and_configuration_packets():
            self.request_packet(packet)

    # System Packets
    def request_packet(self, packet_id):
        print(f"Requesting PacketId:{packet_id}")
        self.ser.write(self.RequestPacket.encode(packet_id).bytes())

    def set_sensor_ranges(self, permanent:int, accelerometers_range:int, gyroscopes_range:int, magnetometers_range:int):
        packet = self.SensorRangesPacket()
        packet.permanent = permanent
        packet.accelerometers_range = accelerometers_range
        packet.gyroscopes_range = gyroscopes_range
        packet.magnetometers_range = magnetometers_range
        self.ser.write(packet.encode().bytes())