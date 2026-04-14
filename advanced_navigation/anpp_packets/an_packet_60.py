################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_60.py                              ##
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
from typing import List
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket
from .an_packet_31 import SatelliteSystem


@dataclass()
class TrackingStatus:
    """Tracking Status"""

    carrier_phase_valid: bool = False
    carrier_phase_cycle_slip_detected: bool = False
    carrier_phase_half_cycle_ambiguity: bool = False
    pseudo_range_valid: bool = False
    doppler_valid: bool = False
    snr_valid: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.carrier_phase_valid = (data & (1 << 0)) != 0
        self.carrier_phase_cycle_slip_detected = (data & (1 << 1)) != 0
        self.carrier_phase_half_cycle_ambiguity = (data & (1 << 2)) != 0
        self.pseudo_range_valid = (data & (1 << 3)) != 0
        self.doppler_valid = (data & (1 << 4)) != 0
        self.snr_valid = (data & (1 << 5)) != 0


class GPSSatelliteFrequency(Enum):
    """GPS Satellite Frequency"""

    unknown = 0
    l1_ca = 1
    l1_c = 2
    l1_p = 3
    l1_m = 4
    l2_c = 5
    l2_p = 6
    l2_m = 7
    l5 = 8


class GLONASSSatelliteFrequency(Enum):
    """GLONASS Satellite Frequency"""

    unknown = 0
    g1_ca = 1
    g1_p = 3
    g2_ca = 5
    g2_p = 6
    g3 = 8


class GalileoSatelliteFrequency(Enum):
    """Galileo Satellite Frequency"""

    unknown = 0
    e1_os = 1
    e1_prs = 2
    e6_c2 = 5
    e6_prs = 6
    e5_a = 8
    e5_b = 9
    e5_ab = 10


class BeiDouSatelliteFrequency(Enum):
    """BeiDou Satellite Frequency"""

    unknown = 0
    b1 = 1
    b2 = 5
    b3 = 8


class SBASSatelliteFrequency(Enum):
    """SBAS Satellite Frequency"""

    unknown = 0
    l1_ca = 1
    l5 = 8


class QZSSSatelliteFrequency(Enum):
    """QZSS Satellite Frequency"""

    unknown = 0
    l1_ca = 1
    l1_c = 2
    l1_saif = 3
    l2_c = 5
    lex = 6
    l5 = 8


@dataclass()
class FrequencyInformation:
    """Frequency Information"""

    satellite_frequency: int = GPSSatelliteFrequency.unknown.value
    tracking_status: TrackingStatus = field(default_factory=TrackingStatus, repr=False)
    carrier_phase: float = 0
    pseudo_range: float = 0
    doppler_frequency: float = 0
    snr: float = 0

    LENGTH = 26

    _structure = struct.Struct("<BBddff")

    def unpack(self, data):
        """Unpack data bytes"""
        (
            self.satellite_frequency,
            tracking_status_value,
            self.carrier_phase,
            self.pseudo_range,
            self.doppler_frequency,
            self.snr,
        ) = self._structure.unpack_from(data)

        self.tracking_status.unpack(tracking_status_value)


@dataclass()
class SatelliteData:
    """Satellite Data"""

    satellite_system: SatelliteSystem = SatelliteSystem.unknown
    prn_satellite_number: int = 0
    elevation: int = 0
    azimuth: int = 0
    number_of_frequencies: int = 0
    frequency_information: List[FrequencyInformation] = field(
        default_factory=list, repr=False
    )

    MINIMUM_LENGTH = 6

    _structure = struct.Struct("<BBBHB")

    def unpack(self, data):
        """Unpack data bytes"""
        (
            satellite_system_value,
            self.prn_satellite_number,
            self.elevation,
            self.azimuth,
            self.number_of_frequencies,
        ) = self._structure.unpack_from(data)

        self.satellite_system = SatelliteSystem(satellite_system_value)

        self.frequency_information = [
            FrequencyInformation()
        ] * self.number_of_frequencies
        for i in range(self.number_of_frequencies):
            index = 6 + i * FrequencyInformation.LENGTH
            self.frequency_information[i].unpack(
                data[index : index + FrequencyInformation.LENGTH]
            )


@dataclass()
class RawSatelliteDataPacket:
    """Packet 60 - Raw Satellite Data Packet"""

    unix_time: int = 0
    nanoseconds: int = 0
    receiver_clock_offset: int = 0
    receiver_number: int = 0
    packet_number: int = 0
    total_packets: int = 0
    number_of_satellites: int = 0
    satellite_data: List[SatelliteData] = field(default_factory=list, repr=False)

    ID = PacketID.raw_satellite_data

    HEAD_LENGTH = 16

    _structure = struct.Struct("<IIiBBBB")

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Raw Satellite Data Packet
        Returns 0 on success and 1 on failure"""
        if an_packet.id == self.ID:
            (
                self.unix_time,
                self.nanoseconds,
                self.receiver_clock_offset,
                self.receiver_number,
                self.packet_number,
                self.total_packets,
                self.number_of_satellites,
            ) = self._structure.unpack_from(an_packet.data)

            self.satellite_data = [SatelliteData()] * self.number_of_satellites

            number_of_previous_frequencies = 0
            for i in range(self.number_of_satellites):
                index = (
                    self.HEAD_LENGTH
                    + i * SatelliteData.MINIMUM_LENGTH
                    + number_of_previous_frequencies * FrequencyInformation.LENGTH
                )
                self.satellite_data[i].unpack(an_packet.data[index:])
                number_of_previous_frequencies = self.satellite_data[
                    i
                ].number_of_frequencies
            return 0
        else:
            return 1
