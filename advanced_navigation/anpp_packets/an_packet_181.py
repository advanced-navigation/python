################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_181.py                              ##
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
class PacketPeriod:
    """Packet Period"""

    packet_id: int = 0
    period: int = 0

    LENGTH = 5

    _structure = struct.Struct("<BI")

    def unpack(self, data):
        """Unpack data bytes"""
        (
            self.packet_id,
            self.period,
        ) = self._structure.unpack_from(data)

    def pack(self):
        return self._structure.pack(self.packet_id, self.period)


@dataclass()
class PacketsPeriodPacket:
    """Packet 181 - Packets Period Packet"""

    permanent: int = 0
    clear_existing_packets: int = 0
    packet_periods: List[PacketPeriod] = field(default_factory=list, repr=False)

    ID = PacketID.packets_period
    MINIMUM_LENGTH = 2
    MAXIMUM_PACKET_PERIODS = 50

    _structure = struct.Struct("BB")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Packets Period Packet
        Returns 0 on success and 1 on failure"""
        if (
            an_packet.id != self.ID
            or (len(an_packet.data) - self.MINIMUM_LENGTH) % PacketPeriod.LENGTH != 0
        ):
            return 1
        packet_periods_count = int(
            (an_packet.length - self.MINIMUM_LENGTH) / PacketPeriod.LENGTH
        )
        self.permanent = an_packet.data[0]
        self.clear_existing_packets = an_packet.data[1]
        self.packet_periods = [PacketPeriod()] * packet_periods_count
        for i in range(packet_periods_count):
            index = self.MINIMUM_LENGTH + i * PacketPeriod.LENGTH
            self.packet_periods[i].unpack(
                an_packet.data[index : index + PacketPeriod.LENGTH]
            )
        return 0

    def encode(self) -> ANPacket:
        """Encode Packets Period Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(self.permanent, self.clear_existing_packets)
        for i in range(len(self.packet_periods)):
            data += self.packet_periods[i].pack()

        an_packet = ANPacket()
        an_packet.encode(
            self.ID,
            (self.MINIMUM_LENGTH + PacketPeriod.LENGTH * len(self.packet_periods)),
            data,
        )

        return an_packet
