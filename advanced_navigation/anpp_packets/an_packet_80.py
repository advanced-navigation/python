################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_80.py                              ##
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

from dataclasses import dataclass
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket
from .an_packet_20 import GNSSFixType


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
    gnss_fix_status: GNSSFixType = GNSSFixType.none

    ID = PacketID.base_station
    LENGTH = 45

    _structure = struct.Struct("<IIdddfffB")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Basestation Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.unix_time,
                self.microseconds,
                self.position_latitude,
                self.position_longitude,
                self.position_altitude,
                self.relative_position_north,
                self.relative_position_east,
                self.relative_position_down,
                self.gnss_fix_status,
            ) = self._structure.unpack_from(an_packet.data)
            return 0
        else:
            return 1
