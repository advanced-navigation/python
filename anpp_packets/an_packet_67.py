################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_67.py                              ##
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
from struct import pack, unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class OdometerFlags:
    """Odometer Flags"""
    reverse_detection_supported: bool = False

    def unpack(self, flags_byte):
        """Unpack data bytes"""
        self.reverse_detection_supported = (flags_byte & (1 << 0)) != 0

    def pack(self):
        return self.reverse_detection_supported << 0


@dataclass()
class ExternalOdometerPacket:
    """Packet 67 - External Odometer Packet"""
    estimated_delay: float = 0
    speed: float = 0
    distance_travelled: float = 0  # Only valid for OBDII input
    flags: OdometerFlags = OdometerFlags()

    ID = PacketID.external_odometer
    LENGTH = 13

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to External Odometer Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.estimated_delay = unpack('<f', bytes(an_packet.data[0:4]))[0]
            self.speed = unpack('<f', bytes(an_packet.data[4:8]))[0]
            self.distance_travelled = unpack('<f', bytes(an_packet.data[8:12]))[0]
            self.flags.unpack(an_packet.data[12])
            return 0
        else:
            return 1

    def encode(self):
        """Encode External Odometer Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<f', self.estimated_delay)
        data += pack('<f', self.speed)
        data += pack('<f', self.distance_travelled)
        data += pack('<B', self.flags.pack())

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet