################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_199.py                              ##
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
class GPIOInputConfigurationPacket:
    """Packet 199 - GPIO Input Configuration Packet"""

    permanent: int = 0
    gimbal_radians_per_encoder_tick: float = 0

    ID = PacketID.gpio_input_configuration
    LENGTH = 65

    _structure = struct.Struct("<Bf60x")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to GPIO Input Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.permanent,
                self.gimbal_radians_per_encoder_tick,
            ) = self._structure.unpack(an_packet.data)
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode GPIO Input Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent, self.gimbal_radians_per_encoder_tick
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
