################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_207.py                              ##
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
class AidingSourceConfig1Enabled:
    """Aiding Source Config 1 Enabled Bitmask"""
    internal_gnss_pvt: bool = False
    internal_gnss_orientation: bool = False
    internal_magnetometers: bool = False
    internal_pressure: bool = False
    external_gnss_pvt: bool = False
    external_gnss_orientation: bool = False
    external_position: bool = False
    external_odometer: bool = False
    external_heading: bool = False
    external_pressure: bool = False
    external_velocity: bool = False
    external_position_velocity: bool = False
    external_body_velocity: bool = False
    external_air_data: bool = False
    external_magnetometers: bool = False
    external_lvs: bool = False

    def unpack(self, data: int):
        """Unpack data bytes"""
        self.internal_gnss_pvt = (data & (1 << 0)) != 0
        self.internal_gnss_orientation = (data & (1 << 1)) != 0
        self.internal_magnetometers = (data & (1 << 2)) != 0
        self.internal_pressure = (data & (1 << 3)) != 0
        self.external_gnss_pvt = (data & (1 << 4)) != 0
        self.external_gnss_orientation = (data & (1 << 5)) != 0
        self.external_position = (data & (1 << 6)) != 0
        self.external_odometer = (data & (1 << 7)) != 0
        self.external_heading = (data & (1 << 8)) != 0
        self.external_pressure = (data & (1 << 9)) != 0
        self.external_velocity = (data & (1 << 10)) != 0
        self.external_position_velocity = (data & (1 << 11)) != 0
        self.external_body_velocity = (data & (1 << 12)) != 0
        self.external_air_data = (data & (1 << 13)) != 0
        self.external_magnetometers = (data & (1 << 14)) != 0
        self.external_lvs = (data & (1 << 15)) != 0

    def pack(self) -> int:
        """Pack data bytes"""
        data = self.internal_gnss_pvt << 0
        data |= self.internal_gnss_orientation << 1
        data |= self.internal_magnetometers << 2
        data |= self.internal_pressure << 3
        data |= self.external_gnss_pvt << 4
        data |= self.external_gnss_orientation << 5
        data |= self.external_position << 6
        data |= self.external_odometer << 7
        data |= self.external_heading << 8
        data |= self.external_pressure << 9
        data |= self.external_velocity << 10
        data |= self.external_position_velocity << 11
        data |= self.external_body_velocity << 12
        data |= self.external_air_data << 13
        data |= self.external_magnetometers << 14
        data |= self.external_lvs << 15
        return data


@dataclass()
class AidingSourceConfigPacket1:
    """Packet 207 - Aiding Source Config Packet 1"""
    permanent: int = 0
    enabled: AidingSourceConfig1Enabled = field(default_factory=AidingSourceConfig1Enabled, repr=False)
    
    internal_gnss_pvt_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    internal_gnss_orientation_rPSb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_gnss_pvt_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_gnss_orientation_rPSb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_position_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_odometer_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_heading_eulerbs: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_pressure_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_velocity_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_position_velocity_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_body_velocity_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_body_velocity_eulerbs: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_air_data_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_air_data_eulerbs: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_magnetometers_eulerbs: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_lvs_rSBb: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    external_lvs_eulerbs: List[float] = field(default_factory=lambda: [0.0]*3, repr=False)
    reserved: List[float] = field(default_factory=lambda: [0.0]*9, repr=False)

    ID = PacketID.aiding_source_config_1
    LENGTH = 243

    # <    : Little-endian
    # B    : 1 uint8 (permanent)
    # H    : 1 uint16 (enabled bitmask)
    # 60f  : 60 floats (17 arrays of 3 + 9 reserved = 60 floats = 240 bytes)
    _structure = struct.Struct("<BH60f")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Aiding Source Config Packet 1
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            
            self.permanent = values[0]
            self.enabled.unpack(values[1])
            
            self.internal_gnss_pvt_rSBb = list(values[2:5])
            self.internal_gnss_orientation_rPSb = list(values[5:8])
            self.external_gnss_pvt_rSBb = list(values[8:11])
            self.external_gnss_orientation_rPSb = list(values[11:14])
            self.external_position_rSBb = list(values[14:17])
            self.external_odometer_rSBb = list(values[17:20])
            self.external_heading_eulerbs = list(values[20:23])
            self.external_pressure_rSBb = list(values[23:26])
            self.external_velocity_rSBb = list(values[26:29])
            self.external_position_velocity_rSBb = list(values[29:32])
            self.external_body_velocity_rSBb = list(values[32:35])
            self.external_body_velocity_eulerbs = list(values[35:38])
            self.external_air_data_rSBb = list(values[38:41])
            self.external_air_data_eulerbs = list(values[41:44])
            self.external_magnetometers_eulerbs = list(values[44:47])
            self.external_lvs_rSBb = list(values[47:50])
            self.external_lvs_eulerbs = list(values[50:53])
            self.reserved = list(values[53:62])
            
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode Aiding Source Config Packet 1 to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.enabled.pack(),
            *self.internal_gnss_pvt_rSBb,
            *self.internal_gnss_orientation_rPSb,
            *self.external_gnss_pvt_rSBb,
            *self.external_gnss_orientation_rPSb,
            *self.external_position_rSBb,
            *self.external_odometer_rSBb,
            *self.external_heading_eulerbs,
            *self.external_pressure_rSBb,
            *self.external_velocity_rSBb,
            *self.external_position_velocity_rSBb,
            *self.external_body_velocity_rSBb,
            *self.external_body_velocity_eulerbs,
            *self.external_air_data_rSBb,
            *self.external_air_data_eulerbs,
            *self.external_magnetometers_eulerbs,
            *self.external_lvs_rSBb,
            *self.external_lvs_eulerbs,
            *self.reserved,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet