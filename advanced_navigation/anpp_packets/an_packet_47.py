################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_47.py                              ##
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
class ExternalBodyVelocityPacket:
    """Packet 47 - External Body Velocity Packet"""

    velocity: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    standard_deviation: List[float] = field(
        default_factory=lambda: [0, 0, 0], repr=False
    )

    ID = PacketID.external_body_velocity
    LENGTH_SHORT = 16
    LENGTH_FULL = 24

    _structure_short = struct.Struct("<ffff")
    _structure_full = struct.Struct("<ffffff")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to External Body Velocity Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH_SHORT):
            (
                *self.velocity,
                self.standard_deviation[0],
            ) = self._structure_short.unpack_from(an_packet.data)

            return 0
        elif (an_packet.id == self.ID) and (len(an_packet.data) == 24):
            values = self._structure_full.unpack_from(an_packet.data)
            self.velocity = list(values[0:3])
            self.standard_deviation = list(values[3:6])
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode External Body Velocity Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure_full.pack(*self.velocity, *self.standard_deviation)

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH_FULL, data)

        return an_packet
