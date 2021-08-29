################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               anpp_packets.py                              ##
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

""" ANPP Packets as defined in Advance Navigation Reference Manuals

    Decode functions take an an_packet and turn it into a specific packet type
    so the fields can be conveniently accessed. Decode functions return 0 for
    success and 1 for failure. Decode functions are used when receiving packets.

    Encode functions take a specific packet type and turn it into an an_packet.
    Encode functions are used when sending packets.
"""

from enum import Enum
from struct import pack, unpack
from dataclasses import dataclass, field
from ctypes.wintypes import DOUBLE
from anpp_packets.packets.an_packet_protocol import AN_Packet

MAXIMUM_PACKET_PERIODS = 50
MAXIMUM_DETAILED_SATELLITES = 32

class PacketID():
    class PacketID(Enum):
        # System Packet IDs
        acknowledge = 0
        request = 1
        boot_mode = 2
        device_information = 3
        restore_factory_settings = 4
        reset = 5
        print_ = 6
        file_transfer_request = 7
        file_transfer_acknowledge = 8
        file_transfer = 9
        serial_port_passthrough = 10
        ip_configuration = 11
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
        depth = 62
        water_profiling = 63
        external_usbl = 64
        speed_of_sound = 65
        lockheed = 66
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
        bus_configuration = 183
        sensor_ranges = 184
        installation_alignment = 185
        filter_options = 186
        advanced_filter_parameters = 187
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


########## System Packets ##########
class BootMode():
    class BootMode(Enum):
        bootloader = 0
        main_program = 1

class BootModePacket():
    @dataclass()
    class BootModePacket:
        boot_mode: int = 0

        def decode(self, an_packet: AN_Packet):
            if ((an_packet.id == PacketID.PacketID.boot_mode.value) and (len(an_packet.data) == 1)):
                self.boot_mode = an_packet.data[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<B', self.boot_mode)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.boot_mode.value, 1, data)

            return an_packet


class DeviceInformationPacket():
    @dataclass()
    class DeviceInformationPacket:
        software_version: int = 0
        device_id: int = 0
        hardware_revision: int = 0
        serial_number: [int, int, int] = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.device_information.value) and (len(an_packet.data) == 24)):
                self.software_version = unpack('<I', an_packet.data[0:4])[0]
                self.device_id = unpack('<I', an_packet.data[4:8])[0]
                self.hardware_revision = unpack('<I', an_packet.data[8:12])[0]
                self.serial_number = unpack('<III', an_packet.data[12:24])
                return 0
            else:
                return 1


class RestoreFactorySettingsPacket():
    @dataclass()
    class RestoreFactorySettingsPacket:
        verification = 0x85429E1C

        def encode(self):
            data = pack('<I', self.verification)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.restore_factory_settings.value, 4, data)

            return an_packet


class ResetVerification():
    class ResetVerification(Enum):
        hot_start = 0x21057A7E
        cold_start = 0x9A5D38B7

class ResetPacket():
    @dataclass()
    class ResetPacket:
        verification: ResetVerification.ResetVerification = ResetVerification.ResetVerification.hot_start

        def encode(self, verification: ResetVerification.ResetVerification):
            data = pack('<I', verification)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.reset.value, 4, data)

            return an_packet


class DataEncoding():
    class DataEncoding(Enum):
        binary = 0
        aes256  = 1

class FileTransferResponse():
    class FileTransferResponse(Enum):
        completed_successfully = 0
        ready = 1
        index_mismatch = 2
        refused = 64
        bad_metadata = 65
        timeout = 66
        retry_error = 67
        storage_error = 68
        data_invalid = 69
        packet_length_invalid = 70
        total_size_invalid = 71
        overflow_error = 72
        busy = 73
        cancelled = 74
        file_not_found = 128
        access_denied = 129

class FileTransferMetadata():    
    class FileTransferMetadata(Enum):
        none = 0
        extended_anpp = 1
        utf8_filename = 2
        an_firmware = 3

class FileTransferAcknowledgePacket():
    @dataclass()
    class FileTransferAcknowledgePacket:
        unique_id: int = 0
        data_index: int = 0
        response_code: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.file_transfer_acknowledge.value) and (len(an_packet.data) == 9)):
                self.unique_id = unpack('<I', an_packet.data[0:4])
                self.data_index = unpack('<I', an_packet.data[4:8])
                self.response_code = an_packet.data[8]
                return 0
            else:
                return 1


class FileTransferFirstPacket():
    @dataclass()
    class FileTransferFirstPacket:
        unique_id: int = 0
        data_index: int = 0
        total_size: int = 0
        data_encoding: int = 0
        metadata_type: int = 0
        metadata: int = 0
        packet_data: int = 0


class FileTransferOngoingPacket():
    @dataclass()
    class FileTransferOngoingPacket:
        unique_id: int = 0
        data_index: int = 0
        packet_data: int = 0


class LinkMode():
    class LinkMode(Enum):
        auto = 0
        full_duplex_100mb = 1
        half_duplex_100mb = 2
        full_duplex_10mb = 3
        half_duplex_10mb = 4

class DHCPMode():
    @dataclass()
    class DHCPMode:
        dhcp_enabled: bool = False
        automatic_dns: bool = False
        link_mode: int = 0
        reserved: int = 0 # Reserved (set to zero)

        def unpack(self, data):
            self.dhcp_enabled =  ((data & 0b0000000000000001) == 0b0000000000000001)
            self.automatic_dns = ((data & 0b0000000000000010) == 0b0000000000000010)
            self.link_mode =     ((data & 0b0000000000000100) >> 2)
            self.link_mode +=    ((data & 0b0000000000001000) >> 2)
            self.link_mode +=    ((data & 0b0000000000010000) >> 2)

class IPConfigurationPacket():
    @dataclass()
    class IPConfigurationPacket:
        permanent: int = 0
        dhcp_mode: DHCPMode = DHCPMode()
        ip_address: int = 0
        ip_netmask: int = 0
        ip_gateway: int = 0
        dns_server: int = 0
        serial_number: [int, int, int] = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.ip_configuration.value) and (len(an_packet.data) == 30)):
                self.permanent = an_packet.data[0]
                self.dhcp_mode.unpack(an_packet.data[1])
                self.ip_address = unpack('<I', bytes(an_packet.data[2:6]))[0]
                self.ip_netmask = unpack('<I', bytes(an_packet.data[6:10]))[0]
                self.ip_gateway = unpack('<I', bytes(an_packet.data[10:14]))[0]
                self.dns_server = unpack('<I', bytes(an_packet.data[14:18]))[0]
                self.serial_number = unpack('<III', bytes(an_packet.data[18:30]))
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<BBIIIIIII', self.permanent, self.dhcp_mode, self.ip_address,
                        self.ip_netmask, self.ip_gateway, self.dns_server, self.serial_number)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.ip_configuration.value, 30, data)

            return an_packet


########## State Packets ##########
class GNSSFixType():
    class GNSSFixType(Enum):
        none = 0
        twoD = 1
        threeD = 2
        sbas = 3
        differential = 4
        omnistar = 5
        rtk_float = 6
        rtk_fixed = 7

class SystemStatus():
    @dataclass()
    class SystemStatus:
        system_failure: bool = False
        accelerometer_sensor_failure: bool = False
        gyroscope_sensor_failure: bool = False
        magnetometer_sensor_failure: bool = False
        pressure_sensor_failure: bool = False
        gnss_failure: bool = False
        accelerometer_over_range: bool = False
        gyroscope_over_range: bool = False
        magnetometer_over_range: bool = False
        pressure_over_range: bool = False
        minimum_temperature_alarm: bool = False
        maximum_temperature_alarm: bool = False
        low_voltage_alarm: bool = False
        high_voltage_alarm: bool = False
        gnss_antenna_disconnected: bool = False
        data_output_overflow_alarm: bool = False

        def unpack(self, data):
            self.system_failure =               ((data & 0b0000000000000001) == 0b0000000000000001)
            self.accelerometer_sensor_failure = ((data & 0b0000000000000010) == 0b0000000000000010)
            self.gyroscope_sensor_failure =     ((data & 0b0000000000000100) == 0b0000000000000100)
            self.magnetometer_sensor_failure =  ((data & 0b0000000000001000) == 0b0000000000001000)
            self.pressure_sensor_failure =      ((data & 0b0000000000010000) == 0b0000000000010000)
            self.gnss_failure =                 ((data & 0b0000000000100000) == 0b0000000000100000)
            self.accelerometer_over_range =     ((data & 0b0000000001000000) == 0b0000000001000000)
            self.gyroscope_over_range =         ((data & 0b0000000010000000) == 0b0000000010000000)
            self.magnetometer_over_range =      ((data & 0b0000000100000000) == 0b0000000100000000)
            self.pressure_over_range =          ((data & 0b0000001000000000) == 0b0000001000000000)
            self.minimum_temperature_alarm =    ((data & 0b0000010000000000) == 0b0000010000000000)
            self.maximum_temperature_alarm =    ((data & 0b0000100000000000) == 0b0000100000000000)
            self.low_voltage_alarm =            ((data & 0b0001000000000000) == 0b0001000000000000)
            self.high_voltage_alarm =           ((data & 0b0010000000000000) == 0b0010000000000000)
            self.gnss_antenna_disconnected =    ((data & 0b0100000000000000) == 0b0100000000000000)
            self.data_output_overflow_alarm =   ((data & 0b1000000000000000) == 0b1000000000000000)

