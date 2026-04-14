################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            encode_decode_test.py                           ##
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
import importlib
import inspect

from advanced_navigation.anpp_packets.an_packet_protocol import ANDecoder
from advanced_navigation.anpp_packets import __all__ as anpp_all


packet_classes = []
for module_name in anpp_all:
    if not module_name.startswith('an_packet_'):
        continue
    module = importlib.import_module(f'advanced_navigation.anpp_packets.{module_name}')
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if hasattr(obj, 'ID') and obj.__module__ == module.__name__:
            if name in ['StatusPacketAdu2', 'RawSensorsPacketAdu', 'FileTransferFirstPacket', 'AcknowledgePacket']:
                continue
            packet_classes.append(obj)
            
@pytest.mark.parametrize("packet_class", packet_classes)
def test_encode_decode_packets(packet_class):
    packet = packet_class()
    encode = getattr(packet, "encode", None)
    decode = getattr(packet, "decode", None)
    if callable(encode) and callable(decode):
        decoder = ANDecoder()
        data = packet.encode().bytes()
        decoder.add_data(data)
        an_packet = decoder.decode()
        new_packet = packet_class()
        assert an_packet is not None, "ANPacket is none"
        new_packet.decode(an_packet)
        assert new_packet == packet, packet_class.ID.name
