################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_28.py                              ##
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
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class RawSensorsPacket:
    """Packet 28 - Raw Sensors Packet"""

    accelerometers: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    gyroscopes: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    magnetometers: List[float] = field(default_factory=lambda: [0, 0, 0], repr=False)
    imu_temperature: float = 0
    pressure: float = 0
    pressure_temperature: float = 0

    ID = PacketID.raw_sensors
    LENGTH = 48

    _structure = struct.Struct("<ffffffffffff")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Raw Sensors Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.accelerometers = list(values[0:3])
            self.gyroscopes = list(values[3:6])
            self.magnetometers = list(values[6:9])

            (self.imu_temperature, self.pressure, self.pressure_temperature) = values[
                9:12
            ]
            return 0
        else:
            return 1


@dataclass()
class RawSensorStatusAdu:
    """Raw Sensor Status (ADU)"""

    absolute_pressure_valid: bool = False
    differential_pressure_valid: bool = False
    absolute_pressure_sensor_overrange: bool = False
    differential_pressure_sensor_overrange: bool = False
    absolute_pressure_sensor_failure: bool = False
    differential_pressure_sensor_failure: bool = False
    temperature_sensor_valid: bool = False
    temperature_sensor_failure: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.absolute_pressure_valid = (data & (1 << 0)) != 0
        self.differential_pressure_valid = (data & (1 << 1)) != 0
        self.absolute_pressure_sensor_overrange = (data & (1 << 2)) != 0
        self.differential_pressure_sensor_overrange = (data & (1 << 3)) != 0
        self.absolute_pressure_sensor_failure = (data & (1 << 4)) != 0
        self.differential_pressure_sensor_failure = (data & (1 << 5)) != 0
        self.temperature_sensor_valid = (data & (1 << 6)) != 0
        self.temperature_sensor_failure = (data & (1 << 7)) != 0


@dataclass()
class RawSensorsPacketAdu:
    """Packet 28 - Raw Sensors Packet (ADU)"""

    absolute_pressure: float = 0
    differential_pressure: float = 0
    raw_sensors_status: RawSensorStatusAdu = field(
        default_factory=RawSensorStatusAdu, repr=False
    )
    temperature: float = 0

    ID = PacketID.raw_sensors
    LENGTH = 13

    _structure = struct.Struct("<ffBf")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Raw Sensors Packet (ADU)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.absolute_pressure,
                self.differential_pressure,
                self.raw_sensors_status,
                self.temperature,
            ) = self._structure.unpack_from(an_packet.data)
            return 0
        else:
            return 1
