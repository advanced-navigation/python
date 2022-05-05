################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_80.py                              ##
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
from anpp_packets.an_packet_20 import GNSSFixType


@dataclass()
class BasestationPacket:
    """Packet 80 - Basestation Packet"""
    unix_time: int = 0
    microseconds: int = 0
    position_latitude: float = 0
    position_longitude: float = 0
    position_altitude: float = 0
    relative_position_north: float = 0
    relative_position_east: float = 0
    relative_position_down: float = 0
    gnss_fix_status: int = GNSSFixType.none

    ID = PacketID.base_station
    LENGTH = 45

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Basestation Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.unix_time = unpack('<I', bytes(an_packet.data[0:4]))[0]
            self.microseconds = unpack('<I', bytes(an_packet.data[4:8]))[0]
            self.position_latitude = unpack('<d', bytes(an_packet.data[8:16]))[0]
            self.position_longitude = unpack('<d', bytes(an_packet.data[16:24]))[0]
            self.position_altitude = unpack('<d', bytes(an_packet.data[24:32]))[0]
            self.relative_position_north = unpack('<f', bytes(an_packet.data[32:36]))[0]
            self.relative_position_east = unpack('<f', bytes(an_packet.data[36:40]))[0]
            self.relative_position_down = unpack('<f', bytes(an_packet.data[40:44]))[0]
            self.gnss_fix_status = unpack('<B', bytes(an_packet.data[45]))[0]
            return 0
        else:
            return 1
