################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_208.py                              ##
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
class AidingSourceConfig2Enabled:
    """Aiding Source Config 2 Enabled Bitmask"""
    internal_depth_sensor: bool = False
    external_subsonus: bool = False
    external_dvl_data: bool = False
    external_depth: bool = False
    external_usbl: bool = False
    external_svs_data: bool = False

    def unpack(self, data: int):
        """Unpack data bytes"""
        self.internal_depth_sensor = (data & (1 << 0)) != 0
        self.external_subsonus = (data & (1 << 1)) != 0
        self.external_dvl_data = (data & (1 << 2)) != 0
        self.external_depth = (data & (1 << 3)) != 0
        self.external_usbl = (data & (1 << 4)) != 0
        self.external_svs_data = (data & (1 << 5)) != 0
        # Bits 6-15 are reserved

    def pack(self) -> int:
        """Pack data bytes"""
        data = self.internal_depth_sensor << 0
        data |= self.external_subsonus << 1
        data |= self.external_dvl_data << 2
        data |= self.external_depth << 3
        data |= self.external_usbl << 4
        data |= self.external_svs_data << 5
        return data


@dataclass()
class AidingSourceConfigPacket2:
    """Packet 208 - Aiding Source Config Packet 2"""
    permanent: int = 0
    enabled: AidingSourceConfig2Enabled = field(default_factory=AidingSourceConfig2Enabled, repr=False)

    internal_depth_sensor_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_subsonus_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_subsonus_eulerbs: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_dvl_data_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_dvl_data_eulerbs: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_depth_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_USBL_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    reserved: List[float] = field(default_factory=lambda: [0.0]*39, repr=False)

    ID = PacketID.aiding_source_config_2
    LENGTH = 243

    # <    : Little-endian
    # B    : 1 uint8 (permanent)
    # H    : 1 uint16 (enabled bitmask)
    # 60f  : 60 floats (7 arrays of 3 + 39 reserved = 60 floats = 240 bytes)
    _structure = struct.Struct("<BH60f")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Aiding Source Config Packet 2
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            
            self.permanent = values[0]
            self.enabled.unpack(values[1])
            
            self.internal_depth_sensor_rSBb = list(values[2:5])
            self.external_subsonus_rSBb = list(values[5:8])
            self.external_subsonus_eulerbs = list(values[8:11])
            self.external_dvl_data_rSBb = list(values[11:14])
            self.external_dvl_data_eulerbs = list(values[14:17])
            self.external_depth_rSBb = list(values[17:20])
            self.external_USBL_rSBb = list(values[20:23])
            self.reserved = list(values[23:62])
            
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode Aiding Source Config Packet 2 to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.enabled.pack(),
            *self.internal_depth_sensor_rSBb,
            *self.external_subsonus_rSBb,
            *self.external_subsonus_eulerbs,
            *self.external_dvl_data_rSBb,
            *self.external_dvl_data_eulerbs,
            *self.external_depth_rSBb,
            *self.external_USBL_rSBb,
            *self.reserved,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet