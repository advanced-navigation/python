################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_31.py                              ##
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
from enum import Enum
from struct import unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


class SatelliteSystem(Enum):
    """Satellite System"""
    unknown = 0
    gps = 1
    glonass = 2
    beidou = 3
    galileo = 4
    sbas = 5
    qzss = 6
    starfire = 7
    omnistar = 8


@dataclass()
class SatelliteFrequencies:
    """Satellite Frequencies"""
    l1_ca: bool = False
    l1_c: bool = False
    l1_p: bool = False
    l1_m: bool = False
    l2_c: bool = False
    l2_p: bool = False
    l2_m: bool = False
    l5: bool = False

    def unpack(self, data):
        self.l1_ca = (data & (1 << 0)) != 0
        self.l1_c = (data & (1 << 1)) != 0
        self.l1_p = (data & (1 << 2)) != 0
        self.l1_m = (data & (1 << 3)) != 0
        self.l2_c = (data & (1 << 4)) != 0
        self.l2_p = (data & (1 << 5)) != 0
        self.l2_m = (data & (1 << 6)) != 0
        self.l5 = (data & (1 << 7)) != 0


@dataclass()
class DetailedSatellite:
    """Detailed Satellite"""
    satellite_system: SatelliteSystem = SatelliteSystem.unknown
    number: int = 0
    frequencies: SatelliteFrequencies = SatelliteFrequencies()
    elevation: int = 0
    azimuth: int = 0
    snr: int = 0

    LENGTH = 7

    def unpack(self, data):
        """Unpack data bytes"""
        self.satellite_system = SatelliteSystem(data[0])
        self.number = data[1]
        self.frequencies.unpack(data[2])
        self.elevation = data[3]
        self.azimuth = unpack('<H', data[4:6])[0]
        self.snr = data[6]


@dataclass()
class DetailedSatellitesPacket:
    """Packet 31 - Detailed Satellites Packet"""
    satellites: [DetailedSatellite] = field(default_factory=list)

    ID = PacketID.detailed_satellites
    MAXIMUM_DETAILED_SATELLITES = 32

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Detailed Satellites Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) \
                and ((len(an_packet.data) % DetailedSatellite.LENGTH) == 0):
            number_of_satellites = int(len(an_packet.data) / DetailedSatellite.LENGTH)
            self.satellites = [DetailedSatellite()] * number_of_satellites
            for i in range(number_of_satellites):
                index = i * DetailedSatellite.LENGTH
                self.satellites[i].unpack(an_packet.data[index:index+DetailedSatellite.LENGTH])
            return 0
        else:
            return 1
