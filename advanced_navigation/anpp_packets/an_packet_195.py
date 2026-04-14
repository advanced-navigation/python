################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              an_packet_195.py                              ##
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
from typing import List
import struct
from struct import pack
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


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
    gpio_rate_8hz = 10


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
class GPIOPort:
    port_input_mode: PortInputMode = PortInputMode.inactive
    port_output_mode: PortOutputMode = PortOutputMode.inactive
    nmea_fix_behaviour: NMEAFixBehaviour = NMEAFixBehaviour.nmea_fix_behaviour_normal
    gpzda_rate: GPIORate = GPIORate.gpio_rate_disabled
    gpgga_rate: GPIORate = GPIORate.gpio_rate_disabled
    gpvtg_rate: GPIORate = GPIORate.gpio_rate_disabled
    gprmc_rate: GPIORate = GPIORate.gpio_rate_disabled
    gphdt_rate: GPIORate = GPIORate.gpio_rate_disabled
    gpgll_rate: GPIORate = GPIORate.gpio_rate_disabled
    pashr_rate: GPIORate = GPIORate.gpio_rate_disabled
    tss1_rate: GPIORate = GPIORate.gpio_rate_disabled
    simrad_rate: GPIORate = GPIORate.gpio_rate_disabled
    gprot_rate: GPIORate = GPIORate.gpio_rate_disabled
    gphev_rate: GPIORate = GPIORate.gpio_rate_disabled
    gpgsv_rate: GPIORate = GPIORate.gpio_rate_disabled
    pfecatt_rate: GPIORate = GPIORate.gpio_rate_disabled
    pfechve_rate: GPIORate = GPIORate.gpio_rate_disabled
    gpgst_rate: GPIORate = GPIORate.gpio_rate_disabled

    LENGTH = 18

    _structure = struct.Struct("<18B8x")

    def unpack(self, data):
        values = self._structure.unpack_from(data)
        self.port_input_mode = PortInputMode(values[0])
        self.port_output_mode = PortOutputMode(values[1])
        self.nmea_fix_behaviour = NMEAFixBehaviour(values[2])
        self.gpzda_rate = GPIORate(values[3])
        self.gpgga_rate = GPIORate(values[4])
        self.gpvtg_rate = GPIORate(values[5])
        self.gprmc_rate = GPIORate(values[6])
        self.gphdt_rate = GPIORate(values[7])
        self.gpgll_rate = GPIORate(values[8])
        self.pashr_rate = GPIORate(values[9])
        self.tss1_rate = GPIORate(values[10])
        self.simrad_rate = GPIORate(values[11])
        self.gprot_rate = GPIORate(values[12])
        self.gphev_rate = GPIORate(values[13])
        self.gpgsv_rate = GPIORate(values[11])
        self.pfecatt_rate = GPIORate(values[15])
        self.pfechve_rate = GPIORate(values[16])
        self.gpgst_rate = GPIORate(values[17])

    def pack(self) -> bytes:
        data = self._structure.pack(
            self.port_input_mode,
            self.port_output_mode,
            self.nmea_fix_behaviour,
            self.gpzda_rate,
            self.gpgga_rate,
            self.gpvtg_rate,
            self.gprmc_rate,
            self.gphdt_rate,
            self.gpgll_rate,
            self.pashr_rate,
            self.tss1_rate,
            self.simrad_rate,
            self.gprot_rate,
            self.gphev_rate,
            self.gpgsv_rate,
            self.pfecatt_rate,
            self.pfechve_rate,
            self.gpgst_rate,
        )
        return data


