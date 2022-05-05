################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_68.py                              ##
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
from struct import pack, unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


@dataclass()
class ExternalAirDataFlags:
    """External Air Data Flags"""
    barometric_altitude_set_and_valid: bool = False
    airspeed_set_and_valid: bool = False
    barometric_altitude_reference_reset: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.barometric_altitude_set_and_valid = (data & (1 << 0)) != 0
        self.airspeed_set_and_valid = (data & (1 << 1)) != 0
        self.barometric_altitude_reference_reset = (data & (1 << 2)) != 0

    def pack(self):
        """Pack to data bytes"""
        return (self.barometric_altitude_set_and_valid << 0) \
               & (self.airspeed_set_and_valid << 1) \
               & (self.barometric_altitude_reference_reset << 2)


@dataclass()
class ExternalAirDataPacket:
    """Packet 68 - External Air Data Packet"""
    barometric_altitude_delay: float = 0
    airspeed_delay: float = 0
    barometric_altitude: float = 0
    airspeed: float = 0
    barometric_altitude_standard_deviation: float = 0
    airspeed_standard_deviation: float = 0
    flags: ExternalAirDataFlags = ExternalAirDataFlags()

    ID = PacketID.external_air_data
    LENGTH = 25

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to External Air Data Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.barometric_altitude_delay = unpack('<f', bytes(an_packet.data[0:4]))[0]
            self.airspeed_delay = unpack('<f', bytes(an_packet.data[4:8]))[0]
            self.barometric_altitude = unpack('<f', bytes(an_packet.data[8:12]))[0]
            self.airspeed = unpack('<f', bytes(an_packet.data[12:16]))[0]
            self.barometric_altitude_standard_deviation = unpack('<f', bytes(an_packet.data[16:20]))[0]
            self.airspeed_standard_deviation = unpack('<f', bytes(an_packet.data[20:24]))[0]
            self.flags.unpack(an_packet.data[24])
            return 0
        else:
            return 1

    def encode(self):
        """Encode External Air Data Packet to ANPacket
        Returns the ANPacket"""
        data = pack('<f', self.barometric_altitude_delay)
        data += pack('<f', self.airspeed_delay)
        data += pack('<f', self.barometric_altitude)
        data += pack('<f', self.airspeed)
        data += pack('<f', self.barometric_altitude_standard_deviation)
        data += pack('<f', self.airspeed_standard_deviation)
        data += pack('<B', self.flags.pack())

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet


@dataclass()
class AirDataFlags:
    """Air Data Flags"""
    barometric_altitude_valid: bool = False
    airspeed_valid: bool = False
    barometric_altitude_sensor_over_range: bool = False
    airspeed_sensor_overrange: bool = False
    barometric_altitude_sensor_failure: bool = False
    airspeed_sensor_failure: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.barometric_altitude_valid = (data & (1 << 0)) != 0
        self.airspeed_valid = (data & (1 << 1)) != 0
        self.barometric_altitude_sensor_over_range = (data & (1 << 2)) != 0
        self.airspeed_sensor_overrange = (data & (1 << 3)) != 0
        self.barometric_altitude_sensor_failure = (data & (1 << 4)) != 0
        self.airspeed_sensor_failure = (data & (1 << 5)) != 0


@dataclass()
class AirDataPacket:
    """Packet 68 - Air Data Packet"""
    barometric_altitude_delay: float = 0
    airspeed_delay: float = 0
    barometric_altitude: float = 0
    airspeed: float = 0
    barometric_altitude_standard_deviation: float = 0
    airspeed_standard_deviation: float = 0
    flags: AirDataFlags = AirDataFlags()

    ID = PacketID.external_air_data
    LENGTH = 25

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to Air Data Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.barometric_altitude_delay = unpack('<f', bytes(an_packet.data[0:4]))[0]
            self.airspeed_delay = unpack('<f', bytes(an_packet.data[4:8]))[0]
            self.barometric_altitude = unpack('<f', bytes(an_packet.data[8:12]))[0]
            self.airspeed = unpack('<f', bytes(an_packet.data[12:16]))[0]
            self.barometric_altitude_standard_deviation = unpack('<f', bytes(an_packet.data[16:20]))[0]
            self.airspeed_standard_deviation = unpack('<f', bytes(an_packet.data[20:24]))[0]
            self.flags.unpack(an_packet.data[24])
            return 0
        else:
            return 1