class FilterStatus():
    @dataclass()
    class FilterStatus:
        orientation_filter_initialised: bool = False
        ins_filter_initialised: bool = False
        heading_initialised: bool = False
        utc_time_initialised: bool = False
        gnss_fix_type: int = 0
        event1_flag: bool = False
        event2_flag: bool = False
        internal_gnss_enabled: bool = False
        magnetic_heading_enabled: bool = False
        velocity_heading_enabled: bool = False
        atmospheric_altitude_enabled: bool = False
        external_position_active: bool = False
        external_velocity_active: bool = False
        external_heading_active: bool = False

        def unpack(self, data):
            self.orientation_filter_initialised = ((data & 0b0000000000000001) == 0b0000000000000001)
            self.navigation_filter_initialised =  ((data & 0b0000000000000010) == 0b0000000000000010)
            self.heading_initialised =            ((data & 0b0000000000000100) == 0b0000000000000100)
            self.utc_time_initialised =           ((data & 0b0000000000001000) == 0b0000000000001000)
            self.gnss_fix_type =                  ((data & 0b0000000000010000) >> 4)
            self.gnss_fix_type +=                 ((data & 0b0000000000100000) >> 4)
            self.gnss_fix_type +=                 ((data & 0b0000000001000000) >> 4)
            self.event1_occurred =                ((data & 0b0000000010000000) == 0b0000000010000000)
            self.event2_occurred =                ((data & 0b0000000100000000) == 0b0000000100000000)
            self.internal_gnss_enabled =          ((data & 0b0000001000000000) == 0b0000001000000000)
            self.magnetic_heading_enabled =       ((data & 0b0000010000000000) == 0b0000010000000000)
            self.velocity_heading_enabled =       ((data & 0b0000100000000000) == 0b0000100000000000)
            self.atmospheric_altitude_enabled =   ((data & 0b0001000000000000) == 0b0001000000000000)
            self.external_position_active =       ((data & 0b0010000000000000) == 0b0010000000000000)
            self.external_velocity_active =       ((data & 0b0100000000000000) == 0b0100000000000000)
            self.external_heading_active =        ((data & 0b1000000000000000) == 0b1000000000000000)

class SystemStatePacket():
    @dataclass()
    class SystemStatePacket:
        system_status: SystemStatus = SystemStatus.SystemStatus()
        filter_status: FilterStatus = FilterStatus.FilterStatus()
        unix_time_seconds: int = 0
        microseconds: int = 0
        latitude: DOUBLE = 0
        longitude: DOUBLE = 0
        height: DOUBLE = 0
        velocity: [float, float, float] = field(default_factory=list)
        body_acceleration: [float, float, float] = field(default_factory=list)
        g_force: float = field(default_factory=list)
        orientation: [float, float, float] = field(default_factory=list)
        angular_velocity: [float, float, float] = field(default_factory=list)
        standard_deviation: [float, float, float] = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.system_state.value) and (len(an_packet.data) == 100)):
                self.system_status.unpack(unpack('<H', bytes(an_packet.data[0:2]))[0])
                self.filter_status.unpack(unpack('<H', bytes(an_packet.data[2:4]))[0])
                self.unix_time_seconds = unpack('<I', bytes(an_packet.data[4:8]))[0]
                self.microseconds = unpack('<I', bytes(an_packet.data[8:12]))[0]
                self.latitude = unpack('<d', bytes(an_packet.data[12:20]))[0]
                self.longitude = unpack('<d', bytes(an_packet.data[20:28]))[0]
                self.height = unpack('<d', bytes(an_packet.data[28:36]))[0]
                self.velocity = unpack('<fff', bytes(an_packet.data[36:48]))
                self.body_acceleration = unpack('<fff', bytes(an_packet.data[48:60]))  
                self.g_force = unpack('<f', bytes(an_packet.data[60:64]))[0]
                self.orientation = unpack('<fff', bytes(an_packet.data[64:76]))
                self.angular_velocity = unpack('<fff', bytes(an_packet.data[76:88]))
                self.standard_deviation = unpack('<fff', bytes(an_packet.data[88:100]))
                return 0
            else:
                return 1


class UnixTimePacket():
    @dataclass()
    class UnixTimePacket:
        unix_time_seconds: int = 0
        microseconds: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.unix_time.value) and (len(an_packet.data) == 8)):
                self.unix_time_seconds = unpack('<I', an_packet.data[0:4])
                self.microseconds = unpack('<I', an_packet.data[4:8])
                return 0
            else:
                return 1


class FormattedTimePacket():
    @dataclass()
    class FormattedTimePacket:
        microseconds: int = 0
        year: int = 0
        year_day: int = 0
        month: int = 0
        month_day: int = 0
        week_day: int = 0
        hour: int = 0
        minute: int = 0
        second: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.formatted_time.value) and (len(an_packet.data) == 14)):
                self.microseconds = unpack('<I', an_packet.data[0:4])
                self.year = unpack('<H', an_packet.data[4:6])
                self.year_day = unpack('<H', an_packet.data[6:8])
                self.month = an_packet[8]
                self.month_day = an_packet[9]
                self.week_day = an_packet[10]
                self.hour = an_packet[11]
                self.minute = an_packet[12]
                self.second = an_packet[13]
                return 0
            else:
                return 1

class StatusPacket():
    @dataclass()
    class StatusPacket:
        system_status: SystemStatus = SystemStatus()
        filter_status: FilterStatus = FilterStatus()

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.status.value) and (len(an_packet.data) == 4)):
                self.system_status.unpack(unpack('<H', bytes(an_packet.data[0:2]))[0])
                self.filter_status.unpack(unpack('<H', bytes(an_packet.data[2:4]))[0])
                return 0
            else:
                return 1


class PositionStandardDeviationPacket():
    @dataclass()
    class PositionStandardDeviationPacket:
        standard_deviation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.position_standard_deviation.value) and (len(an_packet.data) == 12)):
                self.standard_deviation = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1

class VelocityStandardDeviationPacket():
    @dataclass()
    class VelocityStandardDeviationPacket:
        standard_deviation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.velocity_standard_deviation.value) and (len(an_packet.data) == 12)):
                self.standard_deviation = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1

class EulerOrientationStandardDeviationPacket():
    @dataclass()
    class EulerOrientationStandardDeviationPacket:
        standard_deviation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.euler_orientation_standard_deviation.value) and (len(an_packet.data) == 12)):
                self.standard_deviation = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class QuaternionOrientationStandardDeviationPacket():
    @dataclass()
    class QuaternionOrientationStandardDeviationPacket:
        standard_deviation: [float]*4 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.quaternion_orientation_standard_deviation.value) and (len(an_packet.data) == 16)):
                self.standard_deviation = unpack('<ffff', bytes(an_packet.data[0:16]))
                return 0
            else:
                return 1


