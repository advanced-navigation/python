################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_30.py                              ##
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


@dataclass()
class SatellitesPacket:
    """Packet 30 - Satellites Packet"""

    hdop: float = 0
    vdop: float = 0
    gps_satellites: int = 0
    glonass_satellites: int = 0
    beidou_satellites: int = 0
    galileo_satellites: int = 0
    sbas_satellites: int = 0

    ID = PacketID.satellites
    LENGTH = 13

    _structure = struct.Struct("<ffBBBBB")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Satellites Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.hdop,
                self.vdop,
                self.gps_satellites,
                self.glonass_satellites,
                self.beidou_satellites,
                self.galileo_satellites,
                self.sbas_satellites,
            ) = self._structure.unpack_from(an_packet.data)
            return 0
        else:
            return 1
