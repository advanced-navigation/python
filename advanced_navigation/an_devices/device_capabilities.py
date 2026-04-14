################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                           device_capabilities.py                           ##
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
from ..anpp_packets.an_packet_13 import DeviceSubtype, CertusDeviceSubtype, CertusMiniDeviceSubtype

__all__ = [
    'get_auxiliary_baud_rate_array',
    'get_baud_rate_array',
    'get_default_baud_rate',
    'get_gpio_baud_rate_array',
    'get_primary_baud_rate_array',
    'has_10mbaud_serial',
    'has_2400baud_serial',
    'has_4mbaud_serial',
    'has_aiding_source_configuration',
    'has_anfw_v2',
    'has_antenna_connection_reporting',
    'has_application_bootloader',
    'has_atmospheric_altitude_filter',
    'has_automatic_magnetic_calibration_filter',
    'has_base_station',
    'has_can',
    'has_cold_start',
    'has_detailed_satellites',
    'has_disable_navigation_filter',
    'has_dual_antenna',
    'has_dual_antenna_configuration',
    'has_dual_antenna_heading_filter',
    'has_extended_device_information',
    'has_extended_satellites',
    'has_external_air_data',
    'has_external_magnetometers',
    'has_external_sound_velocity',
    'has_external_temperature_sensor_configuration',
    'has_gimbal_support',
    'has_gnss_configuration',
    'has_gnss_firmware_update',
    'has_gnss_receiver_information',
    'has_gnss_summary',
    'has_internal_gnss',
    'has_internal_gnss_filter',
    'has_local_magnetic_field',
    'has_logging',
    'has_magnetic_calibration',
    'has_magnetic_heading_filter',
    'has_magnetometer',
    'has_magnetometer_ranges',
    'has_manual_initialisation',
    'has_motion_analysis_filter',
    'has_networking',
    'has_north_seeking',
    'has_odometer_support',
    'has_packet_timer_period',
    'has_packets_period_port',
    'has_pressure',
    'has_raw_satellite_ephemeris',
    'has_reversing_detection_filter',
    'has_selectable_auxiliary_serial_mode',
    'has_selectable_gpio_serial_mode',
    'has_selectable_gpio_voltage',
    'has_selectable_primary_serial_mode',
    'has_sensor_ranges',
    'has_sensor_temperatures',
    'has_serial_ports',
    'has_specified_packet_periods_port',
    'has_sub_type',
    'has_system_temperatures',
    'has_velocity_heading_filter',
    'has_vessel_motion',
    'has_zero_angular_velocity',
    'is_air_data_unit',
    'is_boreas',
    'is_certus_mini',
    'is_gnss_firmware_update_allowed',
    'is_ins',
    'is_oem',
    'is_orientus'
]

# Device group definitions
AIR_DATA_UNIT_DEVICES = {
    DeviceID.air_data_unit,
    DeviceID.air_data_unit_v2
}

BOREAS_DEVICES = {
    DeviceID.boreas_a50,
    DeviceID.boreas_a70,
    DeviceID.boreas_a90,
    DeviceID.boreas_d50,
    DeviceID.boreas_d70,
    DeviceID.boreas_d90
}

CERTUS_MINI_DEVICES = {
    DeviceID.certus_mini_a,
    DeviceID.certus_mini_n,
    DeviceID.certus_mini_d
}

ORIENTUS_DEVICES = {
    DeviceID.orientus,
    DeviceID.orientus_v3
}

INS_DEVICES = {
    DeviceID.boreas_a50,
    DeviceID.boreas_a70,
    DeviceID.boreas_a90,
    DeviceID.boreas_d50,
    DeviceID.boreas_d70,
    DeviceID.boreas_d90,
    DeviceID.certus,
    DeviceID.certus_mini_a,
    DeviceID.certus_mini_n,
    DeviceID.certus_mini_d,
    DeviceID.gnss_compass,
    DeviceID.motus,
    DeviceID.spatial,
    DeviceID.spatial_dual,
    DeviceID.spatial_fog,
    DeviceID.spatial_fog_dual
}