class RawSensorsPacket():
    @dataclass()
    class RawSensorsPacket:
        accelerometers: [float]*3 = field(default_factory=list)
        gyroscopes: [float]*3 = field(default_factory=list)
        magnetometers: [float]*3 = field(default_factory=list)
        imu_temperature: float = 0
        pressure: float = 0
        pressure_temperature: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.raw_sensors.value) and (len(an_packet.data) == 48)):
                self.accelerometers = unpack('<fff', bytes(an_packet.data[0:12]))
                self.gyroscopes = unpack('<fff', bytes(an_packet.data[12:24]))
                self.magnetometers = unpack('<fff', bytes(an_packet.data[24:36]))
                self.imu_temperature = unpack('<f', bytes(an_packet.data[36:40]))[0]
                self.pressure = unpack('<f', bytes(an_packet.data[40:44]))[0]
                self.pressure_temperature = unpack('<f', bytes(an_packet.data[44:48]))[0]
                return 0
            else:
                return 1

class RawSensorStatusAdu():
    @dataclass()
    class RawSensorStatus:
        absolute_pressure_valid: bool = False
        differential_pressure_valie: bool = False
        absolute_pressure_sensor_overrange: bool = False
        differential_pressure_sensor_overrange: bool = False
        absolute_pressure_sensor_failure: bool = False
        differential_pressure_sensor_failure: bool = False
        temperature_sensor_valid: bool = False
        temperature_sensor_failure: bool = False

        def unpack(self, data):
            self.absolute_pressure_valid                = ((data & 0b00000001) == 0b00000001)
            self.differential_pressure_valid            = ((data & 0b00000010) == 0b00000010)
            self.absolute_pressure_sensor_overrange     = ((data & 0b00000100) == 0b00000100)
            self.differential_pressure_sensor_overrange = ((data & 0b00001000) == 0b00001000)
            self.absolute_pressure_sensor_failure       = ((data & 0b00010000) == 0b00010000)
            self.differential_pressure_sensor_failure   = ((data & 0b00100000) == 0b00100000)
            self.temperature_sensor_valid               = ((data & 0b01000000) == 0b01000000)
            self.temperature_sensor_failure             = ((data & 0b10000000) == 0b10000000)

class RawSensorsPacketAdu():
    @dataclass()
    class RawSensorsPacket:
        absolute_pressure: float = 0
        differential_pressure: float = 0
        raw_sensors_status: RawSensorStatusAdu.RawSensorStatus = RawSensorStatusAdu.RawSensorStatus()
        temperature: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.raw_sensors.value) and (len(an_packet.data) == 13)):
                self.absolute_pressure = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.differential_pressure = unpack('<f', bytes(an_packet.data[4:8]))[0]
                self.raw_sensors_status.unpack(an_packet.data[8])
                self.temperature = unpack('<f', bytes(an_packet.data[9:13]))[0]
                return 0
            else:
                return 1


class RawGNSSFlags():
    @dataclass()
    class RawGNSSFlags:
        fix_type: int = 0
        doppler_velocity_valid: bool = False
        time_valid: bool = False
        external_gnss: bool = False
        tilt_valid: bool = False # This field will only be valid if an external dual antenna GNSS system is connected
        heading_valid: bool = False # This field will only be valid if an external dual antenna GNSS system is connected
        floating_ambiguity_heading: bool = False
        antenna_1_disconnected: bool = False
        antenna_2_disconnected: bool = False
        antenna_1_short: bool = False
        antenna_2_short: bool = False
        gnns_1_failure: bool = False
        gnns_2_failure: bool = False

        def unpack(self, flagsByte):
            self.fix_type                    = (flagsByte & 0b0000000000000001)
            self.fix_type                   += (flagsByte & 0b0000000000000010)
            self.fix_type                   += (flagsByte & 0b0000000000000100)
            self.doppler_velocity_valid     = ((flagsByte & 0b0000000000001000) == 0b0000000000001000)
            self.time_valid                 = ((flagsByte & 0b0000000000010000) == 0b0000000000010000)
            self.external_gnss              = ((flagsByte & 0b0000000000100000) == 0b0000000000100000)
            self.tilt_valid                 = ((flagsByte & 0b0000000001000000) == 0b0000000001000000)
            self.heading_valid              = ((flagsByte & 0b0000000010000000) == 0b0000000010000000)
            self.floating_ambiguity_heading = ((flagsByte & 0b0000000100000000) == 0b0000000100000000)
            # Bit 9 Reserved (set to zero)
            self.antenna_1_disconnected     = ((flagsByte & 0b0000010000000000) == 0b0000010000000000)
            self.antenna_2_disconnected     = ((flagsByte & 0b0000100000000000) == 0b0000100000000000)
            self.antenna_1_short            = ((flagsByte & 0b0001000000000000) == 0b0001000000000000)
            self.antenna_2_short            = ((flagsByte & 0b0010000000000000) == 0b0010000000000000)
            self.gnns_1_failure             = ((flagsByte & 0b0100000000000000) == 0b0100000000000000)
            self.gnns_2_failure             = ((flagsByte & 0b1000000000000000) == 0b1000000000000000)

class RawGNSSPacket():
    @dataclass()
    class RawGNSSPacket:
        unix_time_seconds: int = 0
        microseconds: int = 0
        position: [DOUBLE]*3 = field(default_factory=list)
        velocity: [float]*3 = field(default_factory=list)
        position_standard_deviation: [float]*3 = field(default_factory=list)
        tilt: float = 0 # This field will only be valid if an external dual antenna GNSS system is connected.
        heading: float = 0 # This field will only be valid if an external dual antenna GNSS system is connected.
        tilt_standard_deviation: float = 0 #This field will only be valid if an external dual antenna GNSS system is connected.
        heading_standard_deviation: float = 0 # This field will only be valid if an external dual antenna GNSS system is connected
        flags: RawGNSSFlags = RawGNSSFlags()

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.raw_gnss.value) and (len(an_packet.data) == 74)):
                self.unix_time_seconds = unpack('<I', bytes(an_packet.data[0:4]))[0]
                self.microseconds = unpack('<I', bytes(an_packet.data[4:8]))[0]
                self.position = unpack('<ddd', bytes(an_packet.data[8:32]))
                self.velocity = unpack('<fff', bytes(an_packet.data[32:44]))
                self.position_standard_deviation = unpack('<fff', bytes(an_packet.data[44:56]))
                self.tilt = unpack('<f', bytes(an_packet.data[56:60]))[0]
                self.heading = unpack('<f', bytes(an_packet.data[60:64]))[0]
                self.tilt_standard_deviation = unpack('<f', bytes(an_packet.data[64:68]))[0]
                self.heading_standard_deviation = unpack('<f', bytes(an_packet.data[68:72]))[0]
                self.flags.unpack(unpack('<H', bytes(an_packet.data[72:74]))[0])
                return 0
            else:
                return 1


class SatellitesPacket():
    @dataclass()
    class SatellitesPacket:
        hdop: float = 0
        vdop: float = 0
        gps_satellites: int = 0
        glonass_satellites: int = 0
        beidou_satellites: int = 0
        galileo_satellites: int = 0
        sbas_satellites: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.satellites.value) and (len(an_packet.data) == 13)):
                self.hdop = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.vdop = unpack('<f', bytes(an_packet.data[4:8]))[0]
                self.gps_satellites = an_packet.data[8]
                self.glonass_satellites = an_packet.data[9]
                self.beidou_satellites = an_packet.data[10]
                self.galileo_satellites = an_packet.data[11]
                self.sbas_satellites = an_packet.data[12]
                return 0
            else:
                return 1


class SatelliteSystem():
    class SatelliteSystem(Enum):
        unknown = 0
        gps = 1
        glonass = 2
        beidou = 3
        galileo = 4
        sbas = 5
        qzss = 6
        starfire = 7
        omnistar = 8

class Frequencies():
    @dataclass()
    class Frequencies:
        l1_ca: bool = False
        l1_c: bool = False
        l1_p: bool = False
        l1_m: bool = False
        l2_c: bool = False
        l2_p: bool = False
        l2_m: bool = False
        l5: bool = False

class Satellite():
    @dataclass()
    class Satellite:
        satellite_system: int = 0
        number: int = 0
        frequencies: Frequencies = 0
        elevation: int = 0
        azimuth: int = 0
        snr: int = 0

