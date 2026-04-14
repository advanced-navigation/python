################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_190.py                              ##
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


class MagneticCalibrationAction(Enum):
    """Magnetic Calibration Action"""

    cancel = 0
    start_2d = 2
    start_3d = 3
    reset = 4


@dataclass()
class MagneticCalibrationConfigurationPacket:
    """Packet 190 - Magnetic Calibration Configuration Packet"""

    magnetic_calibration_action: MagneticCalibrationAction = (
        MagneticCalibrationAction.cancel
    )

    ID = PacketID.magnetic_calibration_configuration
    LENGTH = 1

    _structure = struct.Struct("<B")

    def encode(self) -> ANPacket:
        """Encode Magnetic Calibration Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(self.magnetic_calibration_action.value)

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
