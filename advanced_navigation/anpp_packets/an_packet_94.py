################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_94.py                              ##
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
class LvsLineOfSightPacketFlags:
    """LVS Line of Sight Packet Flags"""
    delay_us_valid: bool = False
    velocity_m_per_s_valid: bool = False
    velocity_standard_deviation_m_per_s_valid: bool = False
    range_m_valid: bool = False
    range_standard_deviation_m_valid: bool = False

    def unpack(self, data: int):
        """Unpack data bytes"""
        self.delay_us_valid = (data & (1 << 0)) != 0
        self.velocity_m_per_s_valid = (data & (1 << 1)) != 0
        self.velocity_standard_deviation_m_per_s_valid = (data & (1 << 2)) != 0
        self.range_m_valid = (data & (1 << 3)) != 0
        self.range_standard_deviation_m_valid = (data & (1 << 4)) != 0

    def pack(self) -> int:
        """Pack data bytes"""
        data = self.delay_us_valid << 0
        data |= self.velocity_m_per_s_valid << 1
        data |= self.velocity_standard_deviation_m_per_s_valid << 2
        data |= self.range_m_valid << 3
        data |= self.range_standard_deviation_m_valid << 4
        return data


@dataclass()
class LvsLineOfSightPacketTelescope:
    """LVS Line of Sight Packet Telescope Sub-structure"""
    flags: LvsLineOfSightPacketFlags = field(
        default_factory=LvsLineOfSightPacketFlags, repr=False
    )
    delay_us: int = 0
    velocity_m_per_s: float = 0.0
    velocity_standard_deviation_m_per_s: float = 0.0
    range_m: float = 0.0
    range_standard_deviation_m: float = 0.0

    _structure = struct.Struct("<HHffff")

    def unpack_from(self, data: bytes, offset: int = 0):
        """Unpack from a specific offset within the packet data"""
        values = self._structure.unpack_from(data, offset)
        self.flags.unpack(values[0])
        self.delay_us = values[1]
        self.velocity_m_per_s = values[2]
        self.velocity_standard_deviation_m_per_s = values[3]
        self.range_m = values[4]
        self.range_standard_deviation_m = values[5]

    def pack(self) -> bytes:
        """Pack to bytes"""
        return self._structure.pack(
            self.flags.pack(),
            self.delay_us,
            self.velocity_m_per_s,
            self.velocity_standard_deviation_m_per_s,
            self.range_m,
            self.range_standard_deviation_m,
        )


@dataclass()
class LvsLineOfSightPacket:
    """Packet 94 - LVS Line of Sight Packet"""
    unix_time_us: int = 0
    telescope: List[LvsLineOfSightPacketTelescope] = field(
        default_factory=lambda: [LvsLineOfSightPacketTelescope() for _ in range(4)], repr=False
    )

    ID = PacketID.lvs_line_of_sight
    LENGTH = 88

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to LVS Line of Sight Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            # Unpack the initial 8-byte uint64 timestamp
            self.unix_time_us = struct.unpack_from("<Q", an_packet.data, 0)[0]
            
            # Unpack the array of 4 telescope objects (20 bytes each, starting at offset 8)
            for i in range(4):
                offset = 8 + (i * 20)
                self.telescope[i].unpack_from(an_packet.data, offset)
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode LVS Line of Sight Packet to ANPacket
        Returns the ANPacket"""
        data = struct.pack("<Q", self.unix_time_us)
        for i in range(4):
            data += self.telescope[i].pack()

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet