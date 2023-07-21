################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                        advanced_navigation_device.py                       ##
##                     Copyright 2021, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2021 Advanced Navigation                                       #
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

import os
import serial
import serial.serialutil as serialutil
from abc import ABC, abstractmethod

from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANDecoder
from anpp_packets.an_packet_0 import AcknowledgePacket, AcknowledgeResult
from anpp_packets.an_packet_1 import RequestPacket
from anpp_packets.an_packet_2 import BootModePacket, BootMode
from anpp_packets.an_packet_3 import DeviceInformationPacket
from anpp_packets.an_packet_4 import RestoreFactorySettingsPacket
from anpp_packets.an_packet_5 import ResetPacket, ResetVerification
from anpp_packets.an_packet_7 import (
    FileTransferFirstPacket,
    DataEncoding,
    FileTransferMetadata,
)
from anpp_packets.an_packet_8 import FileTransferAcknowledgePacket, FileTransferResponse
from anpp_packets.an_packet_9 import FileTransferOngoingPacket
from anpp_packets.an_packet_10 import SerialPortPassthroughPacket, PassthroughRoute
from anpp_packets.an_packet_11 import IPConfigurationPacket, LinkMode, DHCPMode
from anpp_packets.an_packet_13 import (
    ExtendedDeviceInformationPacket,
    CertusDeviceSubtype,
)
from anpp_packets.an_packet_14 import SubcomponentInformationPacket
from anpp_packets.an_packet_20 import SystemStatePacket, GNSSFixType
from anpp_packets.an_packet_21 import UnixTimePacket
from anpp_packets.an_packet_22 import FormattedTimePacket
from anpp_packets.an_packet_23 import StatusPacket
from anpp_packets.an_packet_24 import PositionStandardDeviationPacket
from anpp_packets.an_packet_25 import VelocityStandardDeviationPacket
from anpp_packets.an_packet_26 import EulerOrientationStandardDeviationPacket
from anpp_packets.an_packet_27 import QuaternionOrientationStandardDeviationPacket
from anpp_packets.an_packet_28 import RawSensorsPacket
from anpp_packets.an_packet_29 import RawGNSSPacket
from anpp_packets.an_packet_30 import SatellitesPacket
from anpp_packets.an_packet_31 import DetailedSatellitesPacket
from anpp_packets.an_packet_32 import GeodeticPositionPacket
from anpp_packets.an_packet_33 import ECEFPositionPacket
from anpp_packets.an_packet_34 import UTMPositionPacket
from anpp_packets.an_packet_35 import NEDVelocityPacket
from anpp_packets.an_packet_36 import BodyVelocityPacket
from anpp_packets.an_packet_37 import AccelerationPacket
from anpp_packets.an_packet_38 import BodyAccelerationPacket
from anpp_packets.an_packet_39 import EulerOrientationPacket
from anpp_packets.an_packet_40 import QuaternionOrientationPacket
from anpp_packets.an_packet_41 import DCMOrientationPacket
from anpp_packets.an_packet_42 import AngularVelocityPacket
from anpp_packets.an_packet_43 import AngularAccelerationPacket
from anpp_packets.an_packet_44 import ExternalPositionVelocityPacket
from anpp_packets.an_packet_45 import ExternalPositionPacket
from anpp_packets.an_packet_46 import ExternalVelocityPacket
from anpp_packets.an_packet_47 import ExternalBodyVelocityPacket
from anpp_packets.an_packet_48 import ExternalHeadingPacket
from anpp_packets.an_packet_49 import RunningTimePacket
from anpp_packets.an_packet_50 import LocalMagneticFieldPacket
from anpp_packets.an_packet_51 import OdometerStatePacket
from anpp_packets.an_packet_52 import ExternalTimePacket
from anpp_packets.an_packet_53 import ExternalDepthPacket
from anpp_packets.an_packet_54 import GeoidHeightPacket
from anpp_packets.an_packet_55 import RTCMCorrectionsPacket
from anpp_packets.an_packet_57 import WindPacket
from anpp_packets.an_packet_58 import HeavePacket
from anpp_packets.an_packet_60 import (
    RawSatelliteDataPacket,
    GPSSatelliteFrequency,
    GLONASSSatelliteFrequency,
    GalileoSatelliteFrequency,
    BeiDouSatelliteFrequency,
    SBASSatelliteFrequency,
    QZSSSatelliteFrequency,
)
from anpp_packets.an_packet_61 import RawSatelliteEphemerisPacket
from anpp_packets.an_packet_67 import ExternalOdometerPacket
from anpp_packets.an_packet_68 import ExternalAirDataPacket
from anpp_packets.an_packet_69 import (
    GNSSReceiverInformationPacket,
    GNSSManufacturerID,
    TrimbleGNSSReceiverModel,
    AdvancedNavigationGNSSReceiverModel,
    OmnistarEngineMode,
)
from anpp_packets.an_packet_70 import RawDVLDataPacket
from anpp_packets.an_packet_71 import NorthSeekingInitialisationStatusPacket
from anpp_packets.an_packet_72 import GimbalStatePacket
from anpp_packets.an_packet_73 import AutomotivePacket
from anpp_packets.an_packet_75 import ExternalMagnetometersPacket
from anpp_packets.an_packet_80 import BasestationPacket
from anpp_packets.an_packet_83 import ZeroAngularVelocityPacket
from anpp_packets.an_packet_84 import ExtendedSatellitesPacket
from anpp_packets.an_packet_85 import SensorTemperaturePacket
from anpp_packets.an_packet_180 import PacketTimerPeriodPacket
from anpp_packets.an_packet_181 import PacketsPeriodPacket
from anpp_packets.an_packet_182 import BaudRatesPacket
from anpp_packets.an_packet_184 import (
    SensorRangesPacket,
    AccelerometerRange,
    GyroscopeRange,
    MagnetometerRange,
)
from anpp_packets.an_packet_185 import InstallationAlignmentPacket
from anpp_packets.an_packet_186 import FilterOptionsPacket, VehicleType
from anpp_packets.an_packet_188 import (
    GPIOConfigurationPacket,
    GPIO1Function,
    GPIO2Function,
    AuxiliaryTxFunction,
    AuxiliaryRxFunction,
    GPIOIndex,
)
from anpp_packets.an_packet_189 import MagneticCalibrationValuesPacket
from anpp_packets.an_packet_190 import (
    MagneticCalibrationConfigurationPacket,
    MagneticCalibrationAction,
)
from anpp_packets.an_packet_191 import (
    MagneticCalibrationStatusPacket,
    MagneticCalibrationStatus,
)
from anpp_packets.an_packet_192 import OdometerConfigurationPacket
from anpp_packets.an_packet_193 import SetZeroOrientationAlignmentPacket
from anpp_packets.an_packet_194 import ReferencePointOffsetsPacket
from anpp_packets.an_packet_195 import (
    GPIOOutputConfigurationPacket,
    GPIORate,
    NMEAFixBehaviour,
)
from anpp_packets.an_packet_196 import (
    DualAntennaConfigurationPacket,
    OffsetType,
    AutomaticOffsetOrientation,
)
from anpp_packets.an_packet_197 import (
    GNSSConfigurationPacket,
    LBandMode,
    LBandSatelliteID,
    GNSSFrequencies,
)
from anpp_packets.an_packet_198 import UserDataPacket
from anpp_packets.an_packet_199 import GPIOInputConfigurationPacket
from anpp_packets.an_packet_202 import IPDataportConfigurationPacket, IPDataportMode
from anpp_packets.an_packet_203 import CANConfigurationPacket, CANProtocol


