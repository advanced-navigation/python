################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_92.py                              ##
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

from dataclasses import dataclass, field
import struct
from typing import List
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


@dataclass()
class StatusGNSS:
    """GNSS Position Velocity Time Status Bitfield"""

    fix_type: int = 0
    spoofing_status: int = 0
    interference_status: int = 0
    velocity_valid: bool = False
    time_valid: bool = False
    antenna_disconnected: bool = False 
    antenna_short: bool = False 
    gnss_failure: bool = False 
    reserved: int = 0

    def unpack(self, flags_gnss):
        """Unpack data bytes"""
        self.fix_type = flags_gnss & 0x0007
        self.spoofing_status = (flags_gnss & 0x0038) >> 3
        self.interference_status = (flags_gnss & 0x01C0) >> 6 
        self.velocity_valid = (flags_gnss & (1 << 9)) != 0
        self.time_valid = (flags_gnss & (1 << 10)) != 0
        self.antenna_disconnected = (flags_gnss & (1 << 11)) != 0
        self.antenna_short = (flags_gnss & (1 << 12)) != 0
        self.gnss_failure = (flags_gnss & (1 << 13)) != 0
        self.reserved = (flags_gnss & 0xC000) >> 14

    def pack(self) -> int:
        """Pack the boolean flags into a 16 bit integer"""
        flags_gnss = self.fix_type & 0x0007
        flags_gnss |= (self.spoofing_status << 3) & 0x0038
        flags_gnss |= (self.interference_status << 6) & 0x01C0 
        flags_gnss |= int(self.velocity_valid) << 9
        flags_gnss |= int(self.time_valid) << 10
        flags_gnss |= int(self.antenna_disconnected) << 11
        flags_gnss |= int(self.antenna_short) << 12
        flags_gnss |= int(self.gnss_failure) << 13
        flags_gnss |= (self.reserved << 14) & 0xC000
        return flags_gnss


@dataclass()
class GNSSPositionVelocityTimePacket:
    """Packet 92 - GNSS Position Velocity Time Packet"""

    gnss_id: int = 0
    reserved: int = 0
    gnss_position_velocity_time_bitfield: StatusGNSS = field(default_factory=StatusGNSS, repr=False) 
    posix_time_s: int = 0 
    posix_time_micros: int = 0 
    position: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    position_standard_deviation: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    velocity: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    velocity_standard_deviation: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    latency_micros: int = 0

    ID = PacketID.gnss_position_velocity_time
    LENGTH = 76

    _structure = struct.Struct("<BBHIIdddfffffffffI")
    
    def decode(self, an_packet: ANPacket) -> int:
            """Decode ANPacket to GNSS Position Velocity Time Packet
            Returns 0 on success and 1 on failure"""
            if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
                values = self._structure.unpack_from(an_packet.data)
                
                (self.gnss_id, self.reserved) = values[0:2]
                
                flags_gnss = values[2] 
                self.gnss_position_velocity_time_bitfield.unpack(flags_gnss)

                self.posix_time_s = values[3]
                self.posix_time_micros = values[4]

                self.position = list(values[5:8])                    
                self.position_standard_deviation = list(values[8:11]) 
                self.velocity = list(values[11:14])                   
                self.velocity_standard_deviation = list(values[14:17])
                
                self.latency_micros = values[17]

                return 0
            else:
                return 1

    def encode(self) -> ANPacket:
        """Encode GNSS Position Velocity Time Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.gnss_id,
            self.reserved,
            self.gnss_position_velocity_time_bitfield.pack(),
            self.posix_time_s, 
            self.posix_time_micros, 
            *self.position, 
            *self.position_standard_deviation, 
            *self.velocity, 
            *self.velocity_standard_deviation, 
            self.latency_micros
        )
        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
