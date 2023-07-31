################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_197.py                              ##
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
from enum import Enum
import struct
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


class LBandMode(Enum):
    """L Band Mode"""

    disabled = 0
    omnistar_auto = 2
    omnistar_hp = 3
    omnistar_xp = 4
    omnistar_vbs = 5
    omnistar_g2 = 8
    omnistar_hp_g2 = 9
    omnistar_hp_xp = 10
    trimble_rtx = 11
    omnistar_l1_only = 13
    omnistar_g4_only = 14
    omnistar_g2plus_only = 15
    omnistar_g4plus_only = 16


class LBandSatelliteID(Enum):
    """L Band Satellite ID"""

    unknown = 0
    iosat = 2
    aoret = 8
    rtxmx = 15
    amsat = 16
    wasat = 17
    ocsat = 18
    rtxal = 19
    rtxio = 20
    conna = 22
    rtxna = 23
    rtxpa = 27
    rtxea = 29
    emsat = 30
    custom = 100
    auto = 110


@dataclass()
class GNSSFrequencies:
    """GNSS Frequencies"""

    gps_l1ca: bool = False
    gps_l1c: bool = False
    gps_l1p: bool = False
    gps_l2c: bool = False
    gps_l2p: bool = False
    gps_l2m: bool = False
    gps_l5: bool = False
    glonass_g1ca: bool = False
    glonass_g1p: bool = False
    glonass_l1oc: bool = False
    glonass_l1sc: bool = False
    glonass_g2ca: bool = False
    glonass_g2p: bool = False
    glonass_l2oc: bool = False
    glonass_l2sc: bool = False
    glonass_l3oc: bool = False
    glonass_l3sc: bool = False
    beidou_b1: bool = False
    beidou_b2: bool = False
    beidou_b3: bool = False
    galileo_e1: bool = False
    galileo_e5a: bool = False
    galileo_e5b: bool = False
    galileo_e5ab: bool = False
    galileo_e6: bool = False
    qzss_l1ca: bool = False
    qzss_l1saif: bool = False
    qzss_l1c: bool = False
    qzss_l2c: bool = False
    qzss_l5: bool = False
    qzss_lex: bool = False
    sbas_l1ca: bool = False

    def unpack(self, data):
        self.gps_l1ca = (data & (1 << 0)) != 0
        self.gps_l1c = (data & (1 << 1)) != 0
        self.gps_l1p = (data & (1 << 2)) != 0
        self.gps_l2c = (data & (1 << 3)) != 0
        self.gps_l2p = (data & (1 << 4)) != 0
        self.gps_l2m = (data & (1 << 5)) != 0
        self.gps_l5 = (data & (1 << 6)) != 0
        self.glonass_g1ca = (data & (1 << 7)) != 0
        self.glonass_g1p = (data & (1 << 8)) != 0
        self.glonass_l1oc = (data & (1 << 9)) != 0
        self.glonass_l1sc = (data & (1 << 10)) != 0
        self.glonass_g2ca = (data & (1 << 11)) != 0
        self.glonass_g2p = (data & (1 << 12)) != 0
        self.glonass_l2oc = (data & (1 << 13)) != 0
        self.glonass_l2sc = (data & (1 << 14)) != 0
        self.glonass_l3oc = (data & (1 << 15)) != 0
        self.glonass_l3sc = (data & (1 << 16)) != 0
        self.beidou_b1 = (data & (1 << 17)) != 0
        self.beidou_b2 = (data & (1 << 18)) != 0
        self.beidou_b3 = (data & (1 << 19)) != 0
        self.galileo_e1 = (data & (1 << 20)) != 0
        self.galileo_e5a = (data & (1 << 21)) != 0
        self.galileo_e5b = (data & (1 << 22)) != 0
        self.galileo_e5ab = (data & (1 << 23)) != 0
        self.galileo_e6 = (data & (1 << 24)) != 0
        self.qzss_l1ca = (data & (1 << 25)) != 0
        self.qzss_l1saif = (data & (1 << 26)) != 0
        self.qzss_l1c = (data & (1 << 27)) != 0
        self.qzss_l2c = (data & (1 << 28)) != 0
        self.qzss_l5 = (data & (1 << 29)) != 0
        self.qzss_lex = (data & (1 << 30)) != 0
        self.sbas_l1ca = (data & (1 << 31)) != 0

    def pack(self):
        return (
            (self.gps_l1ca << 0)
            & (self.gps_l1c << 1)
            & (self.gps_l1p << 2)
            & (self.gps_l2c << 3)
            & (self.gps_l2p << 4)
            & (self.gps_l2m << 5)
            & (self.gps_l5 << 6)
            & (self.glonass_g1ca << 7)
            & (self.glonass_g1p << 8)
            & (self.glonass_l1oc << 9)
            & (self.glonass_l1sc << 10)
            & (self.glonass_g2ca << 11)
            & (self.glonass_g2p << 12)
            & (self.glonass_l2oc << 13)
            & (self.glonass_l2sc << 14)
            & (self.glonass_l3oc << 15)
            & (self.glonass_l3sc << 16)
            & (self.beidou_b1 << 17)
            & (self.beidou_b2 << 18)
            & (self.beidou_b3 << 19)
            & (self.galileo_e1 << 20)
            & (self.galileo_e5a << 21)
            & (self.galileo_e5b << 22)
            & (self.galileo_e5ab << 23)
            & (self.galileo_e6 << 24)
            & (self.qzss_l1ca << 25)
            & (self.qzss_l1saif << 26)
            & (self.qzss_l1c << 27)
            & (self.qzss_l2c << 28)
            & (self.qzss_l5 << 29)
            & (self.qzss_lex << 30)
            & (self.sbas_l1ca << 31)
        )


