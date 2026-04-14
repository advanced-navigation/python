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

import pytest
import os
from pathlib import Path

from advanced_navigation.anpp_packets.an_packet_protocol import ANDecoder
from advanced_navigation.anpp_packets.an_packets import PacketID
from tests.anpp_packets_tests.test_utils import get_obj_from_enum


_DECODED_PACKET_IDS = None

def get_decoded_packet_ids():
    global _DECODED_PACKET_IDS
    if _DECODED_PACKET_IDS is not None:
        return _DECODED_PACKET_IDS
        
    packet_decoded = set()
    log_path = Path(os.path.dirname(os.path.abspath(__file__))).joinpath("Log.anpp")
    
    with open(log_path, "rb") as log:
        raw_data = log.read()
        
    decoder = ANDecoder()
    decoder.add_data(raw_data)
    
    while True:
        an_packet = decoder.decode()
        if an_packet is None:
            break
            
        new_packet = get_obj_from_enum(an_packet.id)
        if new_packet is not None:
            assert new_packet.decode(an_packet) == 0
            packet_decoded.add(new_packet.ID.value)
            
    _DECODED_PACKET_IDS = packet_decoded
    return _DECODED_PACKET_IDS


PACKETS_NOT_IN_LOG = [8, 10, 52, 60, 61, 67, 80, 86, 89, 92, 93, 94, 95, 96, 184, 190, 193, 206, 207, 208, 209]

TESTABLE_PACKET_IDS = []
for packet_id in PacketID._value2member_map_:
    packet = get_obj_from_enum(PacketID(packet_id))
    if packet is not None:
        decode = getattr(packet, "decode", None)
        if callable(decode) and packet_id not in PACKETS_NOT_IN_LOG:
            TESTABLE_PACKET_IDS.append(packet_id)

@pytest.mark.parametrize("packet_id", TESTABLE_PACKET_IDS)
def test_decode_packet_in_log(packet_id):
    decoded_ids = get_decoded_packet_ids()
    assert packet_id in decoded_ids, f"PacketID {packet_id} was expected to be decoded from Log.anpp but wasn't found."