class DetailedSatellitesPacket():
    @dataclass()
    class DetailedSatellitesPacket:
        satellites: [Satellite]*MAXIMUM_DETAILED_SATELLITES = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.detailed_satellites.value) and ((len(an_packet.data) % 7) == 0)):
                number_of_satellites = len(an_packet.data) / 7
                self.satellites = [Satellite()]*MAXIMUM_DETAILED_SATELLITES
                for i in range(MAXIMUM_DETAILED_SATELLITES):
                    if(i < number_of_satellites):
                        self.satellites[i].satellite_system = an_packet.date[7*i]
                        self.satellites[i].number = an_packet.date[7*i + 1]
                        self.satellites[i].frequencies = an_packet.date[7*i + 2]
                        self.satellites[i].elevation = an_packet.date[7*i + 3]
                        self.satellites[i].azimuth = unpack('<H', bytes(an_packet.date[(7*i + 4):(7*i + 5)]))[0]
                        self.satellites[i].snr = an_packet.date[7*i + 6]
                    else:
                        self.satellites[i].satellite_system = 0
                        self.satellites[i].number = 0
                        self.satellites[i].frequencies = 0
                        self.satellites[i].elevation = 0
                        self.satellites[i].azimuth = 0
                        self.satellites[i].snr = 0
                return 0
            else:
                return 1


class GeodeticPositionPacket():
    @dataclass()
    class GeodeticPositionPacket:
        position: [DOUBLE]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.geodetic_position.value) and (len(an_packet.data) == 24)):
                self.position = unpack('<ddd', bytes(an_packet.data[0:24]))
                return 0
            else:
                return 1


class ECEFPositionPacket():
    @dataclass()
    class ECEFPositionPacket:
        position: [DOUBLE]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.ecef_position.value) and (len(an_packet.data) == 24)):
                self.position = unpack('<ddd', bytes(an_packet.data[0:24]))
                return 0
            else:
                return 1


class UTMPositionPacket():
    @dataclass()
    class UTMPositionPacket:
        position: [DOUBLE]*3 = field(default_factory=list)
        zone_number: int = 0
        zone_character: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.utm_position.value) and (len(an_packet.data) == 26)):
                self.position = unpack('<ddd', bytes(an_packet.data[0:24]))
                self.zone_number = an_packet.data[24]
                self.zone_character = an_packet.data[25]
                return 0
            else:
                return 1


class NEDVelocityPacket():
    @dataclass()
    class NEDVelocityPacket:
        velocity: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.ned_velocity.value) and (len(an_packet.data) == 12)):
                self.velocity = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class BodyVelocityPacket():
    @dataclass()
    class BodyVelocityPacket:
        velocity: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.body_velocity.value) and (len(an_packet.data) == 12)):
                self.velocity = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class AccelerationPacket():
    @dataclass()
    class AccelerationPacket:
        acceleration: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.acceleration.value) and (len(an_packet.data) == 12)):
                self.acceleration = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class BodyAccelerationPacket():
    @dataclass()
    class BodyAccelerationPacket:
        acceleration: [float]*3 = field(default_factory=list)
        g_force: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.body_acceleration.value) and (len(an_packet.data) == 16)):
                self.acceleration = unpack('<fff', bytes(an_packet.data[0:12]))
                self.g_force = unpack('<f', bytes(an_packet.data[12:16]))[0]
                return 0
            else:
                return 1


class EulerOrientationPacket():
    @dataclass()
    class EulerOrientationPacket:
        orientation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.euler_orientation.value) and (len(an_packet.data) == 12)):
                self.orientation = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class QuaternionOrientationPacket():
    @dataclass()
    class QuaternionOrientationPacket:
        orientation: [float]*4 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.quaternion_orientation.value) and (len(an_packet.data) == 16)):
                self.orientation = unpack('<ffff', bytes(an_packet.data[0:16]))
                return 0
            else:
                return 1


class DCMOrientationPacket():
    @dataclass()
    class DCMOrientationPacket:
        orientation: [[float]*3]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.dcm_orientation.value) and (len(an_packet.data) == 36)):
                self.orientation = [unpack('<fff', bytes(an_packet.data[0:12])), 
                                    unpack('<fff', bytes(an_packet.data[12:24])), 
                                    unpack('<fff', bytes(an_packet.data[24:36]))]
                return 0
            else:
                return 1


class AngularVelocityPacket():
    @dataclass()
    class AngularVelocityPacket:
        angular_velocity: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.angular_velocity.value) and (len(an_packet.data) == 12)):
                self.angular_velocity = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class AngularAccelerationPacket():
    @dataclass()
    class AngularAccelerationPacket:
        angular_acceleration: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.angular_acceleration.value) and (len(an_packet.data) == 12)):
                self.angular_acceleration = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class ExternalPositionVelocityPacket():
    @dataclass()
    class ExternalPositionVelocityPacket:
        position: [DOUBLE]*3 = field(default_factory=list)
        velocity: [float]*3 = field(default_factory=list)
        position_standard_deviation: [float]*3 = field(default_factory=list)
        velocity_standard_deviation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_position_velocity.value) and (len(an_packet.data) == 60)):
                self.position = unpack('<ddd', bytes(an_packet.data[0:24]))
                self.velocity = unpack('<fff', bytes(an_packet.data[24:36]))
                self.position_standard_deviation = unpack('<fff', bytes(an_packet.data[36:48]))
                self.velocity_standard_deviation = unpack('<fff', bytes(an_packet.data[48:60]))            
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<ddd', self.position[0], self.position[1], self.position[2])
            data += pack('<fff', self.velocity[0]. self.velocity[1], self.velocity[2])
            data += pack('<fff', self.position_standard_deviation[0]. self.position_standard_deviation[1], self.position_standard_deviation[2])
            data += pack('<fff', self.velocity_standard_deviation[0]. self.velocity_standard_deviation[1], self.velocity_standard_deviation[2])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_position_velocity.value, 60, data)

            return an_packet


class ExternalPositionPacket():
    @dataclass()
    class ExternalPositionPacket:
        position: [DOUBLE]*3 = field(default_factory=list)
        standard_deviation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_position.value) and (len(an_packet.data) == 36)):
                self.position = unpack('<ddd', bytes(an_packet.data[0:24]))
                self.standard_deviation = unpack('<fff', bytes(an_packet.data[24:36]))
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<ddd', self.position[0], self.position[1], self.position[2])
            data += pack('<fff', self.standard_deviation[0]. self.standard_deviation[1], self.standard_deviation[2])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_position.value, 36, data)

            return an_packet


class ExternalVelocityPacket():
    @dataclass()
    class ExternalVelocityPacket:
        velocity: [float]*3 = field(default_factory=list)
        standard_deviation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_velocity.value) and (len(an_packet.data) == 24)):
                self.velocity = unpack('<fff', bytes(an_packet.data[0:12]))
                self.standard_deviation = unpack('<fff', bytes(an_packet.data[12:24]))
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<fff', self.velocity[0], self.velocity[1], self.velocity[2])
            data += pack('<fff', self.standard_deviation[0]. self.standard_deviation[1], self.standard_deviation[2])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_velocity.value, 24, data)

            return an_packet


class ExternalBodyVelocityPacket():
    @dataclass()
    class ExternalBodyVelocityPacket:
        velocity: [float]*3 = field(default_factory=list)
        standard_deviation: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_body_velocity.value) and (len(an_packet.data) == 16)):
                self.velocity = unpack('<fff', bytes(an_packet.data[0:12]))
                self.standard_deviation = unpack('<f', bytes(an_packet.data[12:16]))[0]
                return 0
            elif((an_packet.id == PacketID.PacketID.external_body_velocity.value) and (len(an_packet.data) == 24)):
                self.velocity = unpack('<fff', bytes(an_packet.data[0:12]))
                self.standard_deviation = unpack('<fff', bytes(an_packet.data[12:24]))
            else:
                return 1

        def encode(self):
            data = pack('<fff', self.velocity[0], self.velocity[1], self.velocity[2])
            data += pack('<fff', self.standard_deviation[0], self.standard_deviation[1], self.standard_deviation[2])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_body_velocity.value, 24, data)

            return an_packet


class ExternalHeadingPacket():
    @dataclass()
    class ExternalHeadingPacket:
        heading: float = 0
        standard_deviation: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_heading.value) and (len(an_packet.data) == 8)):
                self.heading = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.standard_deviation = unpack('<f', bytes(an_packet.data[4:8]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<f', self.heading)
            data += pack('<f', self.standard_deviation)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_heading.value, 8, data)

            return an_packet


class RunningTimePacket():
    @dataclass()
    class RunningTimePacket:
        seconds: int = 0
        microseconds: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.running_time.value) and (len(an_packet.data) == 8)):
                self.seconds = unpack('<I', bytes(an_packet.data[0:4]))[0]
                self.microseconds = unpack('<I', bytes(an_packet.data[4:8]))[0]
                return 0
            else:
                return 1


