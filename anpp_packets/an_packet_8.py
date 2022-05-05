################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_8.py                               ##
##                     Copyright 2022, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2022 Advanced Navigation                                       #
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

from dataclasses import dataclass
from enum import Enum
from struct import unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


class FileTransferResponse(Enum):
    """File Transfer Response"""
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


@dataclass()
class FileTransferAcknowledgePacket:
    """Packet 8 - File Transfer Acknowledge Packet"""
    unique_id: int = 0
    data_index: int = 0
    response_code: FileTransferResponse = FileTransferResponse.completed_successfully

    ID = PacketID.file_transfer_acknowledge
    LENGTH = 9

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to File Transfer Acknowledge Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.unique_id = unpack('<I', an_packet.data[0:4])[0]
            self.data_index = unpack('<I', an_packet.data[4:8])[0]
            self.response_code = FileTransferResponse(an_packet.data[8])
            return 0
        else:
            return 1