################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_182.py                              ##
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

from dataclasses import dataclass
from struct import pack, unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class BaudRatesPacket:
    """Packet 182 - Baud Rates Packet"""
    permanent: int = 0
    primary_baud_rate: int = 0
    gpio_1_2_baud_rate: int = 0
    auxiliary_baud_rate: int = 0

    ID = PacketID.baud_rates
    LENGTH = 17

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Baud Rates Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.permanent = an_packet.data[0]
            self.primary_baud_rate = unpack('<I', bytes(an_packet.data[1:5]))[0]
            self.gpio_1_2_baud_rate = unpack('<I', bytes(an_packet.data[5:9]))[0]
            self.auxiliary_baud_rate = unpack('<I', bytes(an_packet.data[9:13]))[0]
            return 0
        else:
            return 1

    def encode(self):
        """Encode Baud Rates Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<B', self.permanent)
        data += pack('<I', self.primary_baud_rate)
        data += pack('<I', self.gpio_1_2_baud_rate)
        data += pack('<I', self.auxiliary_baud_rate)
        data += pack('<I', 0)

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
