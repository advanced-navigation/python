################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_85.py                              ##
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
class SensorTemperaturePacket:
    """Packet 85 - Sensor Temperature Packet"""
    accelerometer_temperature: [float] * 3 = field(default_factory=list)
    gyroscope_temperature: [float] * 3 = field(default_factory=list)
    magnetometer_temperature: float = 0
    pressure_sensor_temperature: float = 0

    ID = PacketID.sensor_temperatures
    LENGTH = 32

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Sensor Temperature Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.accelerometer_temperature = unpack('<fff', bytes(an_packet.data[0:12]))
            self.accelerometer_temperature = unpack('<fff', bytes(an_packet.data[12:24]))
            self.magnetometer_temperature = unpack('<f', bytes(an_packet.data[24:28]))[0]
            self.pressure_sensor_temperature = unpack('<f', bytes(an_packet.data[28:32]))[0]
            return 0
        else:
            return 1
