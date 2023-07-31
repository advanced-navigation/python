################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_0.py                               ##
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
from enum import Enum
import struct
from dataclasses import dataclass
from anpp_packets.an_packet_protocol import ANPacket
from anpp_packets.an_packets import PacketID


class AcknowledgeResult(Enum):
    """Acknowledge Result"""

    success = 0
    failure_crc = 1
    failure_length = 2
    failure_range = 3
    failure_flash = 4
    failure_not_ready = 5
    failure_unknown_packet = 6


@dataclass()
class AcknowledgePacket:
    """Packet 0 - Acknowledge Packet"""

    packet_id: PacketID = PacketID.acknowledge
    packet_crc: int = 0
    acknowledge_result: AcknowledgeResult = AcknowledgeResult.success

    ID = PacketID.acknowledge
    LENGTH = 4

    _structure = struct.Struct("<BHB")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Acknowledge Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.packet_id = PacketID(values[0])
            self.packet_crc = values[1]
            self.acknowledge_result = AcknowledgeResult(values[2])
            return 0
        else:
            return 1