class LocalMagneticFieldPacket():
    @dataclass()
    class LocalMagneticFieldPacket:
        magnetic_field: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.local_magnetic_field.value) and (len(an_packet.data) == 12)):
                self.magnetic_field = unpack('<fff', bytes(an_packet.data[0:12]))
                return 0
            else:
                return 1


class OdometerStatePacket():
    @dataclass()
    class OdometerStatePacket:
        pulse_count: int = 0
        distance: float = 0
        speed: float = 0
        slip: float = 0
        active: int = 0
        reserved: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.odometer_state.value) and (len(an_packet.data) == 20)):
                self.pulse_count = unpack('<i', bytes(an_packet.data[0:4]))[0]
                self.distance = unpack('<f', bytes(an_packet.data[4:8]))[0]
                self.speed = unpack('<f', bytes(an_packet.data[8:12]))[0]
                self.slip = unpack('<f', bytes(an_packet.data[12:16]))[0]
                self.active = an_packet.data[16]
                return 0
            else:
                return 1


class ExternalTimePacket():
    @dataclass()
    class ExternalTimePacket:
        unix_time_seconds: int = 0
        microseconds: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_time.value) and (len(an_packet.data) == 8)):
                self.unix_time_seconds = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.microseconds = unpack('<f', bytes(an_packet.data[4:8]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<f', self.unix_time_seconds)
            data += pack('<f', self.microseconds)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_time.value, 8, data)

            return an_packet


class ExternalDepthPacket():
    @dataclass()
    class ExternalDepthPacket:
        depth: float = 0
        standard_deviation: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_depth.value) and (len(an_packet.data) == 8)):
                self.depth = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.standard_deviation = unpack('<f', bytes(an_packet.data[4:8]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<f', self.depth)
            data += pack('<f', self.standard_deviation)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_depth.value, 8, data)

            return an_packet


class GeoidHeightPacket():
    @dataclass()
    class GeoidHeightPacket:
        geoid_height: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.geoid_height.value) and (len(an_packet.data) == 4)):
                self.geoid_height = unpack('<f', bytes(an_packet.data[0:4]))[0]
                return 0
            else:
                return 1


class WindPacket():
    @dataclass()
    class WindPacket:
        wind_velocity: [float]*2 = field(default_factory=list)
        wind_standard_deviation: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.wind.value) and (len(an_packet.data) == 12)):
                self.wind_velocity = unpack('<ff', bytes(an_packet.data[0:8]))
                self.wind_standard_deviation = unpack('<f', bytes(an_packet.data[8:12]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<ff', self.wind_velocity[0], self.wind_velocity[1])
            data += pack('<f', self.wind_standard_deviation)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.wind.value, 12, data)

            return an_packet


class HeavePacket():
    @dataclass()
    class HeavePacket:
        heave_point_1: float = 0
        heave_point_2: float = 0
        heave_point_3: float = 0
        heave_point_4: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.heave.value) and (len(an_packet.data) == 16)):
                self.heave_point_1 = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.heave_point_2 = unpack('<f', bytes(an_packet.data[4:8]))[0]
                self.heave_point_3 = unpack('<f', bytes(an_packet.data[8:12]))[0]
                self.heave_point_4 = unpack('<f', bytes(an_packet.data[12:16]))[0]
                return 0
            else:
                return 1


class TrackingStatus():
    @dataclass()
    class TrackingStatus():
        carrier_phase_valid:int = 0
        carrier_phase_cycle_slip_detected:int = 1
        carrier_phase_half_cycle_ambiguity:int = 2
        pseudo_range_valid:int = 3
        doppler_valid:int = 4
        snr_valid:int = 5
        reserved:int = 0

        def unpack(self, data):
            self.carrier_phase_valid                = ((data & 0b0000000000000001) == 0b0000000000000001)
            self.carrier_phase_cycle_slip_detected  = ((data & 0b0000000000000010) == 0b0000000000000010)
            self.carrier_phase_half_cycle_ambiguity = ((data & 0b0000000000000100) == 0b0000000000000100)
            self.pseudo_range_valid                 = ((data & 0b0000000000001000) == 0b0000000000001000)
            self.doppler_valid                      = ((data & 0b0000000000010000) == 0b0000000000010000)
            self.snr_valid                          = ((data & 0b0000000000100000) == 0b0000000000100000)

class FrequencyInformation():
    @dataclass()
    class FrequencyInformation:
        satellite_frequency: int = 0
        tracking_status: TrackingStatus = TrackingStatus()
        carrier_phase: int = 0
        pseudo_range: int = 0
        doppler_frequency: int = 0
        snr: int = 0

class SatelliteData():
    @dataclass()
    class SatelliteData:
        satellite_system: int = 0
        prn_satellite_number: int = 0
        elevation: int = 0
        azimuth: int = 0
        number_of_frequencies: int = 0
        frequency_information: FrequencyInformation = FrequencyInformation()

class RawSatelliteDataPacket():
    @dataclass()
    class RawSatelliteDataPacket:
        unix_time: int = 0
        nanoseconds: int = 0
        receiver_clock_offset: int  = 0
        receiver_number: int = 0
        packet_number: int = 0
        total_packets: int = 0
        number_of_satellites: int = 0
        satellite_data: SatelliteData = SatelliteData()

        def decode(self, an_packet: AN_Packet):
            if(an_packet.id == PacketID.PacketID.raw_satellite_data.value):
                self.unix_time = unpack('<I', bytes(an_packet.data[0:4]))[0]
                self.nanoseconds = unpack('<I', bytes(an_packet.data[4:8]))[0]
                self.receiver_clock_offset = unpack('<i', bytes(an_packet.data[8:12]))[0]
                self.receiver_number = an_packet.data[12]
                self.packet_number = an_packet.data[13]
                self.total_packets = an_packet.data[14]
                self.number_of_satellites = an_packet.data[15]
                self.satellite_data = [SatelliteData]*self.number_of_satellites

                datapoint = 15
                for i in range(self.number_of_satellites):
                    self.satellite_data[i].satellite_system = an_packet.data[datapoint + 1]
                    self.satellite_data[i].prn_satellite_number = an_packet.data[datapoint + 2]
                    self.satellite_data[i].elevation = an_packet.data[datapoint + 3]
                    self.satellite_data[i].azimuth = unpack('<H', bytes(an_packet.data[(datapoint + 4):(datapoint + 6)]))[0]
                    self.satellite_data[i].number_of_frequencies = an_packet.data[datapoint + 6]
                    self.satellite_data[i].frequency_information = [FrequencyInformation]*self.satellite_data[i].number_of_frequencies
                    datapoint += 6

                    for x in range(self.satellite_data[i].number_of_frequencies):
                        self.satellite_data[i].frequency_information[x].satellite_frequency = an_packet.data[datapoint + 1]
                        self.satellite_data[i].frequency_information[x].tracking_status.unpack(an_packet.data[datapoint + 2])
                        self.satellite_data[i].frequency_information[x].carrier_phase = unpack('<d', bytes(an_packet.data[(datapoint + 3):(datapoint + 11)]))[0]
                        self.satellite_data[i].frequency_information[x].pseudo_range = unpack('<d', bytes(an_packet.data[(datapoint + 11):(datapoint + 19)]))[0]
                        self.satellite_data[i].frequency_information[x].doppler_frequency = unpack('<f', bytes(an_packet.data[(datapoint + 19):(datapoint + 23)]))[0]
                        self.satellite_data[i].frequency_information[x].snr = unpack('<f', bytes(an_packet.data[(datapoint + 23):(datapoint + 25)]))[0]
                        datapoint += 26
                return 0
            else:
                return 1


class OdometerFlags():
    @dataclass()
    class OdometerFlags:
        reverse_detection_supported: bool = False
        # Bits [1:3] are reserved (set to zero)

        def unpack(self, flagsByte):
            self.reverse_detection_supported = ((flagsByte & 0b00000001) == 0b00000001)

