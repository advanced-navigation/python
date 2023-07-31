################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_13.py                              ##
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
from enum import Enum
from typing import List
import struct
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket
from anpp_packets.an_packet_3 import DeviceID


class CertusDeviceSubtype(Enum):
    """Certus Device Subtype"""

    certus = 0
    certus_evo = 1
    certus_oem = 2
    certus_evo_oem = 3


@dataclass()
class ExtendedDeviceInformationPacket:
    """Packet 13 - Extended Device Information Packet"""

    software_version: int = 0
    device_id: DeviceID = DeviceID.unknown
    hardware_revision: int = 0
    serial_number: List[int] = field(default_factory=lambda: [0, 0, 0], repr=False)
    device_subtype: int = 0

    ID = PacketID.extended_device_information
    LENGTH = 36

    _structure = struct.Struct("<IIIIIII8x")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Extended Device Information Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.software_version = values[0]
            self.device_id = values[1]
            self.hardware_revision = values[2]
            self.serial_number = list(values[3:6])
            self.device_subtype = values[6]
            return 0
        else:
            return 1
