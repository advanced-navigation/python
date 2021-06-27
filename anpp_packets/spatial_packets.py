################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                             spatial_packets.py                             ##
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

from anpp_packets.anpp_packets import *

""" ANPP Packets for Spatial as defined in Spatial Reference Manual """
class SpatialPackets(PacketID,
                     AcknowledgeResult,
                     AcknowledgePacket,
                     RequestPacket,
                     BootMode,
                     BootModePacket,
                     DeviceInformationPacket,
                     RestoreFactorySettingsPacket,
                     ResetVerification,
                     ResetPacket,
                     GNSSFixType,
                     SystemStatus,
                     FilterStatus,
                     SystemStatePacket,
                     UnixTimePacket,
                     FormattedTimePacket,
                     StatusPacket,
                     PositionStandardDeviationPacket,
                     VelocityStandardDeviationPacket,
                     EulerOrientationStandardDeviationPacket,
                     QuaternionOrientationStandardDeviationPacket,
                     RawSensorsPacket,
                     RawGNSSFlags,
                     RawGNSSPacket,
                     SatellitesPacket,
                     SatelliteSystem,
                     Frequencies,
                     Satellite,
                     DetailedSatellitesPacket,
                     GeodeticPositionPacket,
                     ECEFPositionPacket,
                     UTMPositionPacket,
                     NEDVelocityPacket,
                     BodyVelocityPacket,
                     AccelerationPacket,
                     BodyAccelerationPacket,
                     EulerOrientationPacket,
                     QuaternionOrientationPacket,
                     DCMOrientationPacket,
                     AngularVelocityPacket,
                     AngularAccelerationPacket,
                     ExternalPositionVelocityPacket,
                     ExternalPositionPacket,
                     ExternalVelocityPacket,
                     ExternalBodyVelocityPacket,
                     ExternalHeadingPacket,
                     RunningTimePacket,
                     LocalMagneticFieldPacket,
                     OdometerStatePacket,
                     ExternalTimePacket,
                     ExternalDepthPacket,
                     GeoidHeightPacket,
                     WindPacket,
                     HeavePacket,
                     TrackingStatus,
                     FrequencyInformation,
                     SatelliteData,
                     RawSatelliteDataPacket,
                     OdometerFlags,
                     ExternalOdometerPacket,
                     ExternalAirDataPacketFlags,
                     ExternalAirDataPacket,
                     PacketTimerPeriodPacket,
                     PacketPeriod,
                     PacketsPeriodPacket,
                     BaudRatesPacket,
                     AccelerometerRange,
                     GyroscopeRange,
                     MagnetometerRange,
                     SensorRangesPacket,
                     InstallationAlignmentPacket,
                     VehicleType,
                     FilterOptionsPacket,
                     GPIO1Function,
                     GPIO2Function,
                     AuxiliaryTxFunction,
                     AuxiliaryRxFunction,
                     GPIOIndex,
                     GPIOConfigurationPacket,
                     MagneticCalibrationValuesPacket,
                     MagneticCalibrationAction,
                     MagneticCalibrationConfigurationPacket,
                     MagneticCalibrationStatus,
                     MagneticCalibrationStatusPacket,
                     OdometerConfigurationPacket,
                     SetZeroOrientationAlignmentPacket,
                     ReferencePointOffsetsPacket,
                     GPIORate,
                     NMEAFixBehaviour,
                     GPIOOutputRate,
                     GPIOOutputConfigurationPacket):
    pass