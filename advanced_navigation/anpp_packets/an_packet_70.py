################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_70.py                              ##
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
import struct
from typing import List
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


@dataclass
class RawDVLDataFlags:
    """Raw DVL Data Flags"""

    bottom_velocity_valid: bool = False
    water_velocity_valid: bool = False
    temperature_valid: bool = False
    depth_valid: bool = False
    altitude_valid: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.bottom_velocity_valid = (data & (1 << 0)) != 0
        self.water_velocity_valid = (data & (1 << 1)) != 0
        self.temperature_valid = (data & (1 << 2)) != 0
        self.depth_valid = (data & (1 << 3)) != 0
        self.altitude_valid = (data & (1 << 4)) != 0


@dataclass()
class RawDVLDataPacket:
    """Packet 70 - Raw DVL Data Packet"""

    unix_time: int = 0
    microseconds: int = 0
    status: RawDVLDataFlags = field(default_factory=RawDVLDataFlags, repr=False)
    bottom_velocity: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    bottom_velocity_standard_deviation: float = 0
    water_velocity: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    water_velocity_standard_deviation: float = 0
    water_velocity_layer_depth: float = 0
    depth: float = 0
    altitude: float = 0
    temperature: float = 0

    ID = PacketID.raw_dvl_data
    LENGTH = 60

    _structure = struct.Struct("<IIIffffffffffff")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Raw DVL Data Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            (self.unix_time, self.microseconds) = values[0:2]
            self.status.unpack(values[2])

            (*self.bottom_velocity, self.bottom_velocity_standard_deviation) = values[
                3:7
            ]
            (
                *self.water_velocity,
                self.water_velocity_standard_deviation,
                self.water_velocity_layer_depth,
                self.depth,
                self.altitude,
                self.temperature,
            ) = values[7:15]
            return 0
        else:
            return 1
