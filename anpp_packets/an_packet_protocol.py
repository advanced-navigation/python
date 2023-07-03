################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            an_packet_protocol.py                           ##
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
import numpy as np
from dataclasses import dataclass, field
from typing import Final
from array import array
from struct import pack

from anpp_packets.an_packets import PacketID

AN_PACKET_HEADER_SIZE = 5
AN_MAXIMUM_PACKET_SIZE = 255
AN_DECODE_BUFFER_SIZE = 10 * (AN_MAXIMUM_PACKET_SIZE + AN_PACKET_HEADER_SIZE)

# fmt: off
crc16_table: Final = np.array([
    0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
    0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
    0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
    0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
    0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
    0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
    0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
    0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
    0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
    0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
    0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
    0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
    0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
    0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
    0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
    0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
    0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
    0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
    0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
    0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
    0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
    0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
    0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
    0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
    0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
    0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
    0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
    0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
    0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
    0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
    0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
    0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
], dtype=np.uint16)
# fmt: on


def calculate_header_lrc(data: bytes):
    """Takes in byte array and returns LRC"""
    lrc = ((data[0] + data[1] + data[2] + data[3]) ^ 0xFF) + 1
    return lrc & 0xFF


def calculate_crc16(data: bytes):
    """Takes in byte array and returns crc16 value of data"""
    crc = 0xFFFF
    for i in range(0, len(data)):
        crc = ((crc << 8) & 0xFFFF) ^ (crc16_table[(crc >> 8) ^ data[i]])
    return crc


@dataclass()
class ANDecoder:
    """Byte array used to store received binary data to be decoded"""

    buffer: bytearray = field(default_factory=bytearray)
    crc_errors: int = 0

    def add_data(self, packet_bytes):
        """Add data bytes to the buffer"""
        self.buffer.extend(packet_bytes)


@dataclass()
class ANPacket:
    """Class containing Advanced Navigation Packet Protocol packet structure"""

    id: PacketID = PacketID.acceleration
    length: int = 0
    header: bytearray = field(default_factory=bytearray)
    data: bytearray = field(default_factory=bytearray)

    def encode(self, id_: PacketID, length_: int, data_: bytearray):
        """Assign attribute values and calculate header"""
        self.id = id_
        self.length = length_ & 0xFF
        self.data = data_

        crc = pack("<H", calculate_crc16(self.data))
        lrc = calculate_header_lrc(bytes([self.id.value, self.length, crc[0], crc[1]]))

        self.header = bytearray(
            pack("<BBBBB", lrc, self.id.value, self.length, crc[0], crc[1])
        )

    def bytes(self):
        """Returns the packet as byte array"""
        return self.header + self.data


def an_packet_decode(an_decoder: ANDecoder):
    """Takes binary data byte array consisting of ANPP packets. Returns tuple
    consisting of first ANPP packet found and inputted byte array with the first
    ANPP packet returned and data before this packet, removed."""
    decode_iterator = 0
    an_packet = ANPacket()
    decoder_data = an_decoder

    buffer_length = len(an_decoder.buffer)

    while (decode_iterator + AN_PACKET_HEADER_SIZE) <= buffer_length:
        header_lrc = an_decoder.buffer[decode_iterator]
        header_data = an_decoder.buffer[
            decode_iterator + 1 : decode_iterator + AN_PACKET_HEADER_SIZE
        ]

        if header_lrc == calculate_header_lrc(header_data):
            id_val = header_data[0]
            id_ = PacketID(id_val) if id_val in PacketID._value2member_map_ else id_val

            length = header_data[1]
            crc = header_data[2] | (header_data[3] << 8)

            data_start = decode_iterator + AN_PACKET_HEADER_SIZE
            data_end = data_start + length

            if data_end > buffer_length:
                break

            if crc == calculate_crc16(an_decoder.buffer[data_start:data_end]):
                an_packet.id = id_
                an_packet.length = length
                an_packet.header = bytearray(
                    an_decoder.buffer[decode_iterator:data_start]
                )
                an_packet.data = bytearray(an_decoder.buffer[data_start:data_end])

                decode_iterator += AN_PACKET_HEADER_SIZE + int(an_packet.length)
                decoder_data.buffer = an_decoder.buffer[decode_iterator:]
                break
            else:
                decoder_data.crc_errors += 1
        decode_iterator += 1

    if decode_iterator > buffer_length:
        decoder_data = None

    return an_packet, decoder_data
