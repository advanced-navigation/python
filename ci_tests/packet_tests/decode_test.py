################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            decode_test.py                                  ##
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

from pathlib import Path
import os

from anpp_packets.an_packet_protocol import ANDecoder
from anpp_packets.an_packets import PacketID
from anpp_packets import *


def get_obj_from_enum(packet_enum):
    match packet_enum:
        case PacketID.acknowledge:
            return an_packet_0.AcknowledgePacket()

        case PacketID.request:
            return an_packet_1.RequestPacket()

        case PacketID.boot_mode:
            return an_packet_2.BootModePacket()

        case PacketID.device_information:
            return an_packet_3.DeviceInformationPacket()

        case PacketID.restore_factory_settings:
            return an_packet_4.RestoreFactorySettingsPacket()

        case PacketID.reset:
            return an_packet_5.ResetPacket()

        case PacketID.file_transfer_request:
            return an_packet_7.FileTransferFirstPacket()

        case PacketID.file_transfer_acknowledge:
            return an_packet_8.FileTransferAcknowledgePacket()

        case PacketID.file_transfer:
            return an_packet_9.FileTransferOngoingPacket()

        case PacketID.serial_port_passthrough:
            return an_packet_10.SerialPortPassthroughPacket()

        case PacketID.ip_configuration:
            return an_packet_11.IPConfigurationPacket()

        case PacketID.extended_device_information:
            return an_packet_13.ExtendedDeviceInformationPacket()

        case PacketID.subcomponent_information:
            return an_packet_14.SubcomponentInformationPacket()

        case PacketID.system_state:
            return an_packet_20.SystemStatePacket()

        case PacketID.unix_time:
            return an_packet_21.UnixTimePacket()

        case PacketID.formatted_time:
            return an_packet_22.FormattedTimePacket()

        case PacketID.status:
            return an_packet_23.StatusPacket()

        case PacketID.position_standard_deviation:
            return an_packet_24.PositionStandardDeviationPacket()

        case PacketID.velocity_standard_deviation:
            return an_packet_25.VelocityStandardDeviationPacket()

        case PacketID.euler_orientation_standard_deviation:
            return an_packet_26.EulerOrientationStandardDeviationPacket()

        case PacketID.quaternion_orientation_standard_deviation:
            return an_packet_27.QuaternionOrientationStandardDeviationPacket()

        case PacketID.raw_sensors:
            return an_packet_28.RawSensorsPacket()

        case PacketID.raw_gnss:
            return an_packet_29.RawGNSSPacket()

        case PacketID.satellites:
            return an_packet_30.SatellitesPacket()

        case PacketID.detailed_satellites:
            return an_packet_31.DetailedSatellitesPacket()

        case PacketID.geodetic_position:
            return an_packet_32.GeodeticPositionPacket()

        case PacketID.ecef_position:
            return an_packet_33.ECEFPositionPacket()

        case PacketID.utm_position:
            return an_packet_34.UTMPositionPacket()

        case PacketID.ned_velocity:
            return an_packet_35.NEDVelocityPacket()

        case PacketID.body_velocity:
            return an_packet_36.BodyVelocityPacket()

        case PacketID.acceleration:
            return an_packet_37.AccelerationPacket()

        case PacketID.body_acceleration:
            return an_packet_38.BodyAccelerationPacket()

        case PacketID.euler_orientation:
            return an_packet_39.EulerOrientationPacket()

        case PacketID.quaternion_orientation:
            return an_packet_40.QuaternionOrientationPacket()

        case PacketID.dcm_orientation:
            return an_packet_41.DCMOrientationPacket()

        case PacketID.angular_velocity:
            return an_packet_42.AngularVelocityPacket()

        case PacketID.angular_acceleration:
            return an_packet_43.AngularAccelerationPacket()

        case PacketID.external_position_velocity:
            return an_packet_44.ExternalPositionVelocityPacket()

        case PacketID.external_position:
            return an_packet_45.ExternalPositionPacket()

        case PacketID.external_velocity:
            return an_packet_46.ExternalVelocityPacket()

        case PacketID.external_body_velocity:
            return an_packet_47.ExternalBodyVelocityPacket()

        case PacketID.external_heading:
            return an_packet_48.ExternalHeadingPacket()

        case PacketID.running_time:
            return an_packet_49.RunningTimePacket()

        case PacketID.local_magnetic_field:
            return an_packet_50.LocalMagneticFieldPacket()

        case PacketID.odometer_state:
            return an_packet_51.OdometerStatePacket()

        case PacketID.external_time:
            return an_packet_52.ExternalTimePacket()

        case PacketID.external_depth:
            return an_packet_53.ExternalDepthPacket()

        case PacketID.geoid_height:
            return an_packet_54.GeoidHeightPacket()

        case PacketID.rtcm_corrections:
            return an_packet_55.RTCMCorrectionsPacket()

        case PacketID.wind:
            return an_packet_57.WindPacket()

        case PacketID.heave:
            return an_packet_58.HeavePacket()

        case PacketID.raw_satellite_data:
            return an_packet_60.RawSatelliteDataPacket()

        case PacketID.raw_satellite_ephemeris:
            return an_packet_61.RawSatelliteEphemerisPacket()

        case PacketID.external_odometer:
            return an_packet_67.ExternalOdometerPacket()

        case PacketID.external_air_data:
            return an_packet_68.ExternalAirDataPacket()

        case PacketID.gnss_receiver_information:
            return an_packet_69.GNSSReceiverInformationPacket()

        case PacketID.raw_dvl_data:
            return an_packet_70.RawDVLDataPacket()

        case PacketID.north_seeking_initialisation_status:
            return an_packet_71.NorthSeekingInitialisationStatusPacket()

        case PacketID.gimbal_state:
            return an_packet_72.GimbalStatePacket()

        case PacketID.automotive:
            return an_packet_73.AutomotivePacket()

        case PacketID.external_magnetometers:
            return an_packet_75.ExternalMagnetometersPacket()

        case PacketID.base_station:
            return an_packet_80.BasestationPacket()

        case PacketID.zero_angular_velocity:
            return an_packet_83.ZeroAngularVelocityPacket()

        case PacketID.extended_satellites:
            return an_packet_84.ExtendedSatellitesPacket()

        case PacketID.sensor_temperatures:
            return an_packet_85.SensorTemperaturePacket()

        case PacketID.packet_timer_period:
            return an_packet_180.PacketTimerPeriodPacket()

        case PacketID.packets_period:
            return an_packet_181.PacketsPeriodPacket()

        case PacketID.baud_rates:
            return an_packet_182.BaudRatesPacket()

        case PacketID.sensor_ranges:
            return an_packet_184.SensorRangesPacket()

        case PacketID.installation_alignment:
            return an_packet_185.InstallationAlignmentPacket()

        case PacketID.filter_options:
            return an_packet_186.FilterOptionsPacket()

        case PacketID.gpio_configuration:
            return an_packet_188.GPIOConfigurationPacket()

        case PacketID.magnetic_calibration_values:
            return an_packet_189.MagneticCalibrationValuesPacket()

        case PacketID.magnetic_calibration_configuration:
            return an_packet_190.MagneticCalibrationConfigurationPacket()

        case PacketID.magnetic_calibration_status:
            return an_packet_191.MagneticCalibrationStatusPacket()

        case PacketID.odometer_configuration:
            return an_packet_192.OdometerConfigurationPacket()

        case PacketID.set_zero_orientation_alignment:
            return an_packet_193.SetZeroOrientationAlignmentPacket()

        case PacketID.reference_point_offsets:
            return an_packet_194.ReferencePointOffsetsPacket()

        case PacketID.gpio_output_configuration:
            return an_packet_195.GPIOOutputConfigurationPacket()

        case PacketID.dual_antenna_configuration:
            return an_packet_196.DualAntennaConfigurationPacket()

        case PacketID.gnss_configuration:
            return an_packet_197.GNSSConfigurationPacket()

        case PacketID.user_data:
            return an_packet_198.UserDataPacket()

        case PacketID.gpio_input_configuration:
            return an_packet_199.GPIOInputConfigurationPacket()

        case PacketID.ip_dataports_configuration:
            return an_packet_202.IPDataportConfigurationPacket()

        case PacketID.can_configuration:
            return an_packet_203.CANConfigurationPacket()

        case _:
            return None


def test_decode_packets():
    packet_list = [
        an_packet_id
        for an_packet_id in PacketID._value2member_map_
        if an_packet_id
        not in [0, 1, 4, 5, 7, 8, 9, 10, 52, 55, 60, 61, 67, 80, 83, 184, 190, 193]
    ]

    packet_decoded = []
    with open(
        Path(os.path.dirname(os.path.abspath(__file__))).joinpath("Log.anpp"), "rb"
    ) as l:
        raw_data = l.read()

    decoder = ANDecoder()
    decoder.add_data(raw_data)
    while True:
        an_packet = decoder.decode()

        if an_packet is None:
            break

        new_packet = get_obj_from_enum(an_packet.id)
        assert an_packet is not None, "ANPacket is none"
        assert new_packet.decode(an_packet) == 0
        packet_decoded.append(new_packet.ID.value)

    assert all(packet in set(packet_decoded) for packet in packet_list)
