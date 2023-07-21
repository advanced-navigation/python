################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_44.py                              ##
##                     Copyright 2022, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2022 Advanced Navigation                                       #
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
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class ExternalPositionVelocityPacket:
    """Packet 44 - External Position Velocity Packet"""

    position: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    velocity: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    position_standard_deviation: List[float] = field(
        default_factory=lambda: [0, 0, 0], repr=False
    )
    velocity_standard_deviation: List[float] = field(
        default_factory=lambda: [0, 0, 0], repr=False
    )

    ID = PacketID.external_position_velocity
    LENGTH = 60

    _structure = struct.Struct("<dddfffffffff")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to External Position Velocity Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.position = list(values[0:3])
            self.velocity = list(values[3:6])
            self.position_standard_deviation = list(values[6:9])
            self.velocity_standard_deviation = list(values[9:12])
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode External Position Velocity Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            *self.position,
            *self.velocity,
            *self.position_standard_deviation,
            *self.velocity_standard_deviation
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
