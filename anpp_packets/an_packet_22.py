################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_3.py                               ##
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
from struct import unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class FormattedTimePacket:
    """Packet 22 - Formatted Time Packet"""
    microseconds: int = 0
    year: int = 0
    year_day: int = 0
    month: int = 0
    month_day: int = 0
    week_day: int = 0
    hour: int = 0
    minute: int = 0
    second: int = 0

    ID = PacketID.formatted_time
    LENGTH = 14

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Formatted Time Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.microseconds = unpack('<I', an_packet.data[0:4])[0]
            self.year = unpack('<H', an_packet.data[4:6])[0]
            self.year_day = unpack('<H', an_packet.data[6:8])[0]
            self.month = an_packet.data[8]
            self.month_day = an_packet.data[9]
            self.week_day = an_packet.data[10]
            self.hour = an_packet.data[11]
            self.minute = an_packet.data[12]
            self.second = an_packet.data[13]
            return 0
        else:
            return 1