def get_auxiliary_baud_rate_array(device_id: DeviceID) -> List[str]:
    """Get list of available auxiliary baudrates"""
    min_baud = 2400 if has_2400baud_serial(device_id) else 4800
    
    if has_10mbaud_serial(device_id):
        max_baud = 10000000
    elif has_4mbaud_serial(device_id):
        max_baud = 4000000
    elif device_id == DeviceID.gnss_compass:
        max_baud = 1000000
    else:
        max_baud = 2000000
        
    return get_baud_rate_array(min_baud, max_baud)

def get_baud_rate_array(minimum_baud: int, maximum_baud: int) -> List[str]:
    """Trim the default baudrate array to values between a minimum and a maximum"""
    default_baud_rates = [
        "2400",
        "4800",
        "9600",
        "19200",
        "38400",
        "57600",
        "115200",
        "230400",
        "250000",
        "460800",
        "500000",
        "800000",
        "921600",
        "1000000",
        "1250000",
        "2000000",
        "4000000",
        "10000000"
    ]
    return [b for b in default_baud_rates if minimum_baud <= int(b) <= maximum_baud]

def get_default_baud_rate(device_id: DeviceID) -> int:
    """Get device default baudrate"""
    return 115200

def get_gpio_baud_rate_array(device_id: DeviceID) -> List[str]:
    """Get list of available baudrates for the GPIO port"""
    min_baud = 2400 if has_2400baud_serial(device_id) else 4800
    return get_baud_rate_array(min_baud, 250000)

def get_primary_baud_rate_array(device_id: DeviceID) -> List[str]:
    """Get list of available primary baudrates"""
    min_baud = 2400 if has_2400baud_serial(device_id) else 4800
    
    if has_10mbaud_serial(device_id):
        max_baud = 10000000
    elif has_4mbaud_serial(device_id):
        max_baud = 4000000
    elif device_id == DeviceID.gnss_compass:
        max_baud = 1000000
    else:
        max_baud = 2000000
        
    return get_baud_rate_array(min_baud, max_baud)

def has_10mbaud_serial(device_id: DeviceID) -> bool:
    """Check if the device has high speed serial (10Mbaud). Packets impacted: 182"""
    devices = {
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_2400baud_serial(device_id: DeviceID) -> bool:
    """Check if the device has low speed serial (2400baud). Packets impacted: 182"""
    devices = {
        DeviceID.gnss_compass,
        DeviceID.spatial,
        DeviceID.motus,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_4mbaud_serial(device_id: DeviceID) -> bool:
    """Check if the device has high speed serial (4Mbaud). Packets impacted: 182"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus
    }
    return device_id in devices

def has_aiding_source_configuration(device_id: DeviceID) -> bool:
    """Check if the device has aiding source configuration. Packets impacted: 207, 208"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_anfw_v2(device_id: DeviceID) -> bool:
    """Check if the device supports ANFW v2. Packets impacted: 8, 9"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_antenna_connection_reporting(device_id: DeviceID) -> bool:
    """Check if the device reports antenna short/open/connected in ANPP29 Raw GNSS packet."""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_application_bootloader(device_id: DeviceID) -> bool:
    """Check if the device supports application bootloading. Packets impacted: 2"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus
    }
    return device_id in devices

def has_atmospheric_altitude_filter(device_id: DeviceID) -> bool:
    """Check if the atmospheric altitude can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_automatic_magnetic_calibration_filter(device_id: DeviceID) -> bool:
    """Check if the magnetic calibration can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial
    }
    return device_id in devices

def has_base_station(device_id: DeviceID) -> bool:
    """Check if the device has the base station packet. Packets impacted: 80"""
    devices = {
        DeviceID.certus,
        DeviceID.spatial_dual
    }
    return device_id in devices

