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

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
import struct
from typing import Dict
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


class FunctionType(Enum):
    # Name                (GPIO1, GPIO2, AUX_TX, AUX_RX)
    TRISTATE            = (True,  True,  True,  True)
    DIGITAL_OUTPUT      = (True,  True,  True,  False)
    DIGITAL_OUTPUT_ONLY = (True,  False, True,  False)
    DIGITAL_INPUT       = (True,  True,  False, True)
    ENCODER_INPUT       = (True,  True,  False, False)
    FREQUENCY_INPUT     = (True,  True,  False, True)
    GPIO2_ONLY          = (False, True,  False, False)
    SERIAL_RECEIVE      = (False, True,  False, True)
    SERIAL_TRANSMIT     = (True,  False, True,  False)
    SERIAL              = (True,  True,  True,  True)

    def __init__(self, gpio1, gpio2, aux_tx, aux_rx):
        self.gpio1 = gpio1
        self.gpio2 = gpio2
        self.aux_tx = aux_tx
        self.aux_rx = aux_rx


class FunctionId(IntEnum):
    """GPIO Function"""

    inactive = 0
    pps_output = 1
    gnss_fix_output = 2
    odometer_input = 3
    zero_velocity_input = 4
    pitot_tube_input = 5
    nmea_input = 6
    nmea_output = 7
    novatel_gnss_input = 8
    topcon_gnss_input = 9
    anpp_input = 11
    anpp_output = 12
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
    tss1_output = 39
    simrad_1000_output = 40
    simrad_3000_output = 41
    serial_port_passthrough = 42
    gimbal_encoder_phase_a = 43
    gimbal_encoder_phase_b = 44
    odometer_direction_forward_low = 45
    odometer_direction_forward_high = 46
    nortek_dvl_input = 51
    moving_base_corrections_output = 52
    reverse_alignment_forward_low = 53
    reverse_alignment_forward_high = 54
    zero_angular_velocity_input = 55
    mavlink_output = 56
    gnss_receiver_2_passthrough = 57
    water_linked_dvl_input = 59
    system_state_sync_output = 62
    nortek_nucleus_dvl_input = 63
    nortek_nucleus_dvl_output = 64
    valeport_svs_input = 65
    septentrio_gnss_input = 66
    lvs_input = 67
    lvs_output = 68


@dataclass(frozen=True)
class GPIOFunction:
    value: FunctionId
    func_type: FunctionType

    @property
    def name(self) -> str:
        return self.value.name

    def supports_gpio(self, gpio_index: GPIOIndex) -> bool:
        match gpio_index:
            case GPIOIndex.gpio1:
                return self.func_type.gpio1
            case GPIOIndex.gpio2:
                return self.func_type.gpio2
            case GPIOIndex.auxiliary_tx:
                return self.func_type.aux_tx
            case GPIOIndex.auxiliary_rx:
                return self.func_type.aux_rx
        return False

    @staticmethod
    def from_id(id_input: int | FunctionId) -> GPIOFunction:
        if isinstance(id_input, FunctionId):
            return BY_ENUM.get(id_input, GPIO_FUNCTIONS[0])
        return BY_ID.get(id_input, GPIO_FUNCTIONS[0])


