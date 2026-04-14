################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_93.py                              ##
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
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


@dataclass()
class OrientationStatus:
    """GNSS Orientation Status Bitfield"""

    fix_type: int = 0
    antenna_disconnected: bool = False 
    antenna_short: bool = False 
    gnss_failure: bool = False
    spoofing_status: int = 0
    interference_status: int = 0 
    reserved: int = 0

    def unpack(self, flags_gnss):
        """Unpack data bytes"""
        self.fix_type = flags_gnss & 0x0007
        self.antenna_disconnected = (flags_gnss & (1 << 3)) != 0
        self.antenna_short = (flags_gnss & (1 << 4)) != 0 
        self.gnss_failure = (flags_gnss & (1 << 5)) != 0 
        self.spoofing_status = (flags_gnss &  0x01C0) >> 6
        self.interference_status = (flags_gnss & 0x0E00) >> 9
        self.reserved = (flags_gnss & 0xF000) >> 12

    def pack(self) -> int:
        """Pack the flags into a 16 bit integer"""
        flags_gnss = self.fix_type & 0x0007
        flags_gnss |= int(self.antenna_disconnected) << 3
        flags_gnss |= int(self.antenna_short) << 4
        flags_gnss |= int(self.gnss_failure) << 5
        flags_gnss |= (self.spoofing_status << 6) & 0x01C0
        flags_gnss |= (self.interference_status << 9) & 0x0E00 
        flags_gnss |= (self.reserved << 12) & 0xF000
        return flags_gnss


@dataclass()
class GNSSOrientationPacket:
    """Packet 93 - GNSS Orientation Packet"""

    gnss_id: int = 0
    reserved: int = 0
    gnss_orientation_status_bitfield: OrientationStatus = field(default_factory=OrientationStatus, repr=False) 
    posix_time_s: int = 0 
    posix_time_micros: int = 0 
    azimuth_gnss_antennas_baseline: float = 0 
    azimuth_standard_deviation: float = 0 
    tilt_gnss_antennas_baseline: float = 0
    tilt_standard_deviation: float = 0
    baseline_length: float = 0 
    latency_micros: int = 0

    ID = PacketID.gnss_orientation
    LENGTH = 36

    _structure = struct.Struct("<BBHIIfffffI")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to GNSS Orientation Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            (self.gnss_id, self.reserved) = values[0:2]
            flags_gnss = values[2] 
            self.gnss_orientation_status_bitfield.unpack(flags_gnss)
            (
                self.posix_time_s, 
                self.posix_time_micros, 
                self.azimuth_gnss_antennas_baseline, 
                self.azimuth_standard_deviation, 
                self.tilt_gnss_antennas_baseline, 
                self.tilt_standard_deviation, 
                self.baseline_length,
                self.latency_micros
            ) = values[3:]

            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode GNSS Orientation Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.gnss_id,
            self.reserved,
            self.gnss_orientation_status_bitfield.pack(),
            self.posix_time_s, 
            self.posix_time_micros, 
            self.azimuth_gnss_antennas_baseline, 
            self.azimuth_standard_deviation, 
            self.tilt_gnss_antennas_baseline, 
            self.tilt_standard_deviation, 
            self.baseline_length,
            self.latency_micros
        )
        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
