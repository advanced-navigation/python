################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_185.py                              ##
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
class InstallationAlignmentPacket:
    """Packet 185 - Installation Alignment Packet"""

    permanent: int = 0
    alignment_dcm: List[List[float]] = field(
        default_factory=lambda: [[0.0] * 3] * 3, repr=False
    )
    gnss_antenna_offset: List[float] = field(
        default_factory=lambda: [0, 0, 0], repr=False
    )
    odometer_offset: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    external_data_offset: List[float] = field(
        default_factory=lambda: [0, 0, 0], repr=False
    )

    ID = PacketID.installation_alignment
    LENGTH = 73

    _structure = struct.Struct("<B18f")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Installation Alignment Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.permanent = values[0]
            self.alignment_dcm = [
                list(values[1:4]),
                list(values[4:7]),
                list(values[7:10]),
            ]
            self.gnss_antenna_offset = list(values[10:13])
            self.odometer_offset = list(values[13:16])
            self.external_data_offset = list(values[16:19])
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode Installation Alignment Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            *self.alignment_dcm[0],
            *self.alignment_dcm[1],
            *self.alignment_dcm[2],
            *self.gnss_antenna_offset,
            *self.odometer_offset,
            *self.external_data_offset
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
