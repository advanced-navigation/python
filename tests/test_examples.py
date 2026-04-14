################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               test_examples.py                             ##
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
import math
from unittest.mock import patch

from examples.packet_printers import (
    print_packet,
    get_device_specific_packet_obj,
    handle_raw_an_packet
)
from advanced_navigation.anpp_packets.an_packet_3 import DeviceID
from advanced_navigation.anpp_packets.an_packet_20 import SystemStatePacket
from advanced_navigation.anpp_packets.an_packet_28 import RawSensorsPacket, RawSensorsPacketAdu
from advanced_navigation.anpp_packets.an_packet_23 import StatusPacket, StatusPacketAdu2
from advanced_navigation.anpp_packets.an_packet_protocol import ANPacket

class TestPacketPrinters:

    @patch('builtins.print')
    def test_print_packet(self, mock_print):
        import json
        from dataclasses import asdict
        packet = SystemStatePacket()
        packet.unix_time_seconds = 1700000000
        packet.microseconds = 500000
        packet.latitude = math.radians(45.0)
        packet.longitude = math.radians(-90.0)
        packet.height = 100.0
        packet.orientation = [math.radians(10.0), math.radians(20.0), math.radians(30.0)]
        packet.velocity = [1.0, 2.0, 3.0]
        
        print_packet(packet)
        
        expected_json = json.dumps(asdict(packet), default=str)
        mock_print.assert_any_call(f"[SystemStatePacket] {expected_json}")

    @patch('builtins.print')
    def test_print_packet_exception(self, mock_print):
        # Create a mock packet that causes an exception in asdict
        class MockPacket:
            ID = type('EnumLike', (), {'value': 999})
            LENGTH = 10
            # No __dataclass_fields__ so asdict will raise TypeError
        
        packet = MockPacket()
        print_packet(packet)
        mock_print.assert_any_call("Received Packet ID 999 (Length: 10)")

    @pytest.mark.parametrize("packet_id, device_id, expected_type", [
        (23, DeviceID.air_data_unit_v2, StatusPacketAdu2),
        (23, DeviceID.certus, StatusPacket),
        (28, DeviceID.air_data_unit, RawSensorsPacketAdu),
        (28, DeviceID.certus, RawSensorsPacket),
        (20, DeviceID.certus, SystemStatePacket),
    ])
    def test_get_device_specific_packet_obj(self, packet_id, device_id, expected_type):
        obj = get_device_specific_packet_obj(packet_id, device_id)
        assert isinstance(obj, expected_type)

    @patch('examples.packet_printers.print_packet')
    def test_handle_raw_an_packet(self, mock_print_packet):
        import struct
        
        # Build the byte representation manually since there is no encode() function
        data = struct.pack("<ffffffffffff", 
                           1.0, 2.0, 3.0, 
                           0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0)
                           
        raw_an_packet = ANPacket()
        raw_an_packet.id = 28
        raw_an_packet.length = 48
        raw_an_packet.data = data
        
        handle_raw_an_packet(raw_an_packet, DeviceID.certus)
        
        mock_print_packet.assert_called_once()
        args, _ = mock_print_packet.call_args
        assert isinstance(args[0], RawSensorsPacket)
        assert args[0].accelerometers == [1.0, 2.0, 3.0]
