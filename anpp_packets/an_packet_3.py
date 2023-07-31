################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_3.py                               ##
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


class DeviceID(Enum):
    unknown = 0
    spatial = 1
    orientus = 3
    spatial_fog = 4
    spatial_dual = 5
    obdii_odometer = 10
    orientus_v3 = 11
    ilu = 12
    air_data_unit = 13
    spatial_fog_dual = 16
    motus = 17
    gnss_compass = 18
    certus = 26
    aries = 27
    boreas_d90 = 28
    boreas_d90_fpga = 35
    boreas_coil = 36


@dataclass()
class DeviceInformationPacket:
    """Packet 3 - Device Information Packet"""

    software_version: int = 0
    device_id: DeviceID = DeviceID.unknown
    hardware_revision: int = 0
    serial_number: List[int] = field(default_factory=lambda: [0, 0, 0], repr=False)

    ID = PacketID.device_information
    LENGTH = 24

    _structure = struct.Struct("<IIIIII")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Device Information Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.software_version,
                device_id_value,
                self.hardware_revision,
                *self.serial_number,
            ) = self._structure.unpack_from(an_packet.data)
            self.device_id = DeviceID(device_id_value)
            return 0
        else:
            return 1
