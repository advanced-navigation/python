################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_69.py                              ##
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
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


class GNSSManufacturerID(Enum):
    """GNSS Manufacturer ID"""

    unknown = 0
    trimble = 1
    advanced_navigation = 3


class TrimbleGNSSReceiverModel(Enum):
    """Trimble GNSS Receiver Model"""

    unknown = 0
    trimble_bd920 = 1
    trimble_bd930 = 2
    trimble_bd982 = 3
    trimble_mb_one = 4
    trimble_mb_two = 5
    trimble_bd940 = 6
    trimble_bd992 = 7


class AdvancedNavigationGNSSReceiverModel(Enum):
    """Advanced Navigation GNSS Receiver Model"""

    unknown = 0
    aries = 1
    aries_gc2 = 2


class OmnistarEngineMode(Enum):
    """Omnistar Engine Mode"""

    inactive = 0
    hp = 1
    xp = 2
    g2 = 3
    hp_g2 = 4
    hp_xp = 5


class RTKSoftwareLicenseAccuracy(Enum):
    """RTK Software License Accuracy"""

    unknown = 0
    hor_0_3m_ver_0_3m = 1
    hor_0_1m_ver_0_1m = 2
    hor_0_1m_ver_0_02m = 3
    hor_0_008m_ver_0_1m = 4
    hor_0_008m_ver_0_02m = 5


@dataclass()
class AdvancedNavigationGNSSReceiverInformation:
    """Advanced Navigation GNSS Receiver Information"""

    gnss_manufacturer_id: GNSSManufacturerID = GNSSManufacturerID.unknown
    gnss_receiver_model: AdvancedNavigationGNSSReceiverModel = (
        AdvancedNavigationGNSSReceiverModel.unknown
    )
    serial_number: bytes = field(default_factory=lambda: bytes([0] * 24), repr=False)
    firmware_version: int = 0
    hardware_version: int = 0

    LENGTH = 68

    _structure = struct.Struct("<BB24bII")

    def unpack(self, data):
        values = self._structure.unpack_from(data)
        self.gnss_manufacturer_id = GNSSManufacturerID(values[0])
        self.gnss_receiver_model = AdvancedNavigationGNSSReceiverModel(values[1])
        self.serial_number = bytes(values[2:26])
        (
            self.firmware_version,
            self.hardware_version,
        ) = values[26:28]


@dataclass()
class TrimbleGNSSReceiverInformation:
    """Trimble GNSS Receiver Information"""

    gnss_manufacturer_id: GNSSManufacturerID = GNSSManufacturerID.unknown
    gnss_receiver_model: TrimbleGNSSReceiverModel = TrimbleGNSSReceiverModel.unknown
    serial_number: bytes = field(default_factory=lambda: bytes([0] * 10), repr=False)
    firmware_version: int = 0
    software_license_code: List[int] = field(
        default_factory=lambda: [0, 0, 0], repr=False
    )
    omnistar_serial_number: int = 0
    omnistar_subscription_start_unix_time: int = 0
    omnistar_subscription_expiry_unix_time: int = 0
    omnistar_engine_mode: OmnistarEngineMode = OmnistarEngineMode.inactive
    rtk_software_license_accuracy: RTKSoftwareLicenseAccuracy = (
        RTKSoftwareLicenseAccuracy.unknown
    )

    LENGTH = 48

    _structure = struct.Struct("<BB10bIIIIIIIBB6x")

    def unpack(self, data):
        values = self._structure.unpack_from(data)
        self.gnss_manufacturer_id = GNSSManufacturerID(values[0])
        self.gnss_receiver_model = TrimbleGNSSReceiverModel(values[1])
        self.serial_number = bytes(values[2:12])
        self.firmware_version = values[12]
        (
            *self.software_license_code,
            self.omnistar_serial_number,
            self.omnistar_subscription_start_unix_time,
            self.omnistar_subscription_expiry_unix_time,
        ) = values[13:19]

        self.omnistar_engine_mode = OmnistarEngineMode(values[19])
        self.rtk_software_license_accuracy = RTKSoftwareLicenseAccuracy(values[20])


@dataclass()
class GNSSReceiverInformationPacket:
    """Packet 69 - GNSS Receiver Information Packet"""

    advanced_navigation_gnss_receiver_information: AdvancedNavigationGNSSReceiverInformation = field(
        default_factory=AdvancedNavigationGNSSReceiverInformation, repr=False
    )
    trimble_gnss_receiver_information: TrimbleGNSSReceiverInformation = field(
        default_factory=TrimbleGNSSReceiverInformation, repr=False
    )

    ID = PacketID.gnss_receiver_information

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to GNSS Receiver Information Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (
            len(an_packet.data) == AdvancedNavigationGNSSReceiverInformation.LENGTH
        ):
            self.advanced_navigation_gnss_receiver_information.unpack(an_packet.data)
            return 0
        elif (an_packet.id == self.ID) and (
            len(an_packet.data) == TrimbleGNSSReceiverInformation.LENGTH
        ):
            self.trimble_gnss_receiver_information.unpack(an_packet.data)
            return 0
        else:
            return 1
