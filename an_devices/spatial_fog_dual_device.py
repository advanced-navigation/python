################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                         spatial_fog_dual_device.py                         ##
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

from .advanced_navigation_device_serial import (
    AdvancedNavigationDeviceSerial as _AdvancedNavigationDevice,
)
from anpp_packets.an_packets import PacketID as _PacketID

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
from anpp_packets.an_packet_31 import DetailedSatellitesPacket, SatelliteSystem
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
from anpp_packets.an_packet_71 import NorthSeekingInitialisationStatusPacket
from anpp_packets.an_packet_72 import GimbalStatePacket
from anpp_packets.an_packet_73 import AutomotivePacket
from anpp_packets.an_packet_180 import PacketTimerPeriodPacket
from anpp_packets.an_packet_181 import PacketsPeriodPacket
from anpp_packets.an_packet_182 import BaudRatesPacket
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
from anpp_packets.an_packet_198 import UserDataPacket
from anpp_packets.an_packet_199 import GPIOInputConfigurationPacket


class SpatialFOGDual(_AdvancedNavigationDevice):
    """Spatial FOG Dual object with high level functions for setting and receiving values"""

    valid_baud_rates = [
        2400,
        4800,
        9600,
        19200,
        38400,
        57600,
        115200,
        230400,
        250000,
        460800,
        500000,
        800000,
        921600,
        1000000,
        1250000,
        2000000,
    ]

    def return_device_information_and_configuration_packets(self):
        """Returns Spatial FOG Dual's Device Information and Configuration packets as
        all Advanced Navigation devices have different packets available"""
        return [
            _PacketID.device_information,
            _PacketID.gnss_receiver_information,
            _PacketID.north_seeking_initialisation_status,
            _PacketID.packet_timer_period,
            _PacketID.packets_period,
            _PacketID.baud_rates,
            _PacketID.installation_alignment,
            _PacketID.filter_options,
            _PacketID.gpio_configuration,
            _PacketID.odometer_configuration,
            _PacketID.reference_point_offsets,
            _PacketID.gpio_output_configuration,
            _PacketID.dual_antenna_configuration,
            _PacketID.user_data,
            _PacketID.gpio_input_configuration,
        ]