def has_can(device_id: DeviceID) -> bool:
    """Check if the device has CAN. Packets impacted: 203"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_cold_start(device_id: DeviceID) -> bool:
    """Check if the device supports cold start reset. Packets impacted: 5"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_detailed_satellites(device_id: DeviceID) -> bool:
    """Check if the device has detailed satellites. Packets impacted: 61"""
    devices = {
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_disable_navigation_filter(device_id: DeviceID) -> bool:
    """Check if navigation can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_dual_antenna(device_id: DeviceID) -> bool:
    """Check if the device has two GNSS antennas. Packets impacted: 196"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_dual_antenna_configuration(device_id: DeviceID) -> bool:
    """Check if the device has dual antenna configuration. Packets impacted: 196"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_d,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_dual_antenna_heading_filter(device_id: DeviceID) -> bool:
    """Check if the dual antenna heading can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_d,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_extended_device_information(device_id: DeviceID) -> bool:
    """Check if the device has extended device information. Packets impacted: 13"""
    devices = {
        DeviceID.air_data_unit_v2,
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_extended_satellites(device_id: DeviceID) -> bool:
    """Check if the device has extended satellites. Packets impacted: 84"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_external_air_data(device_id: DeviceID) -> bool:
    """Check if the device supports external air data. Packets impacted: 68"""
    devices = {
        DeviceID.air_data_unit,
        DeviceID.air_data_unit_v2,
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_external_magnetometers(device_id: DeviceID) -> bool:
    """Check if the device supports external magnetometers. Packets impacted: 75"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.gnss_compass
    }
    return device_id in devices

def has_external_sound_velocity(device_id: DeviceID) -> bool:
    """Check if the device supports external sound velocity. Packets impacted: 91"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_external_temperature_sensor_configuration(device_id: DeviceID) -> bool:
    """Check if the device supports external temperature sensor configuration. Packets impacted: 209"""
    return device_id == DeviceID.air_data_unit_v2

def has_gimbal_support(device_id: DeviceID) -> bool:
    """Check if the device supports a gimbal. Packets impacted: 72, 188, 199"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_gnss_configuration(device_id: DeviceID) -> bool:
    """Check if the device has the GNSS Configuration packet. Packets impacted: 197"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_gnss_firmware_update(device_id: DeviceID, gnss_manufacturer_id: int, gnss_receiver_model: int) -> bool:
    """Check if the device has GNSS firmware update support"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices and is_gnss_firmware_update_allowed(gnss_manufacturer_id, gnss_receiver_model)

def has_gnss_receiver_information(device_id: DeviceID) -> bool:
    """Check if the device has the GNSS Receiver Information packet. Packets impacted: 196"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_gnss_summary(device_id: DeviceID) -> bool:
    """Check if the device has the GNSS Summary packet. Packets impacted: 66"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_internal_gnss(device_id: DeviceID) -> bool:
    """Check if the device has a GNSS receiver or supports an external receiver. Packets impacted: 29, 30, 31, 60, 61, 66, 69, 84, 186, 196, 197"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_internal_gnss_filter(device_id: DeviceID) -> bool:
    """Check if the internal GNSS can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_local_magnetic_field(device_id: DeviceID) -> bool:
    """Check if the device has the local magnetic field packet. Packets impacted: 50"""
    devices = {
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_logging(device_id: DeviceID) -> bool:
    """Check if the device has internal logging"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus
    }
    return device_id in devices

def has_magnetic_calibration(device_id: DeviceID) -> bool:
    """Check if the device supports magnetic calibration. Packets impacted: 90, 189, 190, 191"""
    devices = {
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial
    }
    return device_id in devices

def has_magnetic_heading_filter(device_id: DeviceID) -> bool:
    """Check if the magnetic heading can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.orientus_v3,
        DeviceID.spatial
    }
    return device_id in devices

def has_magnetometer(device_id: DeviceID) -> bool:
    """Check if the device has magnetometers. Packets impacted: 28, 50, 184, 186, 189, 190, 191"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_d50,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_magnetometer_ranges(device_id: DeviceID, device_sub_type: DeviceSubtype | None = None) -> bool:
    """Check if the device supports magnetometer ranges. Packets impacted: 184"""
    devices = {
        DeviceID.certus,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial,
        DeviceID.spatial_dual
    }
    is_certus_evo = device_id == DeviceID.certus and device_sub_type in (CertusDeviceSubtype.certus_evo, CertusDeviceSubtype.certus_evo_oem)
    return not is_certus_evo and device_id in devices

def has_manual_initialisation(device_id: DeviceID) -> bool:
    """Check if the device supports manual initialisation. Packets impacted: 48"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_motion_analysis_filter(device_id: DeviceID) -> bool:
    """Check if the motion analysis can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.orientus_v3,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_networking(device_id: DeviceID) -> bool:
    """Check if the device has networking. Packets impacted: 11, 202"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.gnss_compass
    }
    return device_id in devices

