################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                                an_packets.py                               ##
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

from enum import IntEnum


class PacketID(IntEnum):
    """Advanced Navigation Packet Protocol IDs"""

    # System Packet IDs
    acknowledge = 0
    request = 1
    boot_mode = 2
    device_information = 3
    restore_factory_settings = 4
    reset = 5
    file_transfer_request = 7
    file_transfer_acknowledge = 8
    file_transfer = 9
    serial_port_passthrough = 10
    ip_configuration = 11
    extended_device_information = 13
    subcomponent_information = 14
    # State Packet IDs
    system_state = 20
    unix_time = 21
    formatted_time = 22
    status = 23
    position_standard_deviation = 24
    velocity_standard_deviation = 25
    euler_orientation_standard_deviation = 26
    quaternion_orientation_standard_deviation = 27
    raw_sensors = 28
    raw_gnss = 29
    satellites = 30
    detailed_satellites = 31
    geodetic_position = 32
    ecef_position = 33
    utm_position = 34
    ned_velocity = 35
    body_velocity = 36
    acceleration = 37
    body_acceleration = 38
    euler_orientation = 39
    quaternion_orientation = 40
    dcm_orientation = 41
    angular_velocity = 42
    angular_acceleration = 43
    external_position_velocity = 44
    external_position = 45
    external_velocity = 46
    external_body_velocity = 47
    external_heading = 48
    running_time = 49
    local_magnetic_field = 50
    odometer_state = 51
    external_time = 52
    external_depth = 53
    geoid_height = 54
    rtcm_corrections = 55
    wind = 57
    heave = 58
    raw_satellite_data = 60
    raw_satellite_ephemeris = 61
    external_odometer = 67
    external_air_data = 68
    gnss_receiver_information = 69
    raw_dvl_data = 70
    north_seeking_initialisation_status = 71
    gimbal_state = 72
    automotive = 73
    external_magnetometers = 75
    base_station = 80
    zero_angular_velocity = 83
    extended_satellites = 84
    sensor_temperatures = 85
    # Configuration Packet IDs
    packet_timer_period = 180
    packets_period = 181
    baud_rates = 182
    sensor_ranges = 184
    installation_alignment = 185
    filter_options = 186
    gpio_configuration = 188
    magnetic_calibration_values = 189
    magnetic_calibration_configuration = 190
    magnetic_calibration_status = 191
    odometer_configuration = 192
    set_zero_orientation_alignment = 193
    reference_point_offsets = 194
    gpio_output_configuration = 195
    dual_antenna_configuration = 196
    gnss_configuration = 197
    user_data = 198
    gpio_input_configuration = 199
    ip_dataports_configuration = 202
    can_configuration = 203