class AdvancedNavigationDevice(ABC):
    def __init__(self, port, baud):
        self.bytes_waiting = ANDecoder()
        self.ser = None
        self.logFile = None

        if isinstance(port, str):
            self.port = port
        else:
            print(f"Port:{port} is not valid")

        if int(baud) in self.valid_baud_rates:
            self.baud = baud
        else:
            print(f"Baud Rate:{baud} is not valid")

    @property
    @abstractmethod
    def valid_baud_rates(self):
        """Child class needs to declare this property"""
        pass

    # Serial Communications
    def start_serial(self):
        # Checks if operating system is Windows or Linux
        if (os.name == "nt") or (os.name == "posix"):
            # Connects to serial port
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                bytesize=serialutil.EIGHTBITS,
                parity=serialutil.PARITY_NONE,
                stopbits=serialutil.STOPBITS_ONE,
                timeout=None,
                xonxoff=False,
                rtscts=False,
                write_timeout=None,
                dsrdtr=False,
                inter_byte_timeout=None,
            )
        else:
            print(
                f"Packet_example currently only supports Windows and Linux operating systems."
            )
            exit()

    def close(self):
        self.ser.close()

    def is_open(self):
        return self.ser.is_open

    def flush(self):
        self.ser.flush()

    def in_waiting(self):
        return self.ser.in_waiting

    def read(self, bytes_in_buffer):
        return self.ser.read(bytes_in_buffer)

    # Device and Configuration Information
    @abstractmethod
    def return_device_information_and_configuration_packets(self):
        """Child class needs to implement this method to return
        the device information and configuration packets as a list"""
        pass

    def get_device_and_configuration_information(self):
        packets = self.return_device_information_and_configuration_packets()
        if len(packets) != 0:
            self.request_packet(packets)
        else:
            print("Warning: No Device Information or Configuration packets defined.")

    # System Packets
    def request_packet(self, packet_id: PacketID):
        print(f"Requesting PacketIDs: {packet_id}")
        self.ser.write(RequestPacket(packet_id).encode().bytes())
