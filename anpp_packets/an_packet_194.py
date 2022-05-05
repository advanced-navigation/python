################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_194.py                              ##
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
class ReferencePointOffsetsPacket:
    """Packet 194 - Reference Point Offsets Packet"""
    permanent: int = 0
    primary_reference_point_offset: [float] * 3 = field(default_factory=list)
    heave_point_2_offset: [float] * 3 = field(default_factory=list)
    heave_point_3_offset: [float] * 3 = field(default_factory=list)
    heave_point_4_offset: [float] * 3 = field(default_factory=list)

    ID = PacketID.reference_point_offsets
    LENGTH = 49

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Reference Point Offsets Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.permanent = an_packet.data[0]
            self.primary_reference_point_offset = unpack('<fff', bytes(an_packet.data[1:13]))[0]
            self.heave_point_2_offset = unpack('<fff', bytes(an_packet.data[13:25]))[0]
            self.heave_point_3_offset = unpack('<fff', bytes(an_packet.data[25:37]))[0]
            self.heave_point_4_offset = unpack('<fff', bytes(an_packet.data[37:49]))[0]
            return 0
        else:
            return 1

    def encode(self):
        """Encode Reference Point Offsets Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<Bffffffffffff', self.permanent,
                    self.primary_reference_point_offset[0], self.primary_reference_point_offset[1],
                    self.primary_reference_point_offset[2],
                    self.heave_point_2_offset[0], self.heave_point_2_offset[1], self.heave_point_2_offset[2],
                    self.heave_point_3_offset[0], self.heave_point_3_offset[1], self.heave_point_3_offset[2],
                    self.heave_point_4_offset[0], self.heave_point_4_offset[1], self.heave_point_4_offset[2])

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