@dataclass()
class GPIOOutputConfigurationPacket:
    """Packet 195 - GPIO Output Configuration Packet"""

    permanent: int = 0
    gpio_1: GPIOPort = field(default_factory=GPIOPort, repr=False)
    gpio_3: GPIOPort = field(default_factory=GPIOPort, repr=False)
    logging: GPIOPort | None = None
    data_ports: List[GPIOPort] | None = None

    ID = PacketID.gpio_output_configuration

    LENGTH_V1 = 33
    LENGTH_V2 = 183
    LENGTH_GPIO = 26

    _structure_v1 = struct.Struct("<BBBxBxBxBxBxBxBxBxBxBxBxBxBxBxBxx")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to GPIO Output Configuration Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH_V2):
            self.permanent = an_packet.data[0]

            self.gpio_3.unpack(an_packet.data[1:27])
            self.gpio_1.unpack(an_packet.data[27:53])

            self.logging = GPIOPort()
            self.logging.unpack(an_packet.data[53:79])

            self.data_ports = [GPIOPort(), GPIOPort(), GPIOPort(), GPIOPort()]
            for i, port in enumerate(self.data_ports):
                offset = i * 26
                port.unpack(an_packet.data[79 + offset: 105 + offset])
            return 0

        elif (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH_V1):
            values = self._structure_v1.unpack_from(an_packet.data)
            self.permanent = values[0]
            self.gpio_1.nmea_fix_behaviour = (
                self.gpio_3.nmea_fix_behaviour
            ) = NMEAFixBehaviour(values[1])
            self.gpio_1.gpzda_rate = GPIORate(values[2])
            self.gpio_3.gpzda_rate = GPIORate((values[2] & 0xFF) >> 4)
            self.gpio_1.gpgga_rate = GPIORate(values[3])
            self.gpio_3.gpgga_rate = GPIORate((values[3] & 0xFF) >> 4)
            self.gpio_1.gpvtg_rate = GPIORate(values[4])
            self.gpio_3.gpvtg_rate = GPIORate((values[4] & 0xFF) >> 4)
            self.gpio_1.gprmc_rate = GPIORate(values[5])
            self.gpio_3.gprmc_rate = GPIORate((values[5] & 0xFF) >> 4)
            self.gpio_1.gphdt_rate = GPIORate(values[6])
            self.gpio_3.gphdt_rate = GPIORate((values[6] & 0xFF) >> 4)
            self.gpio_1.gpgll_rate = GPIORate(values[7])
            self.gpio_3.gpgll_rate = GPIORate((values[7] & 0xFF) >> 4)
            self.gpio_1.pashr_rate = GPIORate(values[8])
            self.gpio_3.pashr_rate = GPIORate((values[8] & 0xFF) >> 4)
            self.gpio_1.tss1_rate = GPIORate(values[9])
            self.gpio_3.tss1_rate = GPIORate((values[9] & 0xFF) >> 4)
            self.gpio_1.simrad_rate = GPIORate(values[10])
            self.gpio_3.simrad_rate = GPIORate((values[10] & 0xFF) >> 4)
            self.gpio_1.gprot_rate = GPIORate(values[11])
            self.gpio_3.gprot_rate = GPIORate((values[11] & 0xFF) >> 4)
            self.gpio_1.gphev_rate = GPIORate(values[12])
            self.gpio_3.gphev_rate = GPIORate((values[12] & 0xFF) >> 4)
            self.gpio_1.gpgsv_rate = GPIORate(values[13])
            self.gpio_3.gpgsv_rate = GPIORate((values[13] & 0xFF) >> 4)
            self.gpio_1.pfecatt_rate = GPIORate(values[14])
            self.gpio_3.pfecatt_rate = GPIORate((values[14] & 0xFF) >> 4)
            self.gpio_1.pfechve_rate = GPIORate(values[15])
            self.gpio_3.pfechve_rate = GPIORate((values[15] & 0xFF) >> 4)
            self.gpio_1.gpgst_rate = GPIORate(values[16])
            self.gpio_3.gpgst_rate = GPIORate((values[16] & 0xFF) >> 4)

            return 0

        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode GPIO Output Configuration Packet to ANPacket
        Returns the ANPacket"""

        if self.logging is not None and self.data_ports is not None:
            data = pack("<B", self.permanent)
            data += self.gpio_1.pack()
            data += self.gpio_3.pack()
            data += self.logging.pack()
            for port in self.data_ports:
                data += port.pack()

            an_packet = ANPacket()
            an_packet.encode(self.ID, self.LENGTH_V2, data)

        else:
            data = self._structure_v1.pack(
                self.permanent,
                self.gpio_1.nmea_fix_behaviour.value,
                self.gpio_1.gpzda_rate.value | (self.gpio_3.gpzda_rate.value << 4),
                self.gpio_1.gpgga_rate.value | (self.gpio_3.gpgga_rate.value << 4),
                self.gpio_1.gpvtg_rate.value | (self.gpio_3.gpvtg_rate.value << 4),
                self.gpio_1.gprmc_rate.value | (self.gpio_3.gprmc_rate.value << 4),
                self.gpio_1.gphdt_rate.value | (self.gpio_3.gphdt_rate.value << 4),
                self.gpio_1.gpgll_rate.value | (self.gpio_3.gpgll_rate.value << 4),
                self.gpio_1.pashr_rate.value | (self.gpio_3.pashr_rate.value << 4),
                self.gpio_1.tss1_rate.value | (self.gpio_3.tss1_rate.value << 4),
                self.gpio_1.simrad_rate.value | (self.gpio_3.simrad_rate.value << 4),
                self.gpio_1.gprot_rate.value | (self.gpio_3.gprot_rate.value << 4),
                self.gpio_1.gphev_rate.value | (self.gpio_3.gphev_rate.value << 4),
                self.gpio_1.gpgsv_rate.value | (self.gpio_3.gpgsv_rate.value << 4),
                self.gpio_1.pfecatt_rate.value | (self.gpio_3.pfecatt_rate.value << 4),
                self.gpio_1.pfechve_rate.value | (self.gpio_3.pfechve_rate.value << 4),
                self.gpio_1.gpgst_rate.value | (self.gpio_3.gpgst_rate.value << 4),
            )

            an_packet = ANPacket()
            an_packet.encode(self.ID, self.LENGTH_V1, data)

        return an_packet
