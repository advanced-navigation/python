################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_61.py                              ##
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
from .an_packet_31 import SatelliteSystem


@dataclass()
class GPSFlags:
    """GPS Flags"""

    l2p_data: bool = False
    l2_codes: int = 0
    anti_spoofing: bool = False
    satellite_health: int = 0
    fit_interval: bool = False
    ura_bad: bool = False
    satellite_type: int = 0

    def unpack(self, data):
        """Unpack data bytes"""
        self.l2p_data = (data & (1 << 0)) != 0
        self.l2_codes = (data >> 1) & 0x0003
        self.anti_spoofing = (data & (1 << 3)) != 0
        self.satellite_health = (data >> 4) & 0x003F
        self.fit_interval = (data & (1 << 10)) != 0
        self.ura_bad = (data & (1 << 11)) != 0
        self.satellite_type = (data >> 12) & 0x0003


@dataclass()
class RawSatelliteGPSEphemerisPacket:
    """Packet 61 - Raw Satellite Ephemeris Packet (GPS)"""

    unix_time: int = 0
    satellite_system: SatelliteSystem = SatelliteSystem.unknown
    satellite_number: int = 0
    time_of_ephemeris: int = 0
    issue_of_data_clock: int = 0
    issue_of_data_ephemeris: int = 0
    satellite_clock_bias: float = 0
    satellite_clock_drift: float = 0
    satellite_clock_drift_rate: float = 0
    crs: float = 0
    delta_n: float = 0
    m0: float = 0
    cuc: float = 0
    eccentricity: float = 0
    cus: float = 0
    sqrtA: float = 0
    cic: float = 0
    omega0: float = 0
    cis: float = 0
    i0: float = 0
    crc: float = 0
    omega: float = 0
    omega_dot: float = 0
    idot: float = 0
    tgd: float = 0
    ephemeris_week_number: int = 0
    transmission_time: int = 0
    user_range_accuracy: int = 0
    flags: GPSFlags = field(default_factory=GPSFlags, repr=False)

    LENGTH = 132

    _structure = struct.Struct("<IBBIHHfffffdfdfdfdfdfdddfHIHH")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Raw Satellite Ephemeris Packet (GPS)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == RawSatelliteEphemerisPacket.ID) and (
            len(an_packet.data) == self.LENGTH
        ):
            (
                self.unix_time,
                satellite_system_value,
                self.satellite_number,
                self.time_of_ephemeris,
                self.issue_of_data_clock,
                self.issue_of_data_ephemeris,
                self.satellite_clock_bias,
                self.satellite_clock_drift,
                self.satellite_clock_drift_rate,
                self.crs,
                self.delta_n,
                self.m0,
                self.cuc,
                self.eccentricity,
                self.cus,
                self.sqrtA,
                self.cic,
                self.omega0,
                self.cis,
                self.i0,
                self.crc,
                self.omega,
                self.omega_dot,
                self.idot,
                self.tgd,
                self.ephemeris_week_number,
                self.transmission_time,
                self.user_range_accuracy,
                flags_value,
            ) = self._structure.unpack_from(an_packet.data)

            self.flags.unpack(flags_value)
            self.satellite_system = SatelliteSystem(satellite_system_value)
            return 0
        else:
            return 1


@dataclass()
class RawSatelliteGLONASSEphemerisPacket:
    """Packet 61 - Raw Satellite Ephemeris Packet (GLONASS)"""

    unix_time: int = 0
    satellite_system: SatelliteSystem = SatelliteSystem.unknown
    satellite_number: int = 0
    clock_bias: float = 0
    frequency_bias: float = 0
    position: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    velocity: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    acceleration: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    frame_start_time: int = 0
    age: int = 0
    frequency_slot: int = 0
    satellite_health: int = 0

    LENGTH = 94

    _structure = struct.Struct("<IBBffdddddddddIBbBx")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Raw Satellite Ephemeris Packet (GLONASS)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == RawSatelliteEphemerisPacket.ID) and (
            len(an_packet.data) == self.LENGTH
        ):
            values = self._structure.unpack_from(an_packet.data)
            (
                self.unix_time,
                self.satellite_system,
                self.satellite_number,
                self.clock_bias,
                self.frequency_bias,
                *self.position,
            ) = values[:8]

            self.velocity = list(values[8:11])

            (
                *self.acceleration,
                self.frame_start_time,
                self.age,
                self.frequency_slot,
                self.satellite_health,
            ) = values[11:18]
            return 0
        else:
            return 1


@dataclass()
class RawSatelliteGPSIonoEphemerisPacket:
    """Packet 61 - Raw Satellite Ephemeris Packet (GPS Ionosphere)"""

    unix_time: int = 0
    satellite_system: SatelliteSystem = SatelliteSystem.unknown
    satellite_number: int = 0
    alpha: List[float] = field(default_factory=lambda: [0, 0, 0, 0], repr=False)
    beta: List[float] = field(default_factory=lambda: [0, 0, 0, 0], repr=False)
    asub: List[float] = field(default_factory=lambda: [0, 0], repr=False)
    delta_ls: int = 0
    delta_tlsf: int = 0
    wnsub_lsf: int = 0
    dn: int = 0

    LENGTH = 92

    _structure = struct.Struct("<IBBddddddddddHHBBx")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Raw Satellite Ephemeris Packet (GPS Ionosphere)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == RawSatelliteEphemerisPacket.ID) and (
            len(an_packet.data) == self.LENGTH
        ):
            values = self._structure.unpack_from(an_packet.data)

            (
                self.unix_time,
                satellite_system_value,
                self.satellite_number,
                *self.alpha,
            ) = values[0:7]

            self.satellite_system = SatelliteSystem(satellite_system_value)
            self.beta = list(values[7:11])

            (
                *self.asub,
                self.delta_ls,
                self.delta_tlsf,
                self.wnsub_lsf,
                self.dn,
            ) = values[11:17]
            return 0
        else:
            return 1


@dataclass()
class RawSatelliteEphemerisPacket:
    """Packet 61 - Raw Satellite Ephemeris Packet"""

    gps: RawSatelliteGPSEphemerisPacket = field(
        default_factory=RawSatelliteGPSEphemerisPacket, repr=False
    )
    glonass: RawSatelliteGLONASSEphemerisPacket = field(
        default_factory=RawSatelliteGLONASSEphemerisPacket, repr=False
    )
    gps_iono: RawSatelliteGPSIonoEphemerisPacket = field(
        default_factory=RawSatelliteGPSIonoEphemerisPacket, repr=False
    )

    ID = PacketID.raw_satellite_ephemeris

    def decode(self, an_packet: ANPacket) -> int:
        if an_packet.id == self.ID:
            match len(an_packet.data):
                case RawSatelliteGPSEphemerisPacket.LENGTH:
                    self.gps.decode(an_packet)
                    return 0
                case RawSatelliteGLONASSEphemerisPacket.LENGTH:
                    self.glonass.decode(an_packet)
                    return 0
                case RawSatelliteGPSIonoEphemerisPacket.LENGTH:
                    self.gps_iono.decode(an_packet)
                    return 0
                case _:
                    return 1
        return 1
