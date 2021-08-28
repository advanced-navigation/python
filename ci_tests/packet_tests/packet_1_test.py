################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              packet_1_test.py                              ##
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
from anpp_packets.packets.packet_1 import RequestPacket

def test_request_packet():
    packet = RequestPacket.RequestPacket()

    # Test encode handles single interger
    check = packet.encode(2)
    assert check.id == 1
    assert check.length == 1
    assert check.header == b'\x8b\x01\x01\xb2\xc1'
    assert check.data == b'\x02'

    # Test encode handles single list value
    check = packet.encode([2])
    assert check.id == 1
    assert check.length == 1
    assert check.header == b'\x8b\x01\x01\xb2\xc1'
    assert check.data == b'\x02'

    # Test encode handles multiple value list
    check = packet.encode([2,3,182])
    assert check.id == 1
    assert check.length == 3
    assert check.header == b'\x1a\x01\x03\xb20'
    assert check.data == b'\x02\x03\xb6'