################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_61.py                              ##
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
from struct import unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket
from anpp_packets.an_packet_31 import SatelliteSystem


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
    flags: GPSFlags = GPSFlags()

    LENGTH = 132

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Raw Satellite Ephemeris Packet (GPS)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == RawSatelliteEphemerisPacket.ID) and (len(an_packet.data) == self.LENGTH):
            self.unix_time = unpack('<I', bytes(an_packet.data[0:4]))[0]
            self.satellite_system = SatelliteSystem(unpack('<B', bytes(an_packet.data[4]))[0])
            self.satellite_number = unpack('<B', bytes(an_packet.data[5]))[0]
            self.time_of_ephemeris = unpack('<I', bytes(an_packet.data[6:10]))[0]
            self.issue_of_data_clock = unpack('<H', bytes(an_packet.data[10:12]))[0]
            self.issue_of_data_ephemeris = unpack('<H', bytes(an_packet.data[12:14]))[0]
            self.satellite_clock_bias = unpack('<f', bytes(an_packet.data[14:18]))[0]
            self.satellite_clock_drift = unpack('<f', bytes(an_packet.data[18:22]))[0]
            self.satellite_clock_drift_rate = unpack('<f', bytes(an_packet.data[22:26]))[0]
            self.crs = unpack('<f', bytes(an_packet.data[26:30]))[0]
            self.delta_n = unpack('<f', bytes(an_packet.data[30:34]))[0]
            self.m0 = unpack('<d', bytes(an_packet.data[34:42]))[0]
            self.cuc = unpack('<f', bytes(an_packet.data[42:46]))[0]
            self.eccentricity = unpack('<d', bytes(an_packet.data[46:54]))[0]
            self.cus = unpack('<f', bytes(an_packet.data[54:58]))[0]
            self.sqrtA = unpack('<d', bytes(an_packet.data[58:66]))[0]
            self.cic = unpack('<f', bytes(an_packet.data[66:70]))[0]
            self.omega0 = unpack('<d', bytes(an_packet.data[70:78]))[0]
            self.cis = unpack('<f', bytes(an_packet.data[78:82]))[0]
            self.i0 = unpack('<d', bytes(an_packet.data[82:90]))[0]
            self.crc = unpack('<f', bytes(an_packet.data[90:94]))[0]
            self.omega = unpack('<d', bytes(an_packet.data[94:102]))[0]
            self.omega_dot = unpack('<d', bytes(an_packet.data[102:110]))[0]
            self.idot = unpack('<d', bytes(an_packet.data[110:118]))[0]
            self.tgd = unpack('<f', bytes(an_packet.data[118:122]))[0]
            self.ephemeris_week_number = unpack('<H', bytes(an_packet.data[122:124]))[0]
            self.transmission_time = unpack('<I', bytes(an_packet.data[124:128]))[0]
            self.user_range_accuracy = unpack('<H', bytes(an_packet.data[128:130]))[0]
            self.flags.unpack(unpack('<H', bytes(an_packet.data[130:132]))[0])
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
    position: [float] * 3 = field(default_factory=list)
    velocity: [float] * 3 = field(default_factory=list)
    acceleration: [float] * 3 = field(default_factory=list)
    frame_start_time: int = 0
    age: int = 0
    frequency_slot: int = 0
    satellite_health: int = 0

    LENGTH = 94

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Raw Satellite Ephemeris Packet (GLONASS)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == RawSatelliteEphemerisPacket.ID) and (len(an_packet.data) == self.LENGTH):
            self.unix_time = unpack('<I', bytes(an_packet.data[0:4]))[0]
            self.satellite_system = SatelliteSystem(unpack('<B', bytes(an_packet.data[4]))[0])
            self.satellite_number = unpack('<B', bytes(an_packet.data[5]))[0]
            self.clock_bias = unpack('<f', bytes(an_packet.data[6:10]))[0]
            self.frequency_bias = unpack('<f', bytes(an_packet.data[10:14]))[0]
            self.position = unpack('<ddd', bytes(an_packet.data[14:38]))
            self.velocity = unpack('<ddd', bytes(an_packet.data[38:62]))
            self.acceleration = unpack('<ddd', bytes(an_packet.data[62:86]))
            self.frame_start_time = unpack('<I', bytes(an_packet.data[86:90]))[0]
            self.age = unpack('<B', bytes(an_packet.data[90]))[0]
            self.frequency_slot = unpack('<b', bytes(an_packet.data[91]))[0]
            self.satellite_health = unpack('<B', bytes(an_packet.data[92]))[0]
            return 0
        else:
            return 1


@dataclass()
class RawSatelliteGPSIonoEphemerisPacket:
    """Packet 61 - Raw Satellite Ephemeris Packet (GPS Ionosphere)"""
    unix_time: int = 0
    satellite_system: SatelliteSystem = SatelliteSystem.unknown
    satellite_number: int = 0
    alpha: [float] * 4 = field(default_factory=list)
    beta: [float] * 4 = field(default_factory=list)
    asub: [float] * 2 = field(default_factory=list)
    delta_ls: int = 0
    delta_tlsf: int = 0
    wnsub_lsf: int = 0
    dn: int = 0

    LENGTH = 92

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Raw Satellite Ephemeris Packet (GPS Ionosphere)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == RawSatelliteEphemerisPacket.ID) and (len(an_packet.data) == self.LENGTH):
            self.unix_time = unpack('<I', bytes(an_packet.data[0:4]))[0]
            self.satellite_system = SatelliteSystem(unpack('<B', bytes(an_packet.data[4]))[0])
            self.satellite_number = unpack('<B', bytes(an_packet.data[5]))[0]
            self.alpha = unpack('<dddd', bytes(an_packet.data[6:38]))
            self.beta = unpack('<dddd', bytes(an_packet.data[38:70]))
            self.asub = unpack('<dd', bytes(an_packet.data[70:86]))
            self.delta_ls = unpack('<H', bytes(an_packet.data[86:88]))[0]
            self.delta_tlsf = unpack('<H', bytes(an_packet.data[88:90]))[0]
            self.wnsub_lsf = unpack('<B', bytes(an_packet.data[90]))[0]
            self.dn = unpack('<B', bytes(an_packet.data[91]))[0]
            return 0
        else:
            return 1


@dataclass()
class RawSatelliteEphemerisPacket:
    """Packet 61 - Raw Satellite Ephemeris Packet"""
    gps: RawSatelliteGPSEphemerisPacket = RawSatelliteGPSEphemerisPacket()
    glonass: RawSatelliteGLONASSEphemerisPacket = RawSatelliteGLONASSEphemerisPacket()
    gps_iono: RawSatelliteGPSIonoEphemerisPacket = RawSatelliteGPSIonoEphemerisPacket()

    ID = PacketID.raw_satellite_ephemeris

    def decode(self, an_packet: ANPacket):
        if an_packet.id == self.ID:
            if len(an_packet.data) == RawSatelliteGPSEphemerisPacket.LENGTH:
                self.gps.decode(an_packet)
                return 0
            if len(an_packet.data) == RawSatelliteGLONASSEphemerisPacket.LENGTH:
                self.glonass.decode(an_packet)
                return 0
            if len(an_packet.data) == RawSatelliteGPSIonoEphemerisPacket.LENGTH:
                self.gps_iono.decode(an_packet)
                return 0
        return 1
