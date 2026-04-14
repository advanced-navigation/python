################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_191.py                              ##
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


class MagneticCalibrationStatus(Enum):
    """Magnetic Calibration Status"""

    not_completed = 0
    completed_2d = 1
    completed_3d = 2
    completed_custom_values = 3
    in_progress_2d = 5
    in_progress_3d = 6
    error_excessive_roll_2d = 7
    error_excessive_pitch_2d = 8
    error_overrange_event = 9
    error_timeout = 10
    error_system = 11
    error_interference = 12


@dataclass()
class MagneticCalibrationStatusPacket:
    """Packet 191 - Magnetic Calibration Status Packet"""

    magnetic_calibration_status: MagneticCalibrationStatus = (
        MagneticCalibrationStatus.not_completed
    )
    magnetic_calibration_progress_percentage: int = 0
    local_magnetic_error_percentage: int = 0

    ID = PacketID.magnetic_calibration_status
    LENGTH = 3

    _structure = struct.Struct("<BBB")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to Magnetic Calibration Status Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.magnetic_calibration_status = MagneticCalibrationStatus(values[0])
            self.magnetic_calibration_progress_percentage = values[1]
            self.local_magnetic_error_percentage = values[2]
            return 0
        else:
            return 1
