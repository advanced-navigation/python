################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_28.py                              ##
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


@dataclass()
class RawSensorsPacket:
    """Packet 28 - Raw Sensors Packet"""
    accelerometers: [float] * 3 = field(default_factory=list)
    gyroscopes: [float] * 3 = field(default_factory=list)
    magnetometers: [float] * 3 = field(default_factory=list)
    imu_temperature: float = 0
    pressure: float = 0
    pressure_temperature: float = 0

    ID = PacketID.raw_sensors
    LENGTH = 48

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Raw Sensors Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.accelerometers = unpack('<fff', bytes(an_packet.data[0:12]))
            self.gyroscopes = unpack('<fff', bytes(an_packet.data[12:24]))
            self.magnetometers = unpack('<fff', bytes(an_packet.data[24:36]))
            self.imu_temperature = unpack('<f', bytes(an_packet.data[36:40]))[0]
            self.pressure = unpack('<f', bytes(an_packet.data[40:44]))[0]
            self.pressure_temperature = unpack('<f', bytes(an_packet.data[44:48]))[0]
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
    raw_sensors_status: RawSensorStatusAdu = RawSensorStatusAdu()
    temperature: float = 0

    ID = PacketID.raw_sensors
    LENGTH = 13

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Raw Sensors Packet (ADU)
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.absolute_pressure = unpack('<f', bytes(an_packet.data[0:4]))[0]
            self.differential_pressure = unpack('<f', bytes(an_packet.data[4:8]))[0]
            self.raw_sensors_status.unpack(an_packet.data[8])
            self.temperature = unpack('<f', bytes(an_packet.data[9:13]))[0]
            return 0
        else:
            return 1
