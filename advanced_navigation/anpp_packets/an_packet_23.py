################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_23.py                              ##
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
from .an_packets import PacketID
from .an_packet_protocol import ANPacket
from .an_packet_20 import SystemStatus, FilterStatus


@dataclass()
class StatusPacket:
    """Packet 23 - Status Packet"""

    system_status: SystemStatus = field(default_factory=SystemStatus, repr=False)
    filter_status: FilterStatus = field(default_factory=FilterStatus, repr=False)

    ID = PacketID.status
    LENGTH = 4

    _structure = struct.Struct("<HH")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Status Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.system_status.unpack(values[0])
            self.filter_status.unpack(values[1])
            return 0
        else:
            return 1

@dataclass()
class StatusPacketAdu2:
    """Packet 23 - ADU V2 Status Packet"""

    system_failure: bool = False
    absolute_pressure_sensor_failure: bool = False
    absolute_pressure_sensor_max_temp_alarm: bool = False
    absolute_pressure_sensor_min_temp_alarm: bool = False
    absolute_pressure_sensor_over_range: bool = False
    differential_pressure_sensor_failure: bool = False
    differential_pressure_sensor_max_temp_alarm: bool = False
    differential_pressure_sensor_min_temp_alarm: bool = False
    differential_pressure_sensor_over_range: bool = False
    aux_absolute_pressure_sensor_failure: bool = False
    aux_absolute_pressure_sensor_max_temp_alarm: bool = False
    aux_absolute_pressure_sensor_min_temp_alarm: bool = False
    aux_absolute_pressure_sensor_over_range: bool = False
    external_temperature_sensor_failure: bool = False
    external_temperature_sensor_over_range: bool = False
    minimum_temperature_alarm: bool = False
    maximum_temperature_alarm: bool = False

    ID = PacketID.status
    LENGTH = 4

    _structure = struct.Struct("<I")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to ADU v2 Status Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            status, = self._structure.unpack_from(an_packet.data)
            self.system_failure = (status & (1 << 0)) != 0
            self.absolute_pressure_sensor_failure = (status & (1 << 1)) != 0
            self.absolute_pressure_sensor_max_temp_alarm = (status & (1 << 2)) != 0
            self.absolute_pressure_sensor_min_temp_alarm = (status & (1 << 3)) != 0
            self.absolute_pressure_sensor_over_range = (status & (1 << 4)) != 0
            self.differential_pressure_sensor_failure = (status & (1 << 5)) != 0
            self.differential_pressure_sensor_max_temp_alarm = (status & (1 << 6)) != 0
            self.differential_pressure_sensor_min_temp_alarm = (status & (1 << 7)) != 0
            self.differential_pressure_sensor_over_range = (status & (1 << 8)) != 0
            self.aux_absolute_pressure_sensor_failure = (status & (1 << 9)) != 0
            self.aux_absolute_pressure_sensor_max_temp_alarm = (status & (1 << 10)) != 0
            self.aux_absolute_pressure_sensor_min_temp_alarm = (status & (1 << 11)) != 0
            self.aux_absolute_pressure_sensor_over_range = (status & (1 << 12)) != 0
            self.external_temperature_sensor_failure = (status & (1 << 13)) != 0
            self.external_temperature_sensor_over_range = (status & (1 << 14)) != 0
            self.minimum_temperature_alarm = (status & (1 << 15)) != 0
            self.maximum_temperature_alarm = (status & (1 << 16)) != 0

            return 0
        else:
            return 1
