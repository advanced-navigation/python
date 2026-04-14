################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_84.py                              ##
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
from .an_packet_31 import SatelliteFrequencies


@dataclass()
class ExtendedSatelliteFlags:
    """Extended Satellite Flags"""

    visible_by_receiver_1: bool = False
    visible_by_receiver_2: bool = False
    used_in_primary_position_solution: bool = False
    used_in_moving_baseline_solution: bool = False


@dataclass()
class ExtendedSatellite:
    """Extended Satellite"""

    satellite_system: int = 0
    number: int = 0
    frequencies: SatelliteFrequencies = field(
        default_factory=SatelliteFrequencies, repr=False
    )
    elevation: int = 0
    azimuth: int = 0
    snr1: int = 0
    snr2: int = 0
    flags: ExtendedSatelliteFlags = field(
        default_factory=ExtendedSatelliteFlags, repr=False
    )

    LENGTH = 9

    _structure = struct.Struct("<BBbBHBBB")

    def unpack(self, data):
        """Unpack data bytes"""
        (
            self.satellite_system,
            self.number,
            self.frequencies,
            self.elevation,
            self.azimuth,
            self.snr1,
            self.snr2,
            self.flags,
        ) = self._structure.unpack_from(data)


@dataclass()
class ExtendedSatellitesPacket:
    """Packet 84 - Extended Satellites Packet"""

    total_number_of_packets: int = 0
    packet_number: int = 0
    extended_satellites: List[ExtendedSatellite] = field(
        default_factory=list, repr=False
    )

    ID = PacketID.extended_satellites
    MINIMUM_LENGTH = 2
    MAXIMUM_EXTENDED_SATELLITES = 28

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Extended Satellites Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (
            ((len(an_packet.data) - self.MINIMUM_LENGTH) % ExtendedSatellite.LENGTH)
            == 0
        ):
            number_of_satellites = int(
                (len(an_packet.data) - self.MINIMUM_LENGTH) / ExtendedSatellite.LENGTH
            )
            self.total_number_of_packets = an_packet.data[0]
            self.packet_number = an_packet.data[1]
            self.extended_satellites = [ExtendedSatellite()] * number_of_satellites
            for i in range(number_of_satellites):
                index = self.MINIMUM_LENGTH + i * ExtendedSatellite.LENGTH
                self.extended_satellites[i].unpack(
                    an_packet.data[index : index + ExtendedSatellite.LENGTH]
                )
            return 0
        else:
            return 1
