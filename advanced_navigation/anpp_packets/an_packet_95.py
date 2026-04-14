################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_95.py                               ##
##                     Copyright 2023, Advanced Navigation                    ##
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
class AidingSourceStatus:
    """Aiding Source Status Flags"""
    online: bool = False
    valid: bool = False
    origin: int = 0

    def unpack(self, data: int):
        """Unpack data bytes"""
        self.online = (data & (1 << 0)) != 0
        self.valid = (data & (1 << 1)) != 0
        # Bits 2-9 are reserved.
        # Bits 10-15 define the origin (6 bits wide). Shift right by 10, mask with 0x3F (00111111).
        self.origin = (data >> 10) & 0x3F


@dataclass()
class AidingSourceStatusPacket:
    """Packet 95 - Aiding Source Status Packet"""
    gnss_pvt: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    gnss_orientation: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    internal_magnetometers: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    pressure: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_gnss_pvt: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_gnss_orientation: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_position: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_odometer: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_heading: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_pressure: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_velocity: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_position_velocity: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_body_velocity: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_air_data: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_magnetometers: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_lvs: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    depth_sensor: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    subsonus: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    dvl_data: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_depth: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_usbl: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    external_svs_data: AidingSourceStatus = field(default_factory=AidingSourceStatus, repr=False)
    reserved: List[int] = field(default_factory=lambda: [0] * 10, repr=False)

    ID = PacketID.filter_aiding_source_status
    LENGTH = 64

    # <     : Little-endian
    # 32H   : 32 unsigned shorts (22 status instances + 10 reserved = 32 * 2 bytes = 64 bytes total)
    _structure = struct.Struct("<32H")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Aiding Source Status Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            
            self.gnss_pvt.unpack(values[0])
            self.gnss_orientation.unpack(values[1])
            self.internal_magnetometers.unpack(values[2])
            self.pressure.unpack(values[3])
            self.external_gnss_pvt.unpack(values[4])
            self.external_gnss_orientation.unpack(values[5])
            self.external_position.unpack(values[6])
            self.external_odometer.unpack(values[7])
            self.external_heading.unpack(values[8])
            self.external_pressure.unpack(values[9])
            self.external_velocity.unpack(values[10])
            self.external_position_velocity.unpack(values[11])
            self.external_body_velocity.unpack(values[12])
            self.external_air_data.unpack(values[13])
            self.external_magnetometers.unpack(values[14])
            self.external_lvs.unpack(values[15])
            self.depth_sensor.unpack(values[16])
            self.subsonus.unpack(values[17])
            self.dvl_data.unpack(values[18])
            self.external_depth.unpack(values[19])
            self.external_usbl.unpack(values[20])
            self.external_svs_data.unpack(values[21])
            
            self.reserved = list(values[22:32])
            
            return 0
        else:
            return 1