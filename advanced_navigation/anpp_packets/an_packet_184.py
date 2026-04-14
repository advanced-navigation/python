################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_184.py                              ##
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

from dataclasses import dataclass
from enum import Enum
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


class AccelerometerRange(Enum):
    """Accelerometer Range"""

    accelerometer_range_2g = 0
    accelerometer_range_4g = 1
    accelerometer_range_16g = 2


class GyroscopeRange(Enum):
    """Gyroscope Range"""

    gyroscope_range_250dps = 0
    gyroscope_range_500dps = 1
    gyroscope_range_2000dps = 2


class MagnetometerRange(Enum):
    """Magnetometer Range"""

    magnetometer_range_2g = 0
    magnetometer_range_4g = 1
    magnetometer_range_8g = 2


@dataclass()
class SensorRangesPacket:
    """Packet 184 - Sensor Ranges Packet"""

    permanent: int = 0
    accelerometers_range: AccelerometerRange = AccelerometerRange.accelerometer_range_2g
    gyroscopes_range: GyroscopeRange = GyroscopeRange.gyroscope_range_250dps
    magnetometers_range: MagnetometerRange = MagnetometerRange.magnetometer_range_2g

    ID = PacketID.sensor_ranges
    LENGTH = 4

    _structure = struct.Struct("<BBBB")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Sensor Ranges Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                self.permanent,
                accelerometers_range_value,
                gyroscopes_range_value,
                magnetometers_range_value,
            ) = self._structure.unpack_from(an_packet.data)

            self.accelerometers_range = AccelerometerRange(accelerometers_range_value)
            self.gyroscopes_range = GyroscopeRange(gyroscopes_range_value)
            self.magnetometers_range = MagnetometerRange(magnetometers_range_value)
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode Sensor Ranges Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.accelerometers_range.value,
            self.gyroscopes_range.value,
            self.magnetometers_range.value,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
