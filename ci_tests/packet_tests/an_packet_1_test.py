################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            an_packet_1_test.py                             ##
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

from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_1 import RequestPacket


def test_request_packet():
    # Test encode handles single ID
    check = RequestPacket(PacketID(2)).encode()
    assert check.id == PacketID.request
    assert check.length == 1
    assert check.header == b'\x8b\x01\x01\xb2\xc1'
    assert check.data == b'\x02'

    # Test encode handles attribute editing
    packet = RequestPacket()
    packet.requested_packets = [PacketID.boot_mode]
    check = packet.encode()
    assert check.id == PacketID(1)
    assert check.length == 1
    assert check.header == b'\x8b\x01\x01\xb2\xc1'
    assert check.data == b'\x02'

    # Test encode handles single value list
    check = RequestPacket([PacketID.boot_mode]).encode()
    assert check.id == PacketID.request
    assert check.length == 1
    assert check.header == b'\x8b\x01\x01\xb2\xc1'
    assert check.data == b'\x02'

    # Test encode handles multiple value list
    check = RequestPacket([PacketID(2), PacketID(3), PacketID(182)]).encode()
    assert check.id == PacketID.request
    assert check.length == 3
    assert check.header == b'\x1a\x01\x03\xb20'
    assert check.data == b'\x02\x03\xb6'
