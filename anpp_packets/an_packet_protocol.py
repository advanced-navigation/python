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

from dataclasses import dataclass, field
from ctypes import c_byte, c_uint16, c_uint32
from typing import Final
from array import array
from struct import pack

AN_PACKET_HEADER_SIZE = 5
AN_MAXIMUM_PACKET_SIZE = 255
AN_DECODE_BUFFER_SIZE = 10*(AN_MAXIMUM_PACKET_SIZE + AN_PACKET_HEADER_SIZE)

crc16_table: Final = array('I',
        [
            0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
            0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
            0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
            0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
            0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
            0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
            0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
            0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
            0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
            0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
            0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
            0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
            0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
            0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
            0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
            0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
            0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
            0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
            0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
            0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
            0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
            0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
            0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
            0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
            0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
            0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
            0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
            0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
            0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
            0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
            0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
            0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0
        ]
    )

""" Takes in byte array and returns LRC """
def calculate_header_lrc(data):
    lrc = (((data[0] + data[1] + data[2] + data[3]) ^ 0xFF) + 1)
    return (lrc & 0xff)

""" Takes byte array and returns crc16 value of data """
def calculate_crc16(data: bytearray):
    crc = 0xFFFF
    for i in range(0, len(data)):
        crc = (((crc << 8) & 0xFFFF) ^ (crc16_table[(crc >> 8) ^ data[i]]))
    return crc

""" Byte array used to store received binary data to be decoded """
@dataclass()
class AN_Decoder:
    buffer: [c_byte] = field(default_factory=list)
    crc_errors: c_uint32 = 0

    def add_data(self, packet_bytes):
        self.buffer.extend(packet_bytes)


""" Class containing Advanced Navigation Packet Protocol packet structure """
@dataclass()
class AN_Packet:
    id: c_byte() = 0
    length: c_byte() = 0
    header: [c_byte] = field(default_factory=list)
    data: [c_byte] = field(default_factory=list)

    def encode(self, id_, length_, data_):
        self.id = id_
        self.length = length_
        self.data = data_

        crc = pack('<H',calculate_crc16(self.data))
        lrc = calculate_header_lrc([self.id, self.length, crc[0], crc[1]])

        self.header = pack('<BBBBB', lrc, self.id, self.length, crc[0], crc[1])

    def bytes(self):
        return (self.header + self.data)


""" Takes binary data byte array consisting of ANPP packets. Returns tuple
    consisting of first ANPP packet found and inputed byte array with the first
    ANPP packet returned and data before this packet, removed. """
def an_packet_decode(an_decoder: AN_Decoder):
    decode_iterator: c_uint16 = 0
    an_packet: AN_Packet = None
    decoder_data = an_decoder

    buffer_length = len(an_decoder.buffer)

    # Checks byte array is large enough to contain a full packet header for calculation
    while ((decode_iterator + AN_PACKET_HEADER_SIZE) < buffer_length):
        # Loop checks first five bytes from decode_iterator to see if they are a valid header as
        # defined in Advanced Navigation Product's Reference Manual.

        # First byte is Header LRC.
        header_lrc = an_decoder.buffer[(decode_iterator)]

        # Check byte is equal to the LRC value calculated by using the Packet Length and Packet ID.
        if (header_lrc == calculate_header_lrc(an_decoder.buffer[(decode_iterator + 1) : (decode_iterator + 5)])):
            # Calculated LRC says the five bytes are a valid header. Assigns the other bytes to the header structure.
            id_ = an_decoder.buffer[(decode_iterator + 1)]
            length = an_decoder.buffer[(decode_iterator + 2)]
            crc = an_decoder.buffer[(decode_iterator + 3)]
            crc |= an_decoder.buffer[(decode_iterator + 4)] << 8

            # Calculate start and end position of the packet's data
            data_start = decode_iterator + AN_PACKET_HEADER_SIZE
            data_end = data_start + length

            # Check if all packet information has been sent, otherwise break to wait for all data to be received.
            if (data_end > buffer_length):
                # Not enough packets in the byte array for full length of the packet. Break loop to stop checking.
                break

            # Check header's CRC value is equal to the calculated CRC value by passing in the packet data.
            if (crc == calculate_crc16(an_decoder.buffer[data_start : data_end])):
                # Create Advanced Navigation Packet to copy packet data into
                an_packet = AN_Packet()
                an_packet.id = id_
                an_packet.length = length
                an_packet.header = an_decoder.buffer[decode_iterator : AN_PACKET_HEADER_SIZE]
                an_packet.data = an_decoder.buffer[data_start : data_end]

                # Increment the iterator to the end of the ANPP packet
                decode_iterator += (AN_PACKET_HEADER_SIZE + an_packet.length)
                # Remove all data before the last byte of the ANPP packet
                decoder_data.buffer = an_decoder.buffer[decode_iterator : ]
                break
            else:
                # CRC error occurred
                decoder_data.crc_errors += 1
        # First byte did not match calculated LRC. Increment byte checked in byte array.
        decode_iterator += 1

    if (decode_iterator > buffer_length):
        decoder_data = None

    return an_packet, decoder_data;