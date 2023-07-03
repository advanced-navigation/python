################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_195.py                              ##
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
from struct import pack, unpack
from anpp_packets.an_packets import PacketID
from anpp_packets.an_packet_protocol import ANPacket


class GPIORate(Enum):
    """GPIO Rate"""

    gpio_rate_disabled = 0
    gpio_rate_0o1hz = 1
    gpio_rate_0o2hz = 2
    gpio_rate_0o5hz = 3
    gpio_rate_1hz = 4
    gpio_rate_2hz = 5
    gpio_rate_5hz = 6
    gpio_rate_10hz = 7
    gpio_rate_25hz = 8
    gpio_rate_50hz = 9


class PortInputMode(Enum):
    """Port Input Modes"""

    inactive = 0
    nmea_0183 = 6
    anpp = 11
    gnss_receiver_passthrough = 38


class PortOutputMode(Enum):
    """Port Output Modes"""

    inactive = 0
    nmea_0183 = 7
    anpp = 12
    gnss_receiver_passthrough = 38
    tss1 = 39
    simrad_1000 = 40
    simrad_3000 = 41


class NMEAFixBehaviour(Enum):
    """NMEA Fix Behaviour"""

    nmea_fix_behaviour_normal = 0
    nmea_fix_behaviour_always_3d = 1


@dataclass()
class GPIOOutputRate:
    """GPIO Output Rate"""

    gpio1_rate: GPIORate = GPIORate.gpio_rate_disabled
    auxiliary_rate: GPIORate = GPIORate.gpio_rate_disabled

    def unpack(self, data):
        """Unpack data bytes"""
        self.gpio1_rate = GPIORate(data & 0x00FF)
        self.auxiliary_rate = GPIORate((data & 0xFF00) >> 8)

    def pack(self):
        return pack("<HH", self.gpio1_rate.value, self.auxiliary_rate.value)


@dataclass()
class GPIOOutputConfigurationPacket:
    """Packet 195 - GPIO Output Configuration Packet"""

    permanent: int = 0
    port_input_mode: PortInputMode = PortInputMode.inactive
    port_output_mode: PortOutputMode = PortOutputMode.inactive
    nmea_fix_behaviour: NMEAFixBehaviour = NMEAFixBehaviour.nmea_fix_behaviour_normal
    gpzda_rate: GPIOOutputRate = GPIOOutputRate()
    gpgga_rate: GPIOOutputRate = GPIOOutputRate()
    gpvtg_rate: GPIOOutputRate = GPIOOutputRate()
    gprmc_rate: GPIOOutputRate = GPIOOutputRate()
    gphdt_rate: GPIOOutputRate = GPIOOutputRate()
    gpgll_rate: GPIOOutputRate = GPIOOutputRate()
    pashr_rate: GPIOOutputRate = GPIOOutputRate()
    tss1_rate: GPIOOutputRate = GPIOOutputRate()
    simrad_rate: GPIOOutputRate = GPIOOutputRate()
    gprot_rate: GPIOOutputRate = GPIOOutputRate()
    gphev_rate: GPIOOutputRate = GPIOOutputRate()
    gpgsv_rate: GPIOOutputRate = GPIOOutputRate()
    pfecatt_rate: GPIOOutputRate = GPIOOutputRate()
    pfechve_rate: GPIOOutputRate = GPIOOutputRate()
    pfechve_rate: GPIOOutputRate = GPIOOutputRate()
    gpgst: GPIOOutputRate = GPIOOutputRate()

    ID = PacketID.gpio_output_configuration
    LENGTH = 33

    def decode(self, an_packet: ANPacket):
        """Decode ANPacket to GPIO Output Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            self.permanent = an_packet.data[0]
            self.port_input_mode = PortInputMode(an_packet.data[1])
            self.port_output_mode = PortOutputMode(an_packet.data[2])
            self.nmea_fix_behaviour = NMEAFixBehaviour(an_packet.data[3])
            self.gpzda_rate.unpack(unpack("<B", bytes([an_packet.data[4]]))[0])
            self.gpgga_rate.unpack(unpack("<B", bytes([an_packet.data[5]]))[0])
            self.gpvtg_rate.unpack(unpack("<B", bytes([an_packet.data[6]]))[0])
            self.gprmc_rate.unpack(unpack("<B", bytes([an_packet.data[7]]))[0])
            self.gphdt_rate.unpack(unpack("<B", bytes([an_packet.data[8]]))[0])
            self.gpgll_rate.unpack(unpack("<B", bytes([an_packet.data[9]]))[0])
            self.pashr_rate.unpack(unpack("<B", bytes([an_packet.data[10]]))[0])
            self.tss1_rate.unpack(unpack("<B", bytes([an_packet.data[11]]))[0])
            self.simrad_rate.unpack(unpack("<B", bytes([an_packet.data[12]]))[0])
            self.gprot_rate.unpack(unpack("<B", bytes([an_packet.data[13]]))[0])
            self.gphev_rate.unpack(unpack("<B", bytes([an_packet.data[14]]))[0])
            self.gpgsv_rate.unpack(unpack("<B", bytes([an_packet.data[15]]))[0])
            self.pfecatt_rate.unpack(unpack("<B", bytes([an_packet.data[16]]))[0])
            self.pfechve_rate.unpack(unpack("<B", bytes([an_packet.data[17]]))[0])
            self.gpgst.unpack(unpack("<B", bytes([an_packet.data[18]]))[0])

            return 0
        else:
            return 1

    def encode(self):
        """Encode GPIO Output Configuration Packet to ANPacket
        Returns the ANPacket"""
        data = pack(
            "<BBIIIIIIIIIIIIIIBBB",
            self.permanent,
            self.nmea_fix_behaviour.value,
            self.gpzda_rate.pack(),
            self.gpgga_rate.pack(),
            self.gpvtg_rate.pack(),
            self.gprmc_rate.pack(),
            self.gphdt_rate.pack(),
            self.gpgll_rate.pack(),
            self.pashr_rate.pack(),
            self.tss1_rate.pack(),
            self.simrad_rate.pack(),
            self.gprot_rate.pack(),
            self.gphev_rate.pack(),
            self.gpgsv_rate.pack(),
            self.pfecatt_rate.pack(),
            self.pfechve_rate.pack(),
            0,
            0,
            0,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
