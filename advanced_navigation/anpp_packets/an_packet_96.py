################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_96.py                              ##
##                     Copyright 2023, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2026 Advanced Navigation                                       #
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
class PoseInitialisationPacket:
    """Pose Initialisation Packet"""

    rBOe_llh: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0], repr=False)
    rBOn_SD: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0], repr=False)
    eulernb: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0], repr=False)
    eulernb_SD: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0], repr=False)
    dErBOn: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0], repr=False)
    dErBOn_SD: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0], repr=False)
    reserved: List[int] = field(default_factory=lambda: [0] * 24, repr=False)

    ID = PacketID.pose_initialisation 
    LENGTH = 108

    # <    : Little-endian
    # 3d   : 3 doubles (8 bytes each)
    # 15f  : 15 floats (4 bytes each)
    # 24B  : 24 unsigned chars (1 byte each)
    _structure = struct.Struct("<3d15f24B")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Pose Initialisation Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            
            self.rBOe_llh = list(values[0:3])
            self.rBOn_SD = list(values[3:6])
            self.eulernb = list(values[6:9])
            self.eulernb_SD = list(values[9:12])
            self.dErBOn = list(values[12:15])
            self.dErBOn_SD = list(values[15:18])
            self.reserved = list(values[18:42])
            
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode Pose Initialisation Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            *self.rBOe_llh,
            *self.rBOn_SD,
            *self.eulernb,
            *self.eulernb_SD,
            *self.dErBOn,
            *self.dErBOn_SD,
            *self.reserved,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet