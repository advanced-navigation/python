################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              packet_0_test.py                              ##
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

from anpp_packets.packets.an_packet_protocol import AN_Packet
from anpp_packets.packets.packet_0 import AcknowledgePacket, AcknowledgeResult

# Dummy Test for now
def test_acknowledge_packet():
    packet = AcknowledgePacket.AcknowledgePacket()
    raw_packet = AN_Packet()
    raw_packet.id = 0
    raw_packet.length = 4

    # Sensor Ranges Packet 184, returned with result: success
    raw_packet.header = b'\x82\x00\x04y\x01'
    raw_packet.data = b'\xb8\xc0\x84\x00'
    assert packet.decode(raw_packet) == 0
    assert packet.packet_id == 184
    assert packet.packet_crc == 33984
    assert packet.acknowledge_result.value == AcknowledgeResult.AcknowledgeResult.success.value

    # Installation Alignment Packet 185, returned with result: failure CRC
    raw_packet.header = b'\xa9\x00\x04\xecg'
    raw_packet.data = b'\xb9\xc0\x84\x01'
    assert packet.decode(raw_packet) == 0
    assert packet.packet_id == 185
    assert packet.packet_crc == 33984
    assert packet.acknowledge_result.value == AcknowledgeResult.AcknowledgeResult.failure_crc.value

    # Filter Options Packet 186, returned with result: failure length
    raw_packet.header = b'*\x00\x04kg'
    raw_packet.data = b'\xba\xec\xc7\x02'
    assert packet.decode(raw_packet) == 0
    assert packet.packet_id == 186
    assert packet.packet_crc == 51180
    assert packet.acknowledge_result.value == AcknowledgeResult.AcknowledgeResult.failure_length.value

    # Test decode fails for wrong packet received
    raw_packet.id = 3
    assert packet.decode(raw_packet) == 1

    # Test decode fails for wrong packet length
    raw_packet.id = 0
    raw_packet.data = b'\xb8\xc0\x84\x00\x00'
    assert packet.decode(raw_packet) == 1