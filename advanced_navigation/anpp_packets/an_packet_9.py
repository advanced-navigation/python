################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_9.py                               ##
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
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket
from enum import Enum

class FileTransferDataEncoding(Enum):
    """File Transfer Data Encoding"""

    binary = 0
    aes256 = 1

class FileTransferMetadataType(Enum):
    """File Transfer Metadata Type"""
    
    none = 0
    extended_anpp = 1
    utf8_filename = 2
    an_firmware = 3

class FileTransferLimits(Enum):
    max_data_size = 224

@dataclass()
class FileTransferFirstPacket:
    """Packet 9 - File Transfer Ongoing Packet"""

    unique_id: int = 0
    data_index: int = 0
    total_size: int = 0
    data_encoding: FileTransferDataEncoding = FileTransferDataEncoding.aes256
    metadata_type: FileTransferMetadataType = FileTransferMetadataType.an_firmware
    metadata_length: int = FileTransferLimits.max_data_size.value
    packet_data: bytes = field(default_factory=bytes, repr=False)

    ID = PacketID.file_transfer

    _structure = struct.Struct("<IIIBBH")

    def encode(self) -> ANPacket:
        """Encode File Transfer First Packet to ANPacket
        Returns the ANPacket"""

        if len(self.packet_data) > FileTransferLimits.max_data_size.value:
            raise Exception("File data exceeds maximum length")

        data = self._structure.pack(self.unique_id, 
                                    self.data_index,
                                    self.total_size,
                                    self.data_encoding.value,
                                    self.metadata_type.value,
                                    self.metadata_length)
        data += self.packet_data

        an_packet = ANPacket()
        an_packet.encode(self.ID, len(data), data)

        return an_packet

@dataclass()
class FileTransferOngoingPacket:
    """Packet 9 - File Transfer Ongoing Packet"""

    unique_id: int = 0
    data_index: int = 0
    packet_data: bytes = field(default_factory=bytes, repr=False)

    ID = PacketID.file_transfer

    _structure = struct.Struct("<II")

    def encode(self) -> ANPacket:
        """Encode File Transfer Ongoing Packet to ANPacket
        Returns the ANPacket"""

        if len(self.packet_data) > FileTransferLimits.max_data_size.value:
            raise Exception("File data exceeds maximum length")
    
        data = self._structure.pack(self.unique_id, self.data_index)
        data += self.packet_data

        an_packet = ANPacket()
        an_packet.encode(self.ID, len(data), data)

        return an_packet
