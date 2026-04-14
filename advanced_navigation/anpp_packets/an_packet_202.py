################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_202.py                              ##
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

from dataclasses import dataclass, field
from enum import Enum
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


class IPDataportMode(Enum):
    """IP Dataport Mode"""

    none = 0
    tcp_server = 2
    tcp_client = 3
    udp = 4


@dataclass()
class IPDataportConfiguration:
    """IP Dataport Configuration"""

    ip_address: int = 0
    port: int = 0
    mode: IPDataportMode = IPDataportMode.none

    LENGTH = 7

    _structure = struct.Struct("<IHB")

    def unpack(self, data):
        """Unpack data bytes"""
        (self.ip_address, self.port, mode_value) = self._structure.unpack_from(data)
        self.mode = IPDataportMode(mode_value)

    def pack(self) -> bytes:
        return self._structure.pack(self.ip_address, self.port, self.mode.value)


@dataclass()
class IPDataportConfigurationPacket:
    """Packet 202 - IP Dataport Configuration Packet"""

    ip_dataport_configuration: list[IPDataportConfiguration] = field(
        default_factory=lambda: [IPDataportConfiguration()] * 4
    )

    ID = PacketID.ip_dataports_configuration
    LENGTH = 30

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to IP Dataport Configuration Packet
        Returns 0 on success and 1 on failure"""
        if an_packet.id != self.ID or len(an_packet.data) != self.LENGTH:
            return 1
        for i in range(4):
            index = 2 + i * IPDataportConfiguration.LENGTH
            self.ip_dataport_configuration[i].unpack(
                an_packet.data[index : index + IPDataportConfiguration.LENGTH]
            )
        return 0

    def encode(self) -> ANPacket:
        """Encode IP Dataport Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = struct.pack("<H", 0)
        for i in range(4):
            data += self.ip_dataport_configuration[i].pack()

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
