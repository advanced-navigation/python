################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_196.py                              ##
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
from enum import Enum
from struct import pack, unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


class OffsetType(Enum):
    """Offset Type"""
    manual_offset = 0
    automatic_offset = 1


class AutomaticOffsetOrientation(Enum):
    """Automatic Offset Orientation"""
    primary_front_secondary_rear = 0
    primary_read_secondary_front = 1
    primary_right_secondary_left = 2
    primary_left_secondary_right = 3


@dataclass()
class DualAntennaConfigurationPacket:
    """Packet 196 - Dual Antenna Configuration Packet"""
    permanent: int = 0
    offset_type: OffsetType = OffsetType.manual_offset
    automatic_offset_orientation: AutomaticOffsetOrientation = AutomaticOffsetOrientation.primary_front_secondary_rear
    manual_offset_x: float = 0
    manual_offset_y: float = 0
    manual_offset_z: float = 0

    ID = PacketID.dual_antenna_configuration
    LENGTH = 17

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Dual Antenna Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.permanent = an_packet.data[0]
            self.offset_type = OffsetType(unpack('<H', an_packet.data[1:3])[0])
            self.automatic_offset_orientation = AutomaticOffsetOrientation(an_packet.data[3])
            self.manual_offset_x = unpack('<f', bytes(an_packet.data[5:9]))[0]
            self.manual_offset_y = unpack('<f', bytes(an_packet.data[9:13]))[0]
            self.manual_offset_z = unpack('<f', bytes(an_packet.data[13:17]))[0]
            return 0
        else:
            return 1

    def encode(self):
        """Encode Dual Antenna Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<BHBB', self.permanent, self.offset_type.value, self.automatic_offset_orientation.value, 0)
        data += pack('<fff', self.manual_offset_x, self.manual_offset_y, self.manual_offset_z)

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
