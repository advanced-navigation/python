################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_188.py                              ##
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
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


class GPIO1Function(Enum):
    """GPIO1 Function"""

    inactive = 0
    pps_output = 1
    gnss_fix_output = 2
    odometer_input = 3
    zero_velocity_input = 4
    pitot_tube_input = 5
    nmea_output = 7
    anpp_output = 12
    disable_magnetometers = 13
    disable_gnss = 14
    disable_pressure = 15
    set_zero_alignment = 16
    system_state_packet_trigger = 17
    raw_sensors_packet_trigger = 18
    pressure_depth_sensor = 26
    left_wheel_speed_sensor = 27
    right_wheel_speed_sensor = 28
    pps_input = 29
    wheel_speed_sensor = 30
    wheel_encoder_phase_a = 31
    wheel_encoder_phase_b = 32
    event_1_input = 33
    event_2_input = 34
    gnss_receiver_passthrough = 38
    tss1_output = 39
    simrad_1000_output = 40
    simrad_3000_output = 41
    serial_port_passthrough = 42
    gimbal_encoder_phase_a = 43
    gimbal_encode_phase_b = 44
    odometer_direction_forward_low = 45
    odometer_direction_forward_high = 46
    reverse_alignment_forward_low = 53
    reverse_alignment_forward_high = 54
    zero_angular_velocity_input = 55


class GPIO2Function(Enum):
    """GPIO2 Function"""

    inactive = 0
    pps_output = 1
    gnss_fix_output = 2
    odometer_input = 3
    zero_velocity_input = 4
    pitot_tube_input = 5
    nmea_input = 6
    novatel_gnss_input = 8
    topcon_gnss_input = 9
    anpp_input = 11
    disable_magnetometers = 13
    disable_gnss = 14
    disable_pressure = 15
    set_zero_alignment = 16
    system_state_packet_trigger = 17
    raw_sensors_packet_trigger = 18
    rtcm_corrections_input = 19
    trimble_gnss_input = 20
    ublox_gnss_input = 21
    hemisphere_gnss_input = 22
    teledyne_dvl_input = 23
    tritech_usbl_input = 24
    linkquest_dvl_input = 25
    pressure_depth_sensor = 26
    left_wheel_speed_sensor = 27
    right_wheel_speed_sensor = 28
    pps_input = 29
    wheel_speed_sensor = 30
    wheel_encoder_phase_a = 31
    wheel_encoder_phase_b = 32
    event_1_input = 33
    event_2_input = 34
    linkquest_usbl_input = 35
    gnss_receiver_passthrough = 38
    serial_port_passthrough = 42
    gimbal_encoder_phase_a = 43
    gimbal_encode_phase_b = 44
    odometer_direction_forward_low = 45
    odometer_direction_forward_high = 46
    nortek_dvl_input = 51
    reverse_alignment_forward_low = 53
    reverse_alignment_forward_high = 54
    zero_angular_velocity_input = 55


class AuxiliaryTxFunction(Enum):
    """Auxiliary Tx Function"""

    inactive = 0
    pps_output = 1
    gnss_fix_output = 2
    nmea_output = 7
    anpp_output = 12
    gnss_receiver_passthrough = 38
    tss1_output = 39
    simrad_1000_output = 40
    simrad_3000_output = 41
    serial_port_passthrough = 42


class AuxiliaryRxFunction(Enum):
    """Auxiliary Rx Function"""

    inactive = 0
    odometer_input = 3
    zero_velocity_input = 4
    pitot_tube_input = 5
    nmea_input = 6
    novatel_gnss_input = 8
    topcon_gnss_input = 9
    anpp_input = 11
    disable_magnetometers = 13
    disable_gnss = 14
    disable_pressure = 15
    set_zero_alignment = 16
    system_state_packet_trigger = 17
    raw_sensors_packet_trigger = 18
    rtcm_corrections_input = 19
    trimble_gnss_input = 20
    ublox_gnss_input = 21
    hemisphere_gnss_input = 22
    teledyne_dvl_input = 23
    tritech_usbl_input = 24
    linkquest_dvl_input = 25
    pressure_depth_sensor = 26
    left_wheel_speed_sensor = 27
    right_wheel_speed_sensor = 28
    pps_input = 29
    wheel_speed_sensor = 30
    event_1_input = 33
    event_2_input = 34
    linkquest_usbl_input = 35
    gnss_receiver_passthrough = 38
    serial_port_passthrough = 42
    odometer_direction_forward_low = 45
    odometer_direction_forward_high = 46
    nortek_dvl_input = 51
    reverse_alignment_forward_low = 53
    reverse_alignment_forward_high = 54
    zero_angular_velocity_input = 55


class GPIOIndex(Enum):
    """GPIO Index"""

    gpio1 = 0
    gpio2 = 1
    auxiliary_tx = 2
    auxiliary_rx = 3


class GPIOVoltage(Enum):
    """GPIO Index"""

    v_5 = 0
    v_3_3 = 1
    power_disabled = 2


@dataclass()
class GPIOConfigurationPacket:
    """Packet 188 - GPIO Configuration Packet"""

    permanent: int = 0
    gpio1_function: GPIO1Function = GPIO1Function.inactive
    gpio2_function: GPIO2Function = GPIO2Function.inactive
    auxTx_function: AuxiliaryTxFunction = AuxiliaryTxFunction.inactive
    auxRx_function: AuxiliaryRxFunction = AuxiliaryRxFunction.inactive
    gpio_voltage_selection: GPIOVoltage = GPIOVoltage.power_disabled

    ID = PacketID.gpio_configuration
    LENGTH = 13

    _structure = struct.Struct("BBBBBB7x")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to GPIO Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            values = self._structure.unpack_from(an_packet.data)
            self.permanent = values[0]
            self.gpio1_function = GPIO1Function(values[1])
            self.gpio2_function = GPIO2Function(values[2])
            self.auxTx_function = AuxiliaryTxFunction(values[3])
            self.auxRx_function = AuxiliaryRxFunction(values[4])
            self.gpio_voltage_selection = GPIOVoltage(values[5])
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode GPIO Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.gpio1_function.value,
            self.gpio2_function.value,
            self.auxTx_function.value,
            self.auxRx_function.value,
            self.gpio_voltage_selection.value,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
