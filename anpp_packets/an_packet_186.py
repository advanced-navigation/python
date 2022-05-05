################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_186.py                              ##
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
from enum import Enum
from struct import pack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


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

    ID = PacketID.filter_options
    LENGTH = 17

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Filter Options Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.permanent = an_packet.data[0]
            self.vehicle_type = VehicleType(an_packet.data[1])
            self.internal_gnss_enabled = an_packet.data[2]
            self.magnetometers_enabled = an_packet.data[3]
            self.atmospheric_altitude_enabled = an_packet.data[4]
            self.velocity_heading_enabled = an_packet.data[5]
            self.reversing_detection_enabled = an_packet.data[6]
            self.motion_analysis_enabled = an_packet.data[7]
            self.automatic_magnetic_calibration_enabled = an_packet.data[8]
            return 0
        else:
            return 1

    def encode(self):
        """Encode Filter Options Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<BBBBBBBBBd', self.permanent, self.vehicle_type,
                    self.internal_gnss_enabled, self.magnetometers_enabled,
                    self.atmospheric_altitude_enabled, self.velocity_heading_enabled,
                    self.reversing_detection_enabled, self.motion_analysis_enabled,
                    self.automatic_magnetic_calibration_enabled, 0)

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
