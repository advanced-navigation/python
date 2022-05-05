################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_185.py                              ##
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
class InstallationAlignmentPacket:
    """Packet 185 - Installation Alignment Packet"""
    permanent: int = 0
    alignment_dcm: [[float] * 3] * 3 = field(default_factory=list)
    gnss_antenna_offset: [float] * 3 = field(default_factory=list)
    odometer_offset: [float] * 3 = field(default_factory=list)
    external_data_offset: [float] * 3 = field(default_factory=list)

    ID = PacketID.installation_alignment
    LENGTH = 73

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Installation Alignment Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.permanent = an_packet.data[0]
            self.alignment_dcm = [[unpack('<fff', bytes(an_packet.data[1:13]))],
                                  [unpack('<fff', bytes(an_packet.data[13:25]))],
                                  [unpack('<fff', bytes(an_packet.data[25:37]))]]
            self.gnss_antenna_offset = [unpack('<fff', bytes(an_packet.data[37:49]))]
            self.odometer_offset = [unpack('<fff', bytes(an_packet.data[49:61]))]
            self.external_data_offset = [unpack('<fff', bytes(an_packet.data[61:73]))]
            return 0
        else:
            return 1

    def encode(self):
        """Encode Installation Alignment Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<B', self.permanent)
        data += pack('<fff', self.alignment_dcm[0][0], self.alignment_dcm[0][1], self.alignment_dcm[0][2])
        data += pack('<fff', self.alignment_dcm[1][0], self.alignment_dcm[1][1], self.alignment_dcm[1][2])
        data += pack('<fff', self.alignment_dcm[2][0], self.alignment_dcm[2][1], self.alignment_dcm[2][2])
        data += pack('<fff', self.gnss_antenna_offset[0], self.gnss_antenna_offset[1], self.gnss_antenna_offset[2])
        data += pack('<fff', self.odometer_offset[0], self.odometer_offset[1], self.odometer_offset[2])
        data += pack('<fff', self.external_data_offset[0], self.external_data_offset[1],
                     self.external_data_offset[2])

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
