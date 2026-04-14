################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            test_capabilities.py                            ##
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

import pytest
from advanced_navigation.anpp_packets.an_packet_3 import DeviceID
from advanced_navigation.anpp_packets.an_packet_13 import CertusDeviceSubtype
from advanced_navigation.anpp_packets.an_packets import PacketID
from advanced_navigation.an_devices import (
    has_magnetometer,
    get_primary_baud_rate_array,
    get_supported_packets,
    has_sub_type,
    is_oem
)

@pytest.mark.parametrize("device_id, expected", [
    (DeviceID.certus, True),
    (DeviceID.air_data_unit, False),
])
def test_capabilities_magnetometer(device_id, expected):
    assert has_magnetometer(device_id) is expected

@pytest.mark.parametrize("device_id, expected_in, expected_not_in", [
    (DeviceID.spatial_fog, ["10000000"], []),
    (DeviceID.certus, ["4000000"], ["10000000"]),
])
def test_capabilities_baud_rates(device_id, expected_in, expected_not_in):
    baud_rates = get_primary_baud_rate_array(device_id)
    for rate in expected_in:
        assert rate in baud_rates
    for rate in expected_not_in:
        assert rate not in baud_rates

@pytest.mark.parametrize("device_id, expected_packets", [
    (DeviceID.certus, [PacketID.system_state, PacketID.device_information]),
])
def test_capabilities_supported_packets(device_id, expected_packets):
    packets = get_supported_packets(device_id)
    for packet in expected_packets:
        assert packet in packets

@pytest.mark.parametrize("device_id, expected", [
    (DeviceID.boreas_d90, True),
    (DeviceID.certus, True),
    (DeviceID.gnss_compass, False),
])
def test_capabilities_sub_type(device_id, expected):
    assert has_sub_type(device_id) is expected

@pytest.mark.parametrize("device_id, sub_type, expected", [
    (DeviceID.certus, CertusDeviceSubtype.certus_oem, True),
    (DeviceID.certus, CertusDeviceSubtype.certus_evo, False),
])
def test_capabilities_oem(device_id, sub_type, expected):
    assert is_oem(device_id, sub_type) is expected
