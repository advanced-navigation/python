################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_13.py                              ##
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

from dataclasses import dataclass, field
from enum import Enum
from struct import unpack
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
    serial_number: [int] * 3 = field(default_factory=list)
    device_subtype: int = 0

    ID = PacketID.extended_device_information
    LENGTH = 36

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Extended Device Information Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.software_version = unpack('<I', an_packet.data[0:4])[0]
            self.device_id = DeviceID(unpack('<I', an_packet.data[4:8])[0])
            self.hardware_revision = unpack('<I', an_packet.data[8:12])[0]
            self.serial_number = unpack('<III', an_packet.data[12:24])
            self.device_subtype = unpack('<I', an_packet.data[24:28])[0]
            return 0
        else:
            return 1
