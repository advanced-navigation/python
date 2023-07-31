################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_7.py                               ##
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

from dataclasses import dataclass, field
from enum import Enum
import struct
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket
from typing import List


class DataEncoding(Enum):
    """Data Encoding"""

    binary = 0
    aes256 = 1


class FileTransferMetadata(Enum):
    """File Transfer Metadata"""

    none = 0
    extended_anpp = 1
    utf8_filename = 2
    an_firmware = 3


@dataclass()
class FileTransferFirstPacket:
    """Packet 7 - File Transfer Request Packet"""

    unique_id: int = 0
    data_index: int = 0
    total_size: int = 0
    data_encoding: DataEncoding = DataEncoding.binary
    metadata_type: FileTransferMetadata = FileTransferMetadata.none
    metadata: bytes = field(default_factory=bytes, repr=False)
    packet_data: bytes = field(default_factory=bytes, repr=False)

    ID = PacketID.file_transfer_request

    _structure = struct.Struct("<IIIBB")

    def encode(self) -> ANPacket:
        """Encode File Transfer Request Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.unique_id,
            self.data_index,
            self.total_size,
            self.data_encoding.value,
            self.metadata_type.value,
        )
        data += self.metadata
        data += self.packet_data

        an_packet = ANPacket()
        an_packet.encode(self.ID, len(data), data)

        return an_packet
