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
from struct import pack, unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class ExternalPositionVelocityPacket:
    """Packet 44 - External Position Velocity Packet"""
    position: [float] * 3 = field(default_factory=list)
    velocity: [float] * 3 = field(default_factory=list)
    position_standard_deviation: [float] * 3 = field(default_factory=list)
    velocity_standard_deviation: [float] * 3 = field(default_factory=list)

    ID = PacketID.external_position_velocity
    LENGTH = 60

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to External Position Velocity Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.position = unpack('<ddd', bytes(an_packet.data[0:24]))
            self.velocity = unpack('<fff', bytes(an_packet.data[24:36]))
            self.position_standard_deviation = unpack('<fff', bytes(an_packet.data[36:48]))
            self.velocity_standard_deviation = unpack('<fff', bytes(an_packet.data[48:60]))
            return 0
        else:
            return 1

    def encode(self):
        """Encode External Position Velocity Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<ddd', self.position[0], self.position[1], self.position[2])
        data += pack('<fff', self.velocity[0].self.velocity[1], self.velocity[2])
        data += pack('<fff', self.position_standard_deviation[0].self.position_standard_deviation[1],
                     self.position_standard_deviation[2])
        data += pack('<fff', self.velocity_standard_deviation[0].self.velocity_standard_deviation[1],
                     self.velocity_standard_deviation[2])

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
