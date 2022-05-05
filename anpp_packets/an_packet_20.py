################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_20.py                              ##
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


class GNSSFixType(Enum):
    """GNSS Fix Type"""
    none = 0
    twoD = 1
    threeD = 2
    sbas = 3
    differential = 4
    omnistar = 5
    rtk_float = 6
    rtk_fixed = 7


@dataclass()
class SystemStatus:
    """System Status"""
    system_failure: bool = False
    accelerometer_sensor_failure: bool = False
    gyroscope_sensor_failure: bool = False
    magnetometer_sensor_failure: bool = False
    pressure_sensor_failure: bool = False
    gnss_failure: bool = False
    accelerometer_over_range: bool = False
    gyroscope_over_range: bool = False
    magnetometer_over_range: bool = False
    pressure_over_range: bool = False
    minimum_temperature_alarm: bool = False
    maximum_temperature_alarm: bool = False
    low_voltage_alarm: bool = False
    high_voltage_alarm: bool = False
    gnss_antenna_disconnected: bool = False
    data_output_overflow_alarm: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.system_failure = (data & (1 << 0)) != 0
        self.accelerometer_sensor_failure = (data & (1 << 1)) != 0
        self.gyroscope_sensor_failure = (data & (1 << 2)) != 0
        self.magnetometer_sensor_failure = (data & (1 << 3)) != 0
        self.pressure_sensor_failure = (data & (1 << 4)) != 0
        self.gnss_failure = (data & (1 << 5)) != 0
        self.accelerometer_over_range = (data & (1 << 6)) != 0
        self.gyroscope_over_range = (data & (1 << 7)) != 0
        self.magnetometer_over_range = (data & (1 << 8)) != 0
        self.pressure_over_range = (data & (1 << 9)) != 0
        self.minimum_temperature_alarm = (data & (1 << 10)) != 0
        self.maximum_temperature_alarm = (data & (1 << 11)) != 0
        self.low_voltage_alarm = (data & (1 << 12)) != 0
        self.high_voltage_alarm = (data & (1 << 13)) != 0
        self.gnss_antenna_disconnected = (data & (1 << 14)) != 0
        self.data_output_overflow_alarm = (data & (1 << 15)) != 0


@dataclass()
class FilterStatus:
    """Filter Status"""
    orientation_filter_initialised: bool = False
    ins_filter_initialised: bool = False
    heading_initialised: bool = False
    utc_time_initialised: bool = False
    gnss_fix_type: GNSSFixType = GNSSFixType.none
    event1_flag: bool = False
    event2_flag: bool = False
    internal_gnss_enabled: bool = False
    magnetic_heading_enabled: bool = False
    velocity_heading_enabled: bool = False
    atmospheric_altitude_enabled: bool = False
    external_position_active: bool = False
    external_velocity_active: bool = False
    external_heading_active: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.orientation_filter_initialised = (data & (1 << 0)) != 0
        self.ins_filter_initialised = (data & (1 << 1)) != 0
        self.heading_initialised = (data & (1 << 2)) != 0
        self.utc_time_initialised = (data & (1 << 3)) != 0
        self.gnss_fix_type = GNSSFixType((data & 0x0070) >> 4)
        self.event1_flag = (data & (1 << 7)) != 0
        self.event2_flag = (data & (1 << 8)) != 0
        self.internal_gnss_enabled = (data & (1 << 9)) != 0
        self.magnetic_heading_enabled = (data & (1 << 10)) != 0
        self.velocity_heading_enabled = (data & (1 << 11)) != 0
        self.atmospheric_altitude_enabled = (data & (1 << 12)) != 0
        self.external_position_active = (data & (1 << 13)) != 0
        self.external_velocity_active = (data & (1 << 14)) != 0
        self.external_heading_active = (data & (1 << 15)) != 0


@dataclass()
class SystemStatePacket:
    """Packet 20 - System State Packet"""
    system_status: SystemStatus = SystemStatus()
    filter_status: FilterStatus = FilterStatus()
    unix_time_seconds: int = 0
    microseconds: int = 0
    latitude: float = 0
    longitude: float = 0
    height: float = 0
    velocity: [float] * 3 = field(default_factory=list)
    body_acceleration: [float] * 3 = field(default_factory=list)
    g_force: float = field(default_factory=list)
    orientation: [float] * 3 = field(default_factory=list)
    angular_velocity: [float] * 3 = field(default_factory=list)
    standard_deviation: [float] * 3 = field(default_factory=list)

    ID = PacketID.system_state
    LENGTH = 100

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to System State Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.system_status.unpack(unpack('<H', bytes(an_packet.data[0:2]))[0])
            self.filter_status.unpack(unpack('<H', bytes(an_packet.data[2:4]))[0])
            self.unix_time_seconds = unpack('<I', bytes(an_packet.data[4:8]))[0]
            self.microseconds = unpack('<I', bytes(an_packet.data[8:12]))[0]
            self.latitude = unpack('<d', bytes(an_packet.data[12:20]))[0]
            self.longitude = unpack('<d', bytes(an_packet.data[20:28]))[0]
            self.height = unpack('<d', bytes(an_packet.data[28:36]))[0]
            self.velocity = unpack('<fff', bytes(an_packet.data[36:48]))
            self.body_acceleration = unpack('<fff', bytes(an_packet.data[48:60]))
            self.g_force = unpack('<f', bytes(an_packet.data[60:64]))[0]
            self.orientation = unpack('<fff', bytes(an_packet.data[64:76]))
            self.angular_velocity = unpack('<fff', bytes(an_packet.data[76:88]))
            self.standard_deviation = unpack('<fff', bytes(an_packet.data[88:100]))
            return 0
        else:
            return 1
