################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_209.py                              ##
##                     Copyright 2026, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2026 Advanced Navigation                                       #
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
class ExternalTemperatureSensorConfigurationPacket:
    """Packet 209 - External Temperature Sensor Configuration Packet"""

    permanent: int = 0
    reference_resistance_ohms: float = 0
    beta_value: float = 0

    ID = PacketID.external_temperature_sensor_configuration
    LENGTH = 36

    _structure = struct.Struct("<Bxxxff24x")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to  External Temperature Sensor Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.permanent,
                self.reference_resistance_ohms,
                self.beta_value,
            ) = self._structure.unpack_from(an_packet.data)
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode External Temperature Sensor Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.reference_resistance_ohms,
            self.beta_value,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
