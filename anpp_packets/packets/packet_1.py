################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                                 packet_1.py                                ##
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

""" Acknowledge Packet 1, as defined in Advance Navigation Reference Manuals """

from struct import pack
from dataclasses import dataclass, field
from anpp_packets.packets.an_packet_protocol import AN_Packet
from anpp_packets.packets.anpp_packets import PacketID

class RequestPacket():
    @dataclass()
    class RequestPacket:
        def encode(self, requested_packets):
            data = bytes()
            print(f"requested_packets: {requested_packets}")

            if(isinstance(requested_packets, int)):
                requested_packets = [requested_packets]

            for packet in requested_packets:
                data += pack('<B', packet)

            an_packet = AN_Packet()
            an_packet.encode(PacketID.PacketID.request.value, len(data), data)

            return an_packet