class ExternalOdometerPacket():
    @dataclass()
    class ExternalOdometerPacket:
        estimated_delay: float = 0
        speed: float = 0
        distance_travelled: float = 0 # Only valid for OBDII input
        flags: OdometerFlags.OdometerFlags = OdometerFlags.OdometerFlags()

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_odometer.value) and (len(an_packet.data) == 13)):
                self.delay = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.speed = unpack('<f', bytes(an_packet.data[4:8]))[0]
                self.distance_travelled = unpack('<f', bytes(an_packet.data[8:12]))[0]
                self.flags.unpack(an_packet.data[12])
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<f', self.delay)
            data += pack('<f', self.speed)
            data += pack('<f', self.distance_travelled)
            data += pack('<B', self.flags)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_odometer.value, 13, data)

            return an_packet


class ExternalAirDataPacketFlags():
    @dataclass()
    class ExternalAirDataPacketFlags:
        barometric_altitude_set_and_valid: bool = False
        airspeed_set_and_valid: bool = False
        barometric_altitude_reference_reset: bool = False

        def unpack(self, data):
            self.barometric_altitude_set_and_valid =    ((data & 0b00000001) == 0b00000001)
            self.airspeed_set_and_valid =               ((data & 0b00000010) == 0b00000010)
            self.barometric_altitude_reference_reset =  ((data & 0b00000100) == 0b00000100)

class ExternalAirDataPacket():
    @dataclass()
    class ExternalAirDataPacket:
        barometric_altitude_delay: float = 0
        airspeed_delay: float = 0
        barometric_altitude: float = 0
        airspeed: float = 0
        barometric_altitude_standard_deviation: float = 0
        airspeed_standard_deviation: float = 0
        flags: ExternalAirDataPacketFlags.ExternalAirDataPacketFlags = ExternalAirDataPacketFlags.ExternalAirDataPacketFlags()

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_air_data.value) and (len(an_packet.data) == 25)):
                self.barometric_altitude_delay = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.airspeed_delay = unpack('<f', bytes(an_packet.data[4:8]))[0]
                self.barometric_altitude = unpack('<f', bytes(an_packet.data[8:12]))[0]
                self.airspeed = unpack('<f', bytes(an_packet.data[12:16]))[0]
                self.barometric_altitude_standard_deviation = unpack('<f', bytes(an_packet.data[16:20]))[0]
                self.airspeed_standard_deviation = unpack('<f', bytes(an_packet.data[20:24]))[0]
                self.flags.unpack(an_packet.data[24])
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<f', self.barometric_altitude_delay)
            data += pack('<f', self.airspeed_delay)
            data += pack('<f', self.barometric_altitude)
            data += pack('<f', self.airspeed)
            data += pack('<f', self.barometric_altitude_standard_deviation)
            data += pack('<f', self.airspeed_standard_deviation)
            data += pack('<B', self.flags)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.external_air_data.value, 25, data)

            return an_packet


class AirDataPacketFlags():
    @dataclass()
    class AirDataPacketFlags:
        barometric_altitude_valid: bool = False
        airspeed_valid: bool = False
        barometric_altitude_sensor_over_range: bool = False
        airspeed_sensor_overrange: bool = False
        barometric_altitude_sensor_failure: bool = False
        airspeed_sensor_failure: bool = False

        def unpack(self, data):
            self.barometric_altitude_valid =                ((data & 0b00000001) == 0b00000001)
            self.airspeed_valid =                           ((data & 0b00000010) == 0b00000010)
            self.barometric_altitude_sensor_over_range =    ((data & 0b00000100) == 0b00000100)
            self.airspeed_sensor_overrange =                ((data & 0b00001000) == 0b00001000)
            self.barometric_altitude_sensor_failure =       ((data & 0b00010000) == 0b00010000)
            self.airspeed_sensor_failure =                  ((data & 0b00100000) == 0b00100000)

class AirDataPacket():
    @dataclass()
    class AirDataPacket:
        barometric_altitude_delay: float = 0
        airspeed_delay: float = 0
        barometric_altitude: float = 0
        airspeed: float = 0
        barometric_altitude_standard_deviation: float = 0
        airspeed_standard_deviation: float = 0
        flags: AirDataPacketFlags.AirDataPacketFlags = AirDataPacketFlags.AirDataPacketFlags()

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.external_air_data.value) and (len(an_packet.data) == 25)):
                self.barometric_altitude_delay = unpack('<f', bytes(an_packet.data[0:4]))[0]
                self.airspeed_delay = unpack('<f', bytes(an_packet.data[4:8]))[0]
                self.barometric_altitude = unpack('<f', bytes(an_packet.data[8:12]))[0]
                self.airspeed = unpack('<f', bytes(an_packet.data[12:16]))[0]
                self.barometric_altitude_standard_deviation = unpack('<f', bytes(an_packet.data[16:20]))[0]
                self.airspeed_standard_deviation = unpack('<f', bytes(an_packet.data[20:24]))[0]
                self.flags.unpack(an_packet.data[24])
                return 0
            else:
                return 1


########## Configuration Packets ##########
class PacketTimerPeriodPacket():
    @dataclass()
    class PacketTimerPeriodPacket:
        permanent: int = 0
        utc_synchronisation: int = 0
        packet_timer_period: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.packet_timer_period.value) and (len(an_packet.data) == 4)):
                self.permanent = an_packet.data[0]
                self.utc_synchronisation = an_packet.data[1]
                self.packet_timer_period = unpack('<H', bytes(an_packet.data[2:4]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<B', self.permanent)
            data += pack('<B', self.utc_synchronisation)
            data += pack('<H', self.packet_timer_period)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.packet_timer_period.value, 4, data)

            return an_packet


class PacketPeriod():
    @dataclass()
    class PacketPeriod:
        packet_id: int = 0
        period: int = 0

class PacketsPeriodPacket():
    @dataclass()
    class PacketsPeriodPacket:
        permanent: int = 0
        clear_existing_packets: int = 0
        packet_periods: PacketPeriod = field(default_factory=list)

        def decode(self,an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.packets_period.value) and ((len(an_packet.data) - 2) % 5 == 0)):
                packet_periods_count = (an_packet.length - 2) / 5
                self.permanent = an_packet.data[0]
                self.clear_existing_packets = an_packet.data[1]
                self.packet_periods = [PacketPeriod()]*MAXIMUM_PACKET_PERIODS
                for i in range(MAXIMUM_PACKET_PERIODS):
                    if(i < packet_periods_count):
                        self.packet_periods[i].packet_id = an_packet.data[2 + 5*i]
                        self.packet_periods[i].period = unpack('<I', an_packet[(2 + 5*i + 1) : (2 + 5*i + 5)])
                    else:
                        self.packet_periods[i].packet_id = 0
                        self.packet_periods[i].period = 0
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<B', self.permanent)
            data += pack('<I', self.clear_existing_packets)
            for i in range(MAXIMUM_PACKET_PERIODS):
                data += pack('<B', self.packet_periods[i].packet_id)
                data += pack('<I', self.packet_periods[i].period)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.packets_period.value, (2 + 5*MAXIMUM_PACKET_PERIODS), data)

            return an_packet


class BaudRatesPacket():
    @dataclass()
    class BaudRatesPacket:
        permanent: int = 0
        primary_baud_rate: int = 0
        gpio_1_2_baud_rate: int = 0
        auxiliary_baud_rate: int = 0
        reserved: int = 0 # Reserved (set to zero)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.baud_rates.value) and (len(an_packet.data) == 17)):
                self.permanent = an_packet.data[0]
                self.primary_baud_rate = unpack('<I', bytes(an_packet.data[1:5]))[0]
                self.gpio_1_2_baud_rate = unpack('<I', bytes(an_packet.data[5:9]))[0]
                self.auxiliary_baud_rate = unpack('<I', bytes(an_packet.data[9:13]))[0]
                self.reserved = unpack('<I', bytes(an_packet.data[13:17]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<B', self.permanent)
            data += pack('<I', self.primary_baud_rate)
            data += pack('<I', self.gpio_1_2_baud_rate)
            data += pack('<I', self.auxiliary_baud_rate)
            data += pack('<I', self.reserved)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.baud_rates.value, 17, data)

            return an_packet


class AccelerometerRange():
    class AccelerometerRange(Enum):
        accelerometer_range_2g = 0
        accelerometer_range_4g = 1
        accelerometer_range_16g = 2

class GyroscopeRange():
    class GyroscopeRange(Enum):
        gyroscope_range_250dps = 0
        gyroscope_range_500dps = 1
        gyroscope_range_2000dps = 2

class MagnetometerRange():
    class MagnetometerRange(Enum):
        magnetometer_range_2g = 0
        magnetometer_range_4g = 1
        magnetometer_range_8g = 2

class SensorRangesPacket():
    @dataclass()
    class SensorRangesPacket:
        permanent: int = 0
        accelerometers_range: int = 0
        gyroscopes_range: int = 0
        magnetometers_range: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.sensor_ranges.value) and (len(an_packet.data) == 4)):
                self.permanent = an_packet.data[0]
                self.accelerometers_range = an_packet.data[1]
                self.gyroscopes_range = an_packet.data[2]
                self.magnetometers_range = an_packet.data[3]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<BBBB', self.permanent, self.accelerometers_range, self.gyroscopes_range, self.magnetometers_range)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.sensor_ranges.value, 4, data)

            return an_packet


