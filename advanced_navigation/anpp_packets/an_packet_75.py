################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_75.py                              ##
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
import struct
from typing import List
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


@dataclass()
class ExternalMagnetometersFlags:
    """External Magnetometers Flags"""

    failure: bool = False
    overrange: bool = False

    def unpack(self, data):
        self.failure = (data & (1 << 0)) != 0
        self.overrange = (data & (1 << 1)) != 0

    def pack(self):
        return (self.failure << 0) & (self.overrange << 1)


@dataclass()
class ExternalMagnetometersPacket:
    """Packet 75 - External Magnetometers Packet"""

    delay: float = 0
    magnetometer: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    flags: ExternalMagnetometersFlags = field(
        default_factory=ExternalMagnetometersFlags, repr=False
    )

    ID = PacketID.external_magnetometers
    LENGTH = 17

    _structure = struct.Struct("<ffffB")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to External Magnetometers Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            (self.delay, *self.magnetometer) = values[:4]
            self.flags.unpack(values[4])
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode External Magnetometers Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(self.delay, *self.magnetometer, self.flags.pack())

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