def has_north_seeking(device_id: DeviceID) -> bool:
    """Check if the device has North seeking. Packets impacted: 71"""
    devices = {
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_odometer_support(device_id: DeviceID) -> bool:
    """Check if the device supports an odometer. Packets impacted: 51, 67, 192"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_packets_period_port(device_id: DeviceID) -> bool:
    """Check if the device supports the selection of the port in the Packets Period packet"""
    return device_id == DeviceID.gnss_compass

def has_packet_timer_period(device_id: DeviceID) -> bool:
    """Check if the device supports the packet timer period. Packets impacted: 180"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices
        

def has_pressure(device_id: DeviceID) -> bool:
    """Check if the device has a pressure sensor. Packets impacted: 28, 186"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_raw_satellite_ephemeris(device_id: DeviceID) -> bool:
    """Check if the device has the raw satellite ephemeris packet. Packets impacted: 61"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.gnss_compass,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_reversing_detection_filter(device_id: DeviceID) -> bool:
    """Check if the reversing detection can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_selectable_auxiliary_serial_mode(device_id: DeviceID, device_sub_type: DeviceSubtype | None = None) -> bool:
    """Check if the device has selectable auxiliary serial mode (RS232/RS422). Packets impacted: 182"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.gnss_compass
    }
    return device_id in devices and not is_oem(device_id, device_sub_type)

def has_selectable_gpio_serial_mode(device_id: DeviceID, device_sub_type: DeviceSubtype | None = None) -> bool:
    """Check if the device has selectable gpio serial mode (RS232/TTL). Packets impacted: 182"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices and not is_oem(device_id, device_sub_type)

def has_selectable_gpio_voltage(device_id: DeviceID) -> bool:
    """Check if the device has selectable GPIO voltage. Packets impacted: 188"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus
    }
    return device_id in devices

def has_selectable_primary_serial_mode(device_id: DeviceID, device_sub_type: DeviceSubtype | None = None) -> bool:
    """Check if the device has selectable primary serial mode (RS232/RS422). Packets impacted: 182"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass
    }
    return device_id in devices and not is_oem(device_id, device_sub_type)

def has_sensor_ranges(device_id: DeviceID, device_sub_type: DeviceSubtype | None = None) -> bool:
    """Check if the device supports sensor ranges. Packets impacted: 184"""
    devices = {
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial,
        DeviceID.spatial_dual
    }
    is_certus_evo = device_id == DeviceID.certus and device_sub_type in (CertusDeviceSubtype.certus_evo, CertusDeviceSubtype.certus_evo_oem)
    return not is_certus_evo and device_id in devices

def has_sensor_temperatures(device_id: DeviceID) -> bool:
    """Check if the device has sensor temperatures packet. Packets impacted: 85"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_serial_ports(device_id: DeviceID, is_ethernet_device: bool = False) -> bool:
    """Check if the device has serial ports. Packets impacted: 182, 188, 195, 199"""
    return not (device_id == DeviceID.gnss_compass and is_ethernet_device)