class InstallationAlignmentPacket():
    @dataclass()
    class InstallationAlignmentPacket:
        permanent: int = 0
        alignment_dcm: [[float]*3]*3 = field(default_factory=list)
        gnss_antenna_offset: [float]*3 = field(default_factory=list)
        odometer_offset: [float]*3 = field(default_factory=list)
        external_data_offset: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.installation_alignment.value) and (len(an_packet.data) == 73)):
                self.permanent = an_packet.data[0]
                self.alignment_dcm = [[unpack('<fff', bytes(an_packet.data[1:13]))],
                                      [unpack('<fff', bytes(an_packet.data[13:25]))],
                                      [unpack('<fff', bytes(an_packet.data[25:37]))]]
                self.gnss_antenna_offset = [unpack('<fff', bytes(an_packet.data[37:49]))]
                self.odometer_offset = [unpack('<fff', bytes(an_packet.data[49:61]))]
                self.external_data_offset = [unpack('<fff', bytes(an_packet.data[61:73]))]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<B', self.permanent)
            data += pack('<fff', self.alignment_dcm[0][0], self.alignment_dcm[0][1], self.alignment_dcm[0][2])
            data += pack('<fff', self.alignment_dcm[1][0], self.alignment_dcm[1][1], self.alignment_dcm[1][2])
            data += pack('<fff', self.alignment_dcm[2][0], self.alignment_dcm[2][1], self.alignment_dcm[2][2])
            data += pack('<fff', self.gnss_antenna_offset[0], self.gnss_antenna_offset[1], self.gnss_antenna_offset[2])
            data += pack('<fff', self.odometer_offset[0], self.odometer_offset[1], self.odometer_offset[2])
            data += pack('<fff', self.external_data_offset[0], self.external_data_offset[1], self.external_data_offset[2])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.installation_alignment.value, 73, data)

            return an_packet


class VehicleType():
    class VehicleType(Enum):
        unconstrained = 0
        bicycle = 1
        car = 2
        hovercraft = 3
        submarine = 4
        underwater_3d = 5
        fixed_wing_plane = 6
        aircraft_3d = 7
        human = 8
        boat = 9
        large_ship = 10
        stationary = 11
        stunt_plane = 12
        race_car = 13

class FilterOptionsPacket():
    @dataclass()
    class FilterOptionsPacket:
        permanent: int = 0
        vehicle_type: int = 0
        internal_gnss_enabled: int = 0
        magnetometers_enabled: int = 0
        atmospheric_altitude_enabled: int = 0
        velocity_heading_enabled: int = 0
        reversing_detection_enabled: int = 0
        motion_analysis_enabled: int = 0
        automatic_magnetic_calibration_enabled: int = 0
        reserved: DOUBLE = 0 # Reserved (set to zero)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.filter_options.value) and (len(an_packet.data) == 17)):
                self.permanent = an_packet.data[0]
                self.vehicle_type = an_packet.data[1]
                self.internal_gnss_enabled = an_packet.data[2]
                self.magnetometers_enabled = an_packet.data[3]
                self.atmospheric_altitude_enabled = an_packet.data[4]
                self.velocity_heading_enabled = an_packet.data[5]
                self.reversing_detection_enabled = an_packet.data[6]
                self.motion_analysis_enabled = an_packet.data[7]
                self.automatic_magnetic_calibration_enabled = an_packet.data[8]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<BBBBBBBBBd', self.permanent, self.vehicle_type,
                        self.internal_gnss_enabled, self.magnetometers_enabled,
                        self.atmospheric_altitude_enabled, self.velocity_heading_enabled,
                        self.reversing_detection_enabled, self.motion_analysis_enabled,
                        self.automatic_magnetic_calibration_enabled, self.reserved)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.filter_options.value, 17, data)

            return an_packet


class GPIO1Function():
    class GPIO1Function(Enum):
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

class GPIO2Function():
    class GPIO2Function(Enum):
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

class AuxiliaryTxFunction():
    class AuxiliaryTxFunction(Enum):
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

class AuxiliaryRxFunction():
    class AuxiliaryRxFunction(Enum):
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

class GPIOIndex():
    class GPIOIndex(Enum):
        gpio1 = 0
        gpio2 = 1
        auxiliary_tx = 2
        auxiliary_rx = 3

class GPIOConfigurationPacket():
    @dataclass()
    class GPIOConfigurationPacket:
        permanent: int = 0
        gpio1_function: int = 0
        gpio2_function: int = 0
        auxTx_function: int = 0
        auxRx_function: int = 0
        reserved: DOUBLE = 0 # Reserved (set to zero)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.gpio_configuration.value) and (len(an_packet.data) == 13)):
                self.permanent = an_packet.data[0]
                self.gpio1_function = an_packet.data[1]
                self.gpio2_function = an_packet.data[2]
                self.auxTx_function = an_packet.data[3]
                self.auxRx_function = an_packet.data[4]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<BBBBBd', self.permanent, self.gpio1_function,
                        self.gpio2_function, self.auxTx_function,
                        self.auxRx_function, self.reserved)
    
            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.gpio_configuration.value, 13, data)

            return an_packet


class MagneticCalibrationValuesPacket():
    @dataclass()
    class MagneticCalibrationValuesPacket:
        permanent: int = 0
        hard_iron: [float]*3 = field(default_factory=list)
        soft_iron: [[float]*3]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.magnetic_calibration_values.value) and (len(an_packet.data) == 49)):
                self.permanent = an_packet.data[0]
                self.hard_iron = unpack('<fff', bytes(an_packet.data[1:13]))
                self.soft_iron = [unpack('<fff', bytes(an_packet.data[13:25])),
                                    unpack('<fff', bytes(an_packet.data[25:37])),
                                    unpack('<fff', bytes(an_packet.data[37:49]))]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<B', self.permanent)
            data += pack('<fff', self.hard_iron[0], self.hard_iron[1], self.hard_iron[2])
            data += pack('<fff', self.soft_iron[0][0], self.soft_iron[0][1], self.soft_iron[0][2])
            data += pack('<fff', self.soft_iron[1][0], self.soft_iron[1][1], self.soft_iron[1][2])
            data += pack('<fff', self.soft_iron[2][0], self.soft_iron[2][1], self.soft_iron[2][2])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.magnetic_calibration_values.value, 49, data)

            return an_packet

class MagneticCalibrationAction():
    class MagneticCalibrationAction(Enum):
        cancel = 0
        start_2d = 2
        start_3d = 3
        reset = 4

class MagneticCalibrationConfigurationPacket():
    @dataclass()
    class MagneticCalibrationConfigurationPacket:
        magnetic_calibration_action: int = 0

        def encode(self):
            data = pack('<B', self.magnetic_calibration_action)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.magnetic_calibration_configuration.value, 1, data)

            return an_packet


class MagneticCalibrationStatus():
    class MagneticCalibrationStatus(Enum):
        not_completed = 0
        completed_2d = 1
        completed_3d = 2
        completed_custom_values = 3
        in_progress_2d = 5
        in_progress_3d = 6
        error_excessive_roll_2d = 7
        error_excessive_pitch_2d = 8
        error_overrange_event = 9
        error_timeout = 10
        error_system = 11
        error_interterence = 12