GPIO_FUNCTIONS = [
    GPIOFunction(FunctionId.inactive,                           FunctionType.TRISTATE),
    GPIOFunction(FunctionId.pps_output,                         FunctionType.DIGITAL_OUTPUT),
    GPIOFunction(FunctionId.gnss_fix_output,                    FunctionType.DIGITAL_OUTPUT),
    GPIOFunction(FunctionId.odometer_input,                     FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.zero_velocity_input,                FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.pitot_tube_input,                   FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.nmea_input,                         FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.nmea_output,                        FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.novatel_gnss_input,                 FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.topcon_gnss_input,                  FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.anpp_input,                         FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.anpp_output,                        FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.disable_magnetometers,              FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.disable_gnss,                       FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.disable_pressure,                   FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.set_zero_alignment,                 FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.system_state_packet_trigger,        FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.raw_sensors_packet_trigger,         FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.rtcm_corrections_input,             FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.trimble_gnss_input,                 FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.ublox_gnss_input,                   FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.hemisphere_gnss_input,              FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.teledyne_dvl_input,                 FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.tritech_usbl_input,                 FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.linkquest_dvl_input,                FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.pressure_depth_sensor,              FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.left_wheel_speed_sensor,            FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.right_wheel_speed_sensor,           FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.pps_input,                          FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.wheel_speed_sensor,                 FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.wheel_encoder_phase_a,              FunctionType.ENCODER_INPUT),
    GPIOFunction(FunctionId.wheel_encoder_phase_b,              FunctionType.ENCODER_INPUT),
    GPIOFunction(FunctionId.event_1_input,                      FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.event_2_input,                      FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.linkquest_usbl_input,               FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.gnss_receiver_passthrough,          FunctionType.SERIAL),
    GPIOFunction(FunctionId.tss1_output,                        FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.simrad_1000_output,                 FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.simrad_3000_output,                 FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.serial_port_passthrough,            FunctionType.SERIAL),
    GPIOFunction(FunctionId.gimbal_encoder_phase_a,             FunctionType.ENCODER_INPUT),
    GPIOFunction(FunctionId.gimbal_encoder_phase_b,             FunctionType.ENCODER_INPUT),
    GPIOFunction(FunctionId.odometer_direction_forward_low,     FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.odometer_direction_forward_high,    FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.nortek_dvl_input,                   FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.moving_base_corrections_output,     FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.reverse_alignment_forward_low,      FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.reverse_alignment_forward_high,     FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.zero_angular_velocity_input,        FunctionType.DIGITAL_INPUT),
    GPIOFunction(FunctionId.mavlink_output,                     FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.gnss_receiver_2_passthrough,        FunctionType.SERIAL),
    GPIOFunction(FunctionId.water_linked_dvl_input,             FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.system_state_sync_output,           FunctionType.DIGITAL_OUTPUT),
    GPIOFunction(FunctionId.nortek_nucleus_dvl_input,           FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.nortek_nucleus_dvl_output,          FunctionType.SERIAL_TRANSMIT),
    GPIOFunction(FunctionId.valeport_svs_input,                 FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.septentrio_gnss_input,              FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.lvs_input,                          FunctionType.SERIAL_RECEIVE),
    GPIOFunction(FunctionId.lvs_output,                         FunctionType.SERIAL_TRANSMIT),
]

BY_ID: Dict[int, GPIOFunction] = {f.value.value: f for f in GPIO_FUNCTIONS}
BY_ENUM = {f.value: f for f in GPIO_FUNCTIONS}


class GPIOIndex(IntEnum):
    """GPIO Index"""

    gpio1 = 0
    gpio2 = 1
    auxiliary_tx = 2
    auxiliary_rx = 3


class GPIOVoltage(IntEnum):
    """GPIO Index"""

    v_5 = 0
    v_3_3 = 1
    power_disabled = 2


@dataclass()
class GPIOConfigurationPacket:
    """Packet 188 - GPIO Configuration Packet"""

    permanent: int = 0
    gpio1_function: GPIOFunction = GPIOFunction.from_id(FunctionId.inactive)
    gpio2_function: GPIOFunction = GPIOFunction.from_id(FunctionId.inactive)
    auxTx_function: GPIOFunction = GPIOFunction.from_id(FunctionId.inactive)
    auxRx_function: GPIOFunction = GPIOFunction.from_id(FunctionId.inactive)
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
            self.gpio1_function = GPIOFunction.from_id(values[1])
            self.gpio2_function = GPIOFunction.from_id(values[2])
            self.auxTx_function = GPIOFunction.from_id(values[3])
            self.auxRx_function = GPIOFunction.from_id(values[4])
            self.gpio_voltage_selection = GPIOVoltage(values[5])
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode GPIO Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.permanent,
            self.gpio1_function.value.value,
            self.gpio2_function.value.value,
            self.auxTx_function.value.value,
            self.auxRx_function.value.value,
            self.gpio_voltage_selection.value,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
