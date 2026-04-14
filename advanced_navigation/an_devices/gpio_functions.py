################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              gpio_functions.py                             ##
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
from ..anpp_packets.an_packet_3 import DeviceID
from ..anpp_packets.an_packet_188 import FunctionId, GPIOFunction, GPIOIndex
from .device_capabilities import (
    is_boreas,
    is_certus_mini,
    is_ins,
    is_orientus,
    has_internal_gnss,
    has_magnetometer,
    has_pressure
)

def get_gpio_functions(device_id: DeviceID, gpio_index: GPIOIndex | None = None) -> List[GPIOFunction]:
    """Get a list of GPIO functions supported by the device"""

    function_ids = [
        FunctionId.inactive,
        FunctionId.nmea_input,
        FunctionId.nmea_output,
        FunctionId.anpp_input,
        FunctionId.anpp_output,
        FunctionId.simrad_1000_output
    ]

    if is_ins(device_id) and device_id != DeviceID.gnss_compass:
        function_ids.append(FunctionId.pps_output)
        function_ids.append(FunctionId.gnss_fix_output)
        function_ids.append(FunctionId.odometer_input)
        function_ids.append(FunctionId.zero_velocity_input)
        function_ids.append(FunctionId.pitot_tube_input)
        function_ids.append(FunctionId.novatel_gnss_input)
        function_ids.append(FunctionId.teledyne_dvl_input)
        function_ids.append(FunctionId.tritech_usbl_input)
        function_ids.append(FunctionId.linkquest_dvl_input)
        function_ids.append(FunctionId.pressure_depth_sensor)
        function_ids.append(FunctionId.left_wheel_speed_sensor)
        function_ids.append(FunctionId.right_wheel_speed_sensor)
        function_ids.append(FunctionId.pps_input)
        function_ids.append(FunctionId.wheel_speed_sensor)
        function_ids.append(FunctionId.wheel_encoder_phase_a)
        function_ids.append(FunctionId.wheel_encoder_phase_b)
        function_ids.append(FunctionId.event_1_input)
        function_ids.append(FunctionId.event_2_input)
        function_ids.append(FunctionId.linkquest_usbl_input)
        function_ids.append(FunctionId.serial_port_passthrough)
        function_ids.append(FunctionId.gimbal_encoder_phase_a)
        function_ids.append(FunctionId.gimbal_encoder_phase_b)
        function_ids.append(FunctionId.odometer_direction_forward_low)
        function_ids.append(FunctionId.odometer_direction_forward_high)
        function_ids.append(FunctionId.nortek_dvl_input)
        function_ids.append(FunctionId.reverse_alignment_forward_low)
        function_ids.append(FunctionId.reverse_alignment_forward_high)
        function_ids.append(FunctionId.zero_angular_velocity_input)
        function_ids.append(FunctionId.water_linked_dvl_input)
        function_ids.append(FunctionId.nortek_nucleus_dvl_input)
        function_ids.append(FunctionId.nortek_nucleus_dvl_output)

    if device_id != DeviceID.gnss_compass:
        function_ids.append(FunctionId.topcon_gnss_input)
        function_ids.append(FunctionId.set_zero_alignment)
        function_ids.append(FunctionId.system_state_packet_trigger)
        function_ids.append(FunctionId.raw_sensors_packet_trigger)
        function_ids.append(FunctionId.trimble_gnss_input)
        function_ids.append(FunctionId.ublox_gnss_input)
        function_ids.append(FunctionId.hemisphere_gnss_input)
        function_ids.append(FunctionId.tss1_output)
        function_ids.append(FunctionId.simrad_3000_output)

    if has_magnetometer(device_id):
        function_ids.append(FunctionId.disable_magnetometers)

    if has_internal_gnss(device_id) and device_id != DeviceID.gnss_compass:
        function_ids.append(FunctionId.disable_gnss)
        function_ids.append(FunctionId.rtcm_corrections_input)

    if has_pressure(device_id):
        function_ids.append(FunctionId.disable_pressure)

    if has_internal_gnss(device_id) and not is_certus_mini(device_id):
        function_ids.append(FunctionId.gnss_receiver_passthrough)

    if device_id in (DeviceID.spatial_dual, DeviceID.spatial_fog):
        function_ids.append(FunctionId.moving_base_corrections_output)

    if device_id in (DeviceID.spatial, DeviceID.spatial_dual, DeviceID.spatial_fog, \
                     DeviceID.spatial_fog_dual):
        function_ids.append(FunctionId.mavlink_output)

    if (is_boreas(device_id) and has_internal_gnss(device_id)) \
        or device_id == DeviceID.certus or device_id == DeviceID.gnss_compass:
        function_ids.append(FunctionId.gnss_receiver_2_passthrough)

    if is_orientus(device_id) \
        or device_id in (DeviceID.motus, DeviceID.spatial, DeviceID.spatial_dual, \
                         DeviceID.spatial_fog, DeviceID.spatial_fog_dual):
        function_ids.append(FunctionId.system_state_sync_output)

    if is_ins(device_id) and device_id not in (DeviceID.gnss_compass, DeviceID.spatial_fog, DeviceID.spatial_fog_dual):
        function_ids.append(FunctionId.valeport_svs_input)
        function_ids.append(FunctionId.septentrio_gnss_input)
        function_ids.append(FunctionId.lvs_input)
        function_ids.append(FunctionId.lvs_output)


    supported_functions = [GPIOFunction.from_id(f_id) for f_id in function_ids]

    if gpio_index is not None: 
        return [f for f in supported_functions if f is not None and f.supports_gpio(gpio_index)]

    return [f for f in supported_functions if f is not None]