class MagneticCalibrationStatusPacket():
    @dataclass()
    class MagneticCalibrationStatusPacket:
        magnetic_calibration_status: int = 0
        magnetic_calibration_progress_percentage: int = 0
        local_magnetic_error_percentage: int = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.magnetic_calibration_status.value) and (len(an_packet.data) == 3)):
                self.magnetic_calibration_status = an_packet.data[0]
                self.magnetic_calibration_progress_percentage = an_packet.data[1]
                self.local_magnetic_error_percentage = an_packet.data[2]
                return 0
            else:
                return 1


class OdometerConfigurationPacket():
    @dataclass()
    class OdometerConfigurationPacket:
        permanent: int = 0
        automatic_pulse_measurement_active: int = 0
        reserved: int = 0 # Reserved (set to zero)
        pulse_length: float = 0

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.odometer_configuration.value) and (len(an_packet.data) == 8)):
                self.permanent = an_packet.data[0]
                self.automatic_calibration = an_packet.data[1]
                self.pulse_length = unpack('<f', bytes(an_packet.data[4:8]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<BBHf', self.permanent, self.automatic_calibration, self.reserved, self.pulse_length)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.odometer_configuration.value, 8, data)

            return an_packet


class SetZeroOrientationAlignmentPacket():
    @dataclass()
    class SetZeroOrientationAlignmentPacket:
        permanent: int = 0

        def encode(self):
            verification = 0x9A4E8055
            data = pack('<BI', self.permanent, verification)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.set_zero_orientation_alignment.value, 5, data)

            return an_packet


class ReferencePointOffsetsPacket():
    @dataclass()
    class ReferencePointOffsetsPacket:
        permanent: int = 0
        primary_reference_point_offset: [float]*3 = field(default_factory=list)
        heave_point_2_offset: [float]*3 = field(default_factory=list)
        heave_point_3_offset: [float]*3 = field(default_factory=list)
        heave_point_4_offset: [float]*3 = field(default_factory=list)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.reference_point_offsets.value) and (len(an_packet.data) == 49)):
                self.permanent = an_packet.data[0]
                self.primary_reference_point_offset = unpack('<fff', bytes(an_packet.data[1:13]))[0]
                self.heave_point_2_offset = unpack('<fff', bytes(an_packet.data[13:25]))[0]
                self.heave_point_3_offset = unpack('<fff', bytes(an_packet.data[25:37]))[0]
                self.heave_point_4_offset = unpack('<fff', bytes(an_packet.data[37:49]))[0]
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<Bffffffffffff', self.permanent,
                        self.primary_reference_point_offset[0], self.primary_reference_point_offset[1], self.primary_reference_point_offset[2],
                        self.heave_point_2_offset[0], self.heave_point_2_offset[1], self.heave_point_2_offset[2],
                        self.heave_point_3_offset[0], self.heave_point_3_offset[1], self.heave_point_3_offset[2],
                        self.heave_point_4_offset[0], self.heave_point_4_offset[1], self.heave_point_4_offset[2])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.reference_point_offsets.value, 49, data)

            return an_packet


class GPIORate():
    class GPIORate(Enum):
        gpio_rate_disabled = 0
        gpio_rate_0o1hz = 1
        gpio_rate_0o2hz = 2
        gpio_rate_0o5hz = 3
        gpio_rate_1hz = 4
        gpio_rate_2hz = 5
        gpio_rate_5hz = 6
        gpio_rate_10hz = 7
        gpio_rate_25hz = 8
        gpio_rate_50hz = 9

class NMEAFixBehaviour():
    class NMEAFixBehaviour(Enum):
        nmea_fix_behaviour_normal = 0
        nmea_fix_behaviour_always_3d = 1

class GPIOOutputRate():
    @dataclass()
    class GPIOOutputRate:
        gpio1_rate: int = 0
        auxiliary_rate: int = 0

        def unpack(self, data):
            self.gpio1_rate = (data & 0b00001111)
            self.auxiliary_rate = ((data & 0b11110000) >> 4)

class GPIOOutputConfigurationPacket():
    @dataclass()
    class GPIOOutputConfigurationPacket:
        permanent: int = 0
        nmea_fix_behaviour: int = 0
        gpzda_rate: GPIOOutputRate = GPIOOutputRate()
        gpgga_rate: GPIOOutputRate = GPIOOutputRate()
        gpvtg_rate: GPIOOutputRate = GPIOOutputRate()
        gprmc_rate: GPIOOutputRate = GPIOOutputRate()
        gphdt_rate: GPIOOutputRate = GPIOOutputRate()
        gpgll_rate: GPIOOutputRate = GPIOOutputRate()
        pashr_rate: GPIOOutputRate = GPIOOutputRate()
        tss1_rate: GPIOOutputRate = GPIOOutputRate()
        simrad_rate: GPIOOutputRate = GPIOOutputRate()
        gprot_rate: GPIOOutputRate = GPIOOutputRate()
        gphev_rate: GPIOOutputRate = GPIOOutputRate()
        gpgsv_rate: GPIOOutputRate = GPIOOutputRate()
        pfecatt_rate: GPIOOutputRate = GPIOOutputRate()
        pfechve_rate: GPIOOutputRate = GPIOOutputRate()
        reserved: int = 0 # 3 bytes reserved (set to zero)

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.gpio_output_configuration.value) and (len(an_packet.data) == 33)):
                self.permanent = an_packet.data[0]
                self.nmea_fix_behaviour = an_packet.data[1]
                self.gpzda_rate.unpack(unpack('<I', bytes(an_packet.data[2:4]))[0])
                self.gpgga_rate.unpack(unpack('<I', bytes(an_packet.data[4:6]))[0])
                self.gpvtg_rate.unpack(unpack('<I', bytes(an_packet.data[6:8]))[0])
                self.gprmc_rate.unpack(unpack('<I', bytes(an_packet.data[8:10]))[0])
                self.gphdt_rate.unpack(unpack('<I', bytes(an_packet.data[10:12]))[0])
                self.gpgll_rate.unpack(unpack('<I', bytes(an_packet.data[12:14]))[0])
                self.pashr_rate.unpack(unpack('<I', bytes(an_packet.data[14:16]))[0])
                self.tss1_rate.unpack(unpack('<I', bytes(an_packet.data[16:18]))[0])
                self.simrad_rate.unpack(unpack('<I', bytes(an_packet.data[18:20]))[0])
                self.gprot_rate.unpack(unpack('<I', bytes(an_packet.data[20:22]))[0])
                self.gphev_rate.unpack(unpack('<I', bytes(an_packet.data[22:24]))[0])
                self.gpgsv_rate.unpack(unpack('<I', bytes(an_packet.data[24:26]))[0])
                self.pfecatt_rate.unpack(unpack('<I', bytes(an_packet.data[26:28]))[0])
                self.pfechve_rate.unpack(unpack('<I', bytes(an_packet.data[28:30]))[0])
                return 0
            else:
                return 1

        def encode(self):
            data = pack('<BBIIIIIIIIIIIIIIBBB', self.permanent,
                        self.gpzda_rate, self.gpgga_rate, self.gpvtg_rate,
                        self.gprmc_rate, self.gphdt_rate, self.gpgll_rate,
                        self.pashr_rate, self.tss1_rate, self.simrad_rate,
                        self.gprot_rate, self.gphev_rate, self.gpgsv_rate,
                        self.pfecatt_rate, self.pfechve_rate, 0, 0, 0)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.gpio_output_configuration.value, 33, data)

            return an_packet


class UserDatapacket():
    @dataclass()
    class UserDatapacket:
        user_data: [int]*64

        def decode(self, an_packet: AN_Packet):
            if((an_packet.id == PacketID.PacketID.user_data.value) and (len(an_packet.data) == 64)):
                self.user_data = an_packet.data[0:64]
                return 0
            else:
                return 1
        def encode(self):
            data = []
            for x in range(64):
                data.append(self.user_data[x])

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.user_data.value, 64, data)

            return an_packet

class GpioInputConfigurationPacket():
    @dataclass()
    class GpioInputConfigurationPacket:
        permanent: int = 0
        gimbal_radians_per_encoder_tick: float = 0
        reserved: [float]*60 = field(default_factory=list)
        def decode(self):
            pass
        def encode(self):
            pass