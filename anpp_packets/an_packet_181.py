################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_181.py                              ##
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
class PacketPeriod:
    """Packet Period"""
    packet_id: int = 0
    period: int = 0

    LENGTH = 5

    def unpack(self, data):
        """Unpack data bytes"""
        self.packet_id = data[0]
        self.period = unpack('<I', data[1:4])[0]

    def pack(self):
        return pack('<BI', self.packet_id, self.period)


@dataclass()
class PacketsPeriodPacket:
    """Packet 181 - Packets Period Packet"""
    permanent: int = 0
    clear_existing_packets: int = 0
    packet_periods: [PacketPeriod] = field(default_factory=list)

    ID = PacketID.packets_period
    MINIMUM_LENGTH = 2
    MAXIMUM_PACKET_PERIODS = 50

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Packets Period Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and ((len(an_packet.data) - self.MINIMUM_LENGTH) % PacketPeriod.LENGTH == 0):
            packet_periods_count = int((an_packet.length - self.MINIMUM_LENGTH) / PacketPeriod.LENGTH)
            self.permanent = an_packet.data[0]
            self.clear_existing_packets = an_packet.data[1]
            for i in range(packet_periods_count):
                index = 2 + i * PacketPeriod.LENGTH
                self.packet_periods[i].unpack(an_packet.data[index:index+PacketPeriod.LENGTH])
            return 0
        else:
            return 1

    def encode(self):
        """Encode Packets Period Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<B', self.permanent)
        data += pack('<I', self.clear_existing_packets)
        number_of_periods = int(len(self.packet_periods) / PacketPeriod.LENGTH)
        for i in range(number_of_periods):
            data += self.packet_periods[i].pack()

        an_packet = ANPacket()
        an_packet.encode(self.ID, (2 + PacketPeriod.LENGTH * number_of_periods), data)

        return an_packet
