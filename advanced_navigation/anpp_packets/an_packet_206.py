################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_206.py                              ##
##                     Copyright 2026, Advanced Navigation                    ##
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
class LvsAlignmentAndOffset:
    """LVS Alignment and Offset Sub-structure"""
    azimuth_st: float = 0.0
    elevation_st: float = 0.0
    rTSs: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0], repr=False)

    # <    : Little-endian
    # 5f   : 5 floats (4 bytes each = 20 bytes total)
    _structure = struct.Struct("<5f")

    def unpack_from(self, data: bytes, offset: int = 0):
        """Unpack from a specific offset within the packet data"""
        values = self._structure.unpack_from(data, offset)
        self.azimuth_st = values[0]
        self.elevation_st = values[1]
        self.rTSs = list(values[2:5])

    def pack(self) -> bytes:
        """Pack data bytes"""
        return self._structure.pack(
            self.azimuth_st,
            self.elevation_st,
            *self.rTSs,
        )


@dataclass()
class LvsLineOfSightConfiguration:
    """LVS Line of Sight Configuration"""
    telescope: List[LvsAlignmentAndOffset] = field(
        default_factory=lambda: [LvsAlignmentAndOffset() for _ in range(4)], repr=False
    )

    def unpack_from(self, data: bytes, offset: int = 0):
        """Unpack the 4 telescope structs from a specific offset"""
        for i in range(4):
            # Each telescope is 20 bytes long
            self.telescope[i].unpack_from(data, offset + (i * 20))

    def pack(self) -> bytes:
        """Pack data bytes"""
        data = b""
        for i in range(4):
            data += self.telescope[i].pack()
        return data


@dataclass()
class LvsLineOfSightConfigurationPacket:
    """Packet 206 - LVS Line of Sight Configuration Packet"""
    permanent: int = 0
    configuration: LvsLineOfSightConfiguration = field(
        default_factory=LvsLineOfSightConfiguration, repr=False
    )

    ID = PacketID.lvs_line_of_sight_configuration
    LENGTH = 81

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to LVS Line of Sight Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            # Unpack the initial 1-byte uint8 (permanent)
            self.permanent = struct.unpack_from("<B", an_packet.data, 0)[0]
            
            # Unpack the 80-byte configuration struct starting at offset 1
            self.configuration.unpack_from(an_packet.data, 1)
            
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode LVS Line of Sight Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = struct.pack("<B", self.permanent)
        data += self.configuration.pack()

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet