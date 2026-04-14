################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_1.py                               ##
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

from .an_packet_protocol import ANPacket
from advanced_navigation.anpp_packets.an_packets import PacketID


@dataclass()
class RequestPacket:
    """Packet 1 - Request Packet"""

    requested_packets: List[PacketID] = field(default_factory=list, repr=False)

    ID = PacketID.request

    _structure = struct.Struct("<B")

    def encode(self) -> ANPacket:
        """Encode Request Packet to ANPacket
        Returns the ANPacket"""
        if not isinstance(self.requested_packets, list):
            self.requested_packets = [self.requested_packets]

        data = bytes()
        for packet in self.requested_packets:
            data += self._structure.pack(PacketID(packet).value)

        an_packet = ANPacket()
        an_packet.encode(self.ID, len(data), data)

        return an_packet
