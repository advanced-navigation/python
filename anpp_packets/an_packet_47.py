################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_47.py                              ##
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
class ExternalBodyVelocityPacket:
    """Packet 47 - External Body Velocity Packet"""
    velocity: [float] * 3 = field(default_factory=list)
    standard_deviation: [float] * 3 = field(default_factory=list)

    ID = PacketID.external_body_velocity
    LENGTH = 16

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to External Body Velocity Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.velocity = unpack('<fff', bytes(an_packet.data[0:12]))
            self.standard_deviation = unpack('<f', bytes(an_packet.data[12:16]))[0]
            return 0
        elif (an_packet.id == self.ID) and (len(an_packet.data) == 24):
            self.velocity = unpack('<fff', bytes(an_packet.data[0:12]))
            self.standard_deviation = unpack('<fff', bytes(an_packet.data[12:24]))
        else:
            return 1

    def encode(self):
        """Encode External Body Velocity Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<fff', self.velocity[0], self.velocity[1], self.velocity[2])
        data += pack('<fff', self.standard_deviation[0], self.standard_deviation[1], self.standard_deviation[2])

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
