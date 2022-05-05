################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_29.py                              ##
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
from struct import pack, unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class RawGNSSFlags:
    """Raw GNSS Flags"""
    fix_type: int = 0
    doppler_velocity_valid: bool = False
    time_valid: bool = False
    external_gnss: bool = False
    tilt_valid: bool = False
    """Only valid if an external dual antenna GNSS system is connected"""
    heading_valid: bool = False
    """Only valid if an external dual antenna GNSS system is connected"""
    floating_ambiguity_heading: bool = False
    antenna_1_disconnected: bool = False
    antenna_2_disconnected: bool = False
    antenna_1_short: bool = False
    antenna_2_short: bool = False
    gnns_1_failure: bool = False
    gnns_2_failure: bool = False

    def unpack(self, flags_byte):
        """Unpack data bytes"""
        self.fix_type = (flags_byte & 0x0007)
        self.doppler_velocity_valid = (flags_byte & (1 << 3)) != 0
        self.time_valid = (flags_byte & (1 << 4)) != 0
        self.external_gnss = (flags_byte & (1 << 5)) != 0
        self.tilt_valid = (flags_byte & (1 << 6)) != 0
        self.heading_valid = (flags_byte & (1 << 7)) != 0
        self.floating_ambiguity_heading = (flags_byte & (1 << 8)) != 0
        self.antenna_1_disconnected = (flags_byte & (1 << 10)) != 0
        self.antenna_2_disconnected = (flags_byte & (1 << 11)) != 0
        self.antenna_1_short = (flags_byte & (1 << 12)) != 0
        self.antenna_2_short = (flags_byte & (1 << 13)) != 0
        self.gnns_1_failure = (flags_byte & (1 << 14)) != 0
        self.gnns_2_failure = (flags_byte & (1 << 15)) != 0


@dataclass()
class RawGNSSPacket:
    """Packet 29 - Raw GNSS Packet"""
    unix_time_seconds: int = 0
    microseconds: int = 0
    position: [float] * 3 = field(default_factory=list)
    velocity: [float] * 3 = field(default_factory=list)
    position_standard_deviation: [float] * 3 = field(default_factory=list)
    tilt: float = 0
    """Only valid if an external dual antenna GNSS system is connected"""
    heading: float = 0
    """Only valid if an external dual antenna GNSS system is connected"""
    tilt_standard_deviation: float = 0
    """Only valid if an external dual antenna GNSS system is connected"""
    heading_standard_deviation: float = 0
    """Only valid if an external dual antenna GNSS system is connected"""
    flags: RawGNSSFlags = RawGNSSFlags()

    ID = PacketID.raw_gnss
    LENGTH = 74

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Raw GNSS Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.unix_time_seconds = unpack('<I', bytes(an_packet.data[0:4]))[0]
            self.microseconds = unpack('<I', bytes(an_packet.data[4:8]))[0]
            self.position = unpack('<ddd', bytes(an_packet.data[8:32]))
            self.velocity = unpack('<fff', bytes(an_packet.data[32:44]))
            self.position_standard_deviation = unpack('<fff', bytes(an_packet.data[44:56]))
            self.tilt = unpack('<f', bytes(an_packet.data[56:60]))[0]
            self.heading = unpack('<f', bytes(an_packet.data[60:64]))[0]
            self.tilt_standard_deviation = unpack('<f', bytes(an_packet.data[64:68]))[0]
            self.heading_standard_deviation = unpack('<f', bytes(an_packet.data[68:72]))[0]
            self.flags.unpack(unpack('<H', bytes(an_packet.data[72:74]))[0])
            return 0
        else:
            return 1

    def encode(self):
        """Encode Raw GNSS Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<II', self.unix_time_seconds, self.microseconds)
        data += pack('<ddd', self.position[0], self.position[1], self.position[2])
        data += pack('<fff', self.velocity[0], self.velocity[1], self.velocity[2])
        data += pack('<fff', self.position_standard_deviation[0], self.position_standard_deviation[1],
                     self.position_standard_deviation[2])
        data += pack('<ff', self.tilt, self.heading)
        data += pack('<ff', self.tilt_standard_deviation, self.heading_standard_deviation)
        data += pack('<H', self.flags)

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
