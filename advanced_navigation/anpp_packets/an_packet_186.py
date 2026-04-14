################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_186.py                              ##
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

from dataclasses import dataclass
from enum import Enum
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


class VehicleType(Enum):
    """Vehicle Type"""

    unconstrained = 0
    bicycle = 1
    car = 2
    hovercraft = 3
    submarine = 4
    underwater_3d = 5
    fixed_wing_plane = 6
    aircraft_3d = 7
    human = 8
    boat = 9
    large_ship = 10
    stationary = 11
    stunt_plane = 12
    race_car = 13


@dataclass()
class FilterOptionsPacket:
    """Packet 186 - Filter Options Packet"""

    permanent: int = 0
    vehicle_type: VehicleType = VehicleType.unconstrained
    internal_gnss_enabled: int = 0
    magnetometers_enabled: int = 0
    atmospheric_altitude_enabled: int = 0
    velocity_heading_enabled: int = 0
    reversing_detection_enabled: int = 0
    motion_analysis_enabled: int = 0
    automatic_magnetic_calibration_enabled: int = 0
    dual_antenna_disabled: int = 0

    ID = PacketID.filter_options
    LENGTH = 17

    _structure = struct.Struct("<10B7x")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Filter Options Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.permanent,
                vehicle_type_value,
                self.internal_gnss_enabled,
                self.magnetometers_enabled,
                self.atmospheric_altitude_enabled,
                self.velocity_heading_enabled,
                self.reversing_detection_enabled,
                self.motion_analysis_enabled,
                self.automatic_magnetic_calibration_enabled,
                self.dual_antenna_disabled
            ) = self._structure.unpack_from(an_packet.data)
            self.vehicle_type = VehicleType(vehicle_type_value)
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode Filter Options Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.vehicle_type.value,
            self.internal_gnss_enabled,
            self.magnetometers_enabled,
            self.atmospheric_altitude_enabled,
            self.velocity_heading_enabled,
            self.reversing_detection_enabled,
            self.motion_analysis_enabled,
            self.automatic_magnetic_calibration_enabled,
            self.dual_antenna_disabled
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
