################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_14.py                              ##
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
from struct import unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket
from anpp_packets.an_packet_3 import DeviceID


@dataclass()
class SubcomponentInformation:
    """Subcomponent Information"""
    software_version: int = 0
    device_id: DeviceID = DeviceID.unknown
    hardware_revision: int = 0
    serial_number: [int] * 3 = field(default_factory=list)

    LENGTH = 24

    def unpack(self, data):
        self.software_version = unpack('<I', data[0:4])[0]
        self.device_id = DeviceID(unpack('<I', data[4:8])[0])
        self.hardware_revision = unpack('<I', data[8:12])[0]
        self.serial_number = unpack('<III', data[12:24])


@dataclass()
class SubcomponentInformationPacket:
    """Packet 14 - Subcomponent Information Packet"""
    subcomponents_information: [SubcomponentInformation] = field(default_factory=list)

    ID = PacketID.subcomponent_information

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Subcomponent Information Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) % SubcomponentInformation.LENGTH == 0):
            subcomponents = int(len(an_packet.data) % SubcomponentInformation.LENGTH)
            for i in range(subcomponents):
                index = SubcomponentInformation.LENGTH * i
                self.subcomponents_information.append(SubcomponentInformation())
                self.subcomponents_information[i].unpack(an_packet.data[index:index+SubcomponentInformation.LENGTH])
            return 0
        else:
            return 1
