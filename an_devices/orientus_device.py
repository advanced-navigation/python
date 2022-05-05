################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            orientus_device.py                              ##
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

from .advanced_navigation_device import AdvancedNavigationDevice as _AdvancedNavigationDevice
from anpp_packets.an_packets import PacketID as _PacketID

from anpp_packets.an_packet_0 import AcknowledgePacket, AcknowledgeResult
from anpp_packets.an_packet_1 import RequestPacket
from anpp_packets.an_packet_2 import BootModePacket, BootMode
from anpp_packets.an_packet_3 import DeviceInformationPacket
from anpp_packets.an_packet_4 import RestoreFactorySettingsPacket
from anpp_packets.an_packet_5 import ResetPacket, ResetVerification
from anpp_packets.an_packet_7 import FileTransferFirstPacket, DataEncoding, FileTransferMetadata
from anpp_packets.an_packet_8 import FileTransferAcknowledgePacket, FileTransferResponse
from anpp_packets.an_packet_9 import FileTransferOngoingPacket
from anpp_packets.an_packet_20 import SystemStatePacket, GNSSFixType
from anpp_packets.an_packet_21 import UnixTimePacket
from anpp_packets.an_packet_23 import StatusPacket
from anpp_packets.an_packet_26 import EulerOrientationStandardDeviationPacket
from anpp_packets.an_packet_27 import QuaternionOrientationStandardDeviationPacket
from anpp_packets.an_packet_28 import RawSensorsPacket
from anpp_packets.an_packet_37 import AccelerationPacket
from anpp_packets.an_packet_39 import EulerOrientationPacket
from anpp_packets.an_packet_40 import QuaternionOrientationPacket
from anpp_packets.an_packet_41 import DCMOrientationPacket
from anpp_packets.an_packet_42 import AngularVelocityPacket
from anpp_packets.an_packet_43 import AngularAccelerationPacket
from anpp_packets.an_packet_44 import ExternalPositionVelocityPacket
from anpp_packets.an_packet_45 import ExternalPositionPacket
from anpp_packets.an_packet_46 import ExternalVelocityPacket
from anpp_packets.an_packet_48 import ExternalHeadingPacket
from anpp_packets.an_packet_49 import RunningTimePacket
from anpp_packets.an_packet_50 import LocalMagneticFieldPacket
from anpp_packets.an_packet_180 import PacketTimerPeriodPacket
from anpp_packets.an_packet_181 import PacketsPeriodPacket
from anpp_packets.an_packet_182 import BaudRatesPacket
from anpp_packets.an_packet_184 import SensorRangesPacket, AccelerometerRange, GyroscopeRange, MagnetometerRange
from anpp_packets.an_packet_185 import InstallationAlignmentPacket
from anpp_packets.an_packet_186 import FilterOptionsPacket, VehicleType
from anpp_packets.an_packet_188 import GPIOConfigurationPacket, GPIO1Function, GPIO2Function, AuxiliaryTxFunction, AuxiliaryRxFunction, GPIOIndex
from anpp_packets.an_packet_189 import MagneticCalibrationValuesPacket
from anpp_packets.an_packet_190 import MagneticCalibrationConfigurationPacket, MagneticCalibrationAction
from anpp_packets.an_packet_191 import MagneticCalibrationStatusPacket, MagneticCalibrationStatus
from anpp_packets.an_packet_193 import SetZeroOrientationAlignmentPacket


class Orientus(_AdvancedNavigationDevice):
    """ Orientus object with high level functions for setting and receiving values """

    valid_baud_rates = [2400, 4800, 9600, 19200, 38400, 57600,
                        115200, 230400, 250000, 460800, 500000,
                        800000, 921600, 1000000, 1250000, 2000000]

    def return_device_information_and_configuration_packets(self):
        """ Returns Orientus' Device Information and Configuration packets as
            all Advanced Navigation devices have different packets available """
        return [_PacketID.device_information,
                _PacketID.packet_timer_period,
                _PacketID.packets_period,
                _PacketID.baud_rates,
                _PacketID.sensor_ranges,
                _PacketID.installation_alignment,
                _PacketID.filter_options,
                _PacketID.gpio_configuration,
                _PacketID.magnetic_calibration_values,
                _PacketID.magnetic_calibration_status]
