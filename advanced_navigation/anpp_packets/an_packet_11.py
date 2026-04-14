################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_11.py                              ##
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
from typing import List
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


class LinkMode(Enum):
    """Link Mode"""

    auto = 0
    full_duplex_100mb = 1
    half_duplex_100mb = 2
    full_duplex_10mb = 3
    half_duplex_10mb = 4


@dataclass()
class DHCPMode:
    """DHCP Mode"""

    dhcp_enabled: bool = False
    automatic_dns: bool = False
    link_mode: LinkMode = LinkMode.auto

    def unpack(self, data):
        self.dhcp_enabled = (data & 0x1) != 0
        self.automatic_dns = (data & 0x2) != 0
        self.link_mode = LinkMode((data & 0x1C) >> 2)

    def pack(self):
        return (
            (self.dhcp_enabled << 0)
            & (self.automatic_dns << 1)
            & (self.link_mode.value << 2)
        )


@dataclass()
class IPConfigurationPacket:
    """Packet 11 - IP Configuration Packet"""

    permanent: int = 0
    dhcp_mode: DHCPMode = field(default_factory=DHCPMode, repr=False)
    ip_address: int = 0
    ip_netmask: int = 0
    ip_gateway: int = 0
    dns_server: int = 0
    serial_number: List[int] = field(default_factory=lambda: [0, 0, 0], repr=False)

    ID = PacketID.ip_configuration
    LENGTH = 30

    _structure = struct.Struct("<BBIIIIIII")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to IP Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.permanent,
                dhcp_mode_data,
                self.ip_address,
                self.ip_netmask,
                self.ip_gateway,
                self.dns_server,
                *self.serial_number,
            ) = self._structure.unpack_from(an_packet.data)
            self.dhcp_mode.unpack(dhcp_mode_data)
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode IP Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.dhcp_mode.pack(),
            self.ip_address,
            self.ip_netmask,
            self.ip_gateway,
            self.dns_server,
            *self.serial_number,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