def has_specified_packet_periods_port(device_id: DeviceID) -> bool:
    """Check if the device populates the ANPP181 Packet Periods fields 'portSpecified' and 'port'."""
    return device_id == DeviceID.gnss_compass

def has_sub_type(device_id: DeviceID) -> bool:
    """Check if the device has a subtype. Packets impacted: 13"""
    devices = {
        DeviceID.air_data_unit_v2,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d
    }
    return device_id in devices

def has_system_temperatures(device_id: DeviceID) -> bool:
    """Check if the device has system temperatures packet. Packets impacted: 86"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90
    }
    return device_id in devices

def has_velocity_heading_filter(device_id: DeviceID) -> bool:
    """Check if the velocity heading can be enabled/disabled. Packets impacted: 186"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_a,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.gnss_compass,
        DeviceID.motus,
        DeviceID.orientus,
        DeviceID.orientus_v3,
        DeviceID.spatial,
        DeviceID.spatial_dual,
        DeviceID.spatial_fog,
        DeviceID.spatial_fog_dual
    }
    return device_id in devices

def has_vessel_motion(device_id: DeviceID) -> bool:
    """Check if the device has the vessel motion packet. Packets impacted: 89"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus
    }
    return device_id in devices

def has_zero_angular_velocity(device_id: DeviceID) -> bool:
    """Check if the device has the zero angular velocity packet. Packets impacted: 83"""
    devices = {
        DeviceID.boreas_a50,
        DeviceID.boreas_a70,
        DeviceID.boreas_a90,
        DeviceID.boreas_d50,
        DeviceID.boreas_d70,
        DeviceID.boreas_d90,
        DeviceID.certus,
        DeviceID.certus_mini_n,
        DeviceID.certus_mini_d,
        DeviceID.motus,
        DeviceID.spatial_dual
    }
    return device_id in devices

def is_air_data_unit(device_id: DeviceID) -> bool:
    return device_id in AIR_DATA_UNIT_DEVICES

def is_boreas(device_id: DeviceID) -> bool:
    return device_id in BOREAS_DEVICES

def is_certus_mini(device_id: DeviceID) -> bool:
    return device_id in CERTUS_MINI_DEVICES

def is_gnss_firmware_update_allowed(gnss_manufacturer_id: int, gnss_receiver_model: int) -> bool:
    """Check if GNSS firmware update is allowed"""
    GNSS_MANUFACTURER_TRIMBLE = 1
    GNSS_MANUFACTURER_ADNAV = 5
    GNSS_RECEIVER_MODEL_ADNAV_ARIES_GC2 = 0
    GNSS_RECEIVER_MODEL_ADNAV_ARIES_SKYTRAQ_PX1172RH = 1

    if gnss_manufacturer_id == GNSS_MANUFACTURER_TRIMBLE:
        return True
    if gnss_manufacturer_id == GNSS_MANUFACTURER_ADNAV:
        if gnss_receiver_model in (GNSS_RECEIVER_MODEL_ADNAV_ARIES_GC2, GNSS_RECEIVER_MODEL_ADNAV_ARIES_SKYTRAQ_PX1172RH):
            return True
    return False

def is_ins(device_id: DeviceID) -> bool:
    return device_id in INS_DEVICES

def is_oem(device_id: DeviceID, device_sub_type: DeviceSubtype | None = None) -> bool:
    if device_id == DeviceID.certus:
        return device_sub_type in (CertusDeviceSubtype.certus_oem, CertusDeviceSubtype.certus_evo_oem)
    elif device_id in (DeviceID.certus_mini_a, DeviceID.certus_mini_d, DeviceID.certus_mini_n):
        return device_sub_type == CertusMiniDeviceSubtype.certus_mini_oem
    return False

def is_orientus(device_id: DeviceID) -> bool:
    return device_id in ORIENTUS_DEVICES
