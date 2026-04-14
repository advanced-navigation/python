################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            supported_packets.py                            ##
##                     Copyright 2026, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2026 Advanced Navigation                                       #
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

from typing import List
from ..anpp_packets.an_packet_3 import DeviceID as DID
from ..anpp_packets.an_packets import PacketID as PID
from .device_capabilities import (
    has_base_station,
    has_can,
    has_detailed_satellites,
    has_dual_antenna_configuration,
    has_extended_device_information,
    has_extended_satellites,
    has_external_air_data,
    has_external_magnetometers,
    has_external_sound_velocity,
    has_external_temperature_sensor_configuration,
    has_gnss_configuration,
    has_gnss_receiver_information,
    has_gnss_summary,
    has_internal_gnss,
    has_local_magnetic_field,
    has_magnetic_calibration,
    has_networking,
    has_north_seeking,
    has_odometer_support,
    has_packet_timer_period,
    has_raw_satellite_ephemeris,
    has_sensor_ranges,
    has_sensor_temperatures,
    has_system_temperatures,
    has_zero_angular_velocity,
    is_air_data_unit,
    is_boreas,
    is_ins,
    is_orientus
)

def get_supported_packets(device_id: DID) -> List[PID]:
    """Get the list of packets supported by the device"""

    # Base packets
    packets = {
        PID.acknowledge,
        PID.request,
        PID.boot_mode,
        PID.device_information,
        PID.reset,
        PID.raw_sensors
    }

    # Common packets excluding Air Data Unit v1
    if device_id != DID.air_data_unit:
        packets.update({
            PID.restore_factory_settings,
            PID.file_transfer_request,
            PID.file_transfer_acknowledge,
            PID.file_transfer,
            PID.system_state,
            PID.quaternion_orientation_standard_deviation,
            PID.baud_rates
        })

    # Common packets excluding Air Data Unit
    if not is_air_data_unit(device_id):
        packets.update({
            PID.unix_time,
            PID.status,
            PID.euler_orientation_standard_deviation,
            PID.acceleration,
            PID.euler_orientation,
            PID.quaternion_orientation,
            PID.dcm_orientation,
            PID.angular_velocity,
            PID.angular_acceleration,
            PID.external_position_velocity,
            PID.external_position,
            PID.external_velocity,
            PID.external_heading,
            PID.running_time,
            PID.packets_period,
            PID.installation_alignment,
            PID.filter_options,
            PID.gpio_configuration,
            PID.set_zero_orientation_alignment
        })

    # Common packets excluding Air Data Unit and Orientus
    if not is_air_data_unit(device_id) and not is_orientus(device_id):
        packets.update({
            PID.serial_port_passthrough,
            PID.gpio_output_configuration
        })

    if is_ins(device_id):
        packets.update({
            PID.formatted_time,
            PID.position_standard_deviation,
            PID.velocity_standard_deviation,
            PID.raw_gnss,
            PID.satellites,
            PID.geodetic_position,
            PID.ecef_position,
            PID.utm_position,
            PID.ned_velocity,
            PID.body_velocity,
            PID.body_acceleration,
            PID.external_body_velocity,
            PID.external_time,
            PID.external_depth,
            PID.geoid_height,
            PID.rtcm_corrections,
            PID.wind,
            PID.heave,
            PID.automotive,
            PID.reference_point_offsets
        })

    if is_ins(device_id) and device_id != DID.gnss_compass:
        packets.update({
            PID.external_odometer,
            PID.gimbal_state,
            PID.user_data,
            PID.gpio_input_configuration
        })

    if is_boreas(device_id) or device_id == DID.certus:
        packets.update({
            PID.subcomponent_information,
            PID.raw_dvl_data,
            PID.vessel_motion,
            PID.gnss_position_velocity_time,
            PID.gnss_orientation
        })

    if has_base_station(device_id):
        packets.update({
            PID.base_station
        })

    if has_can(device_id):
        packets.update({
            PID.can_configuration
        })

    if has_detailed_satellites(device_id):
        packets.update({
            PID.detailed_satellites
        })

    if has_dual_antenna_configuration(device_id):
        packets.update({
            PID.dual_antenna_configuration
        })

    if has_extended_device_information(device_id):
        packets.update({
            PID.extended_device_information
        })

    if has_extended_satellites(device_id):
        packets.update({
            PID.extended_satellites
        })

    if has_external_air_data(device_id):
        packets.update({
            PID.external_air_data
        })

    if has_external_magnetometers(device_id):
        packets.update({
            PID.external_magnetometers
        })

    if has_external_sound_velocity(device_id):
        packets.update({
            PID.external_sound_velocity_sensor
        })

    if has_external_temperature_sensor_configuration(device_id):
        packets.update({
            PID.external_temperature_sensor_configuration
        })

    if has_gnss_configuration(device_id):
        packets.update({
            PID.gnss_configuration
        })

    if has_gnss_receiver_information(device_id):
        packets.update({
            PID.gnss_receiver_information,
        })

    if has_gnss_summary(device_id):
        packets.update({
            PID.gnss_summary
        })

    if has_internal_gnss(device_id):
        packets.update({
            PID.raw_satellite_data
        })

    if has_local_magnetic_field(device_id):
        packets.update({
            PID.local_magnetic_field
        })

    if has_magnetic_calibration(device_id):
        packets.update({
            PID.automatic_magnetometer_calibration_status,
            PID.magnetic_calibration_values,
            PID.magnetic_calibration_configuration,
            PID.magnetic_calibration_status
        })

    if has_networking(device_id):
        packets.update({
            PID.ip_configuration,
            PID.ip_dataports_configuration
        })

    if has_north_seeking(device_id):
        packets.update({
            PID.north_seeking_initialisation_status
        })

    if has_odometer_support(device_id):
        packets.update({
            PID.odometer_state,
            PID.odometer_configuration
        })

    if has_packet_timer_period(device_id):
        packets.update({
            PID.packet_timer_period
        })

    if has_raw_satellite_ephemeris(device_id):
        packets.update({
            PID.raw_satellite_ephemeris
        })

    if has_sensor_ranges(device_id):
        packets.update({
            PID.sensor_ranges
        })

    if has_sensor_temperatures(device_id):
        packets.update({
            PID.sensor_temperatures
        })

    if has_system_temperatures(device_id):
        packets.update({
            PID.system_temperatures
        })

    if has_zero_angular_velocity(device_id):
        packets.update({
            PID.zero_angular_velocity
        })


    return sorted(list(packets))
