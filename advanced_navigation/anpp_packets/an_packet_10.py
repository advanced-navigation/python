################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_3.py                               ##
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


class PassthroughRoute(Enum):
    """Passthrough Route"""

    gpio = 0
    auxiliary = 1


@dataclass()
class SerialPortPassthroughPacket:
    """Packet 10 - Serial Port Passthrough Packet"""

    passthrough_route: PassthroughRoute = PassthroughRoute.gpio
    passthrough_data: bytes = field(default_factory=bytes, repr=False)

    ID = PacketID.serial_port_passthrough

    _structure = struct.Struct("<B")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Serial Port Passthrough Packet
        Returns 0 on success and 1 on failure"""
        if an_packet.id == self.ID:
            self.passthrough_route = PassthroughRoute(an_packet.data[0])
            self.passthrough_data = bytes(an_packet.data[1:])
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode Serial Port Passthrough Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(self.passthrough_route.value)
        data += self.passthrough_data

        an_packet = ANPacket()
        an_packet.encode(self.ID, len(data), data)

        return an_packet