@dataclass()
class GNSSConfigurationPacket:
    """Packet 197 - GNSS Configuration Packet"""

    permanent: int = 0
    gnss_frequencies: GNSSFrequencies = field(
        default_factory=GNSSFrequencies, repr=False
    )
    pdop: float = 0
    tfop: float = 0
    elevation_mask: int = 0
    snr_mask: int = 0
    sbas_corrections_enabled: int = 0
    lband_mode: LBandMode = LBandMode.disabled
    lband_frequency: int = 0
    lband_baud: int = 0
    primary_antenna_type: int = 0
    secondary_antenna_type: int = 0
    lband_satellite_id: LBandSatelliteID = LBandSatelliteID.auto

    ID = PacketID.gnss_configuration
    LENGTH = 85

    _structure_aries = struct.Struct("<BQ76x")
    _structure_trimble = struct.Struct("<BQffBBBBIIIIB47x")

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to GNSS Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.permanent,
                gnss_frequencies_value,
                self.pdop,
                self.tfop,
                self.elevation_mask,
                self.snr_mask,
                self.sbas_corrections_enabled,
                lband_mode_value,
                self.lband_frequency,
                self.lband_baud,
                self.primary_antenna_type,
                self.secondary_antenna_type,
                lband_satellite_id_value,
            ) = self._structure_trimble.unpack_from(an_packet.data)

            self.gnss_frequencies.unpack(gnss_frequencies_value)
            self.lband_mode = LBandMode(lband_mode_value)
            self.lband_satellite_id = LBandSatelliteID(lband_satellite_id_value)
            return 0
        return 1

    def encode(self):
        """Encode GNSS Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure_trimble.pack(
            self.permanent,
            self.gnss_frequencies.pack(),
            self.pdop,
            self.tfop,
            self.elevation_mask,
            self.snr_mask,
            self.sbas_corrections_enabled,
            self.lband_mode.value,
            self.lband_frequency,
            self.lband_baud,
            self.primary_antenna_type,
            self.secondary_antenna_type,
            self.lband_satellite_id.value,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
