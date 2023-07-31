################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                        advanced_navigation_device_tcp.py                   ##
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

import socket
from abc import ABC, abstractmethod

from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANDecoder
from anpp_packets.an_packet_1 import RequestPacket


class AdvancedNavigationDeviceTCP(ABC):
    def __init__(self, address, port):
        self.timeout = 0.5
        self.address = None
        self.port = None
        self.decoder = ANDecoder()

        if isinstance(address, str):
            self.address = address
        else:
            raise ValueError(f"IP Address :{address} is not valid")

        if isinstance(port, int):
            self.port = port
        else:
            raise ValueError(f"Port:{port} is not valid")

    # TCP Communications
    def start(self):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.settimeout(self.timeout)

        try:
            self.tcp.connect((self.address, self.port))
            return True
        except socket.timeout:
            return False
        except:
            return False

    def close(self):
        self.tcp.close()

    def is_open(self):
        try:
            self.tcp.recv(8, socket.MSG_PEEK)
            return True
        except socket.timeout:
            return True
        except Exception as e:
            print(f"exception in connection check : {e}")
            return False

    def read(self):
        try:
            return self.tcp.recv(64)
        except Exception as e:
            print(f"exception in read : {e}")
            return None

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
        self.tcp.sendall(RequestPacket(packet_id).encode().bytes())
