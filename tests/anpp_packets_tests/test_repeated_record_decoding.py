################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                    test_repeated_record_decoding.py                        ##
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

import struct

import pytest

from advanced_navigation.anpp_packets.an_packet_31 import (
    DetailedSatellitesPacket,
    SatelliteFrequencies,
)
from advanced_navigation.anpp_packets.an_packet_41 import DCMOrientationPacket
from advanced_navigation.anpp_packets.an_packet_60 import RawSatelliteDataPacket
from advanced_navigation.anpp_packets.an_packet_84 import (
    ExtendedSatelliteFlags,
    ExtendedSatellitesPacket,
)
from advanced_navigation.anpp_packets.an_packet_181 import PacketsPeriodPacket
from advanced_navigation.anpp_packets.an_packet_185 import InstallationAlignmentPacket
from advanced_navigation.anpp_packets.an_packet_189 import (
    MagneticCalibrationValuesPacket,
)
from advanced_navigation.anpp_packets.an_packet_202 import (
    IPDataportConfigurationPacket,
)
from advanced_navigation.anpp_packets.an_packet_protocol import ANPacket

DETAILED_SATELLITE = struct.Struct("<BBBBHB")
FREQUENCY_INFORMATION = struct.Struct("<BBddff")
SATELLITE_DATA = struct.Struct("<BBBHB")
RAW_SATELLITE_DATA_HEADER = struct.Struct("<IIiBBBB")
EXTENDED_SATELLITE = struct.Struct("<BBBBHBBB")
PACKET_PERIOD = struct.Struct("<BI")
IP_DATAPORT_CONFIGURATION = struct.Struct("<IHB")


def make_packet(packet_id, data):
    return ANPacket(id=packet_id, length=len(data), data=data)


@pytest.mark.parametrize(
    ("packet_type", "data", "records_attribute", "value_attribute", "expected"),
    [
        (
            DetailedSatellitesPacket,
            DETAILED_SATELLITE.pack(1, 11, 1, 10, 100, 31)
            + DETAILED_SATELLITE.pack(4, 22, 2, 20, 200, 42),
            "satellites",
            "number",
            [11, 22],
        ),
        (
            ExtendedSatellitesPacket,
            bytes([1, 0])
            + EXTENDED_SATELLITE.pack(1, 11, 1, 10, 100, 31, 32, 1)
            + EXTENDED_SATELLITE.pack(4, 22, 2, 20, 200, 41, 42, 2),
            "extended_satellites",
            "number",
            [11, 22],
        ),
        (
            PacketsPeriodPacket,
            bytes([1, 0]) + PACKET_PERIOD.pack(31, 100) + PACKET_PERIOD.pack(84, 200),
            "packet_periods",
            "packet_id",
            [31, 84],
        ),
        (
            IPDataportConfigurationPacket,
            bytes(2)
            + b"".join(
                IP_DATAPORT_CONFIGURATION.pack(0, port, 2)
                for port in [16718, 16719, 16720, 16721]
            ),
            "ip_dataport_configuration",
            "port",
            [16718, 16719, 16720, 16721],
        ),
    ],
    ids=["packet-31", "packet-84", "packet-181", "packet-202"],
)
def test_decodes_distinct_repeated_records(
    packet_type, data, records_attribute, value_attribute, expected
):
    packet = packet_type()

    assert packet.decode(make_packet(packet.ID, data)) == 0

    records = getattr(packet, records_attribute)
    assert [getattr(record, value_attribute) for record in records] == expected


def test_packet_84_decodes_nested_frequency_and_flag_fields():
    data = bytes([1, 0]) + EXTENDED_SATELLITE.pack(1, 11, 0b10000001, 10, 100, 31, 32, 0b0101)
    packet = ExtendedSatellitesPacket()

    assert packet.decode(make_packet(packet.ID, data)) == 0

    satellite = packet.extended_satellites[0]
    assert isinstance(satellite.frequencies, SatelliteFrequencies)
    assert satellite.frequencies.l1_ca is True
    assert satellite.frequencies.l1_c is False
    assert satellite.frequencies.l5 is True
    assert isinstance(satellite.flags, ExtendedSatelliteFlags)
    assert satellite.flags.visible_by_receiver_1 is True
    assert satellite.flags.visible_by_receiver_2 is False
    assert satellite.flags.used_in_primary_position_solution is True
    assert satellite.flags.used_in_moving_baseline_solution is False


@pytest.mark.parametrize(
    ("packet_type", "matrix_attribute"),
    [
        (DCMOrientationPacket, "orientation"),
        (InstallationAlignmentPacket, "alignment_dcm"),
        (MagneticCalibrationValuesPacket, "soft_iron"),
    ],
    ids=["packet-41", "packet-185", "packet-189"],
)
def test_matrix_default_factory_uses_independent_rows(packet_type, matrix_attribute):
    matrix = getattr(packet_type(), matrix_attribute)
    matrix[0][0] = 1.0
    assert matrix[1][0] == 0.0
    assert matrix[2][0] == 0.0


def pack_frequency(frequency):
    return FREQUENCY_INFORMATION.pack(frequency, 0, float(frequency), 0, 0, 0)


def pack_satellite(system, number, frequencies):
    return SATELLITE_DATA.pack(system, number, 0, 0, len(frequencies)) + b"".join(
        pack_frequency(frequency) for frequency in frequencies
    )


def test_packet_60_uses_cumulative_frequency_offsets():
    frequencies = [[1, 5], [3], [8, 9]]
    data = RAW_SATELLITE_DATA_HEADER.pack(0, 0, 0, 1, 1, 1, 3) + b"".join(
        pack_satellite(system, number, satellite_frequencies)
        for system, number, satellite_frequencies in [
            (1, 11, frequencies[0]),
            (2, 22, frequencies[1]),
            (4, 33, frequencies[2]),
        ]
    )
    packet = RawSatelliteDataPacket()

    assert packet.decode(make_packet(packet.ID, data)) == 0

    assert [satellite.prn_satellite_number for satellite in packet.satellite_data] == [
        11,
        22,
        33,
    ]
    assert [
        [record.satellite_frequency for record in satellite.frequency_information]
        for satellite in packet.satellite_data
    ] == frequencies
