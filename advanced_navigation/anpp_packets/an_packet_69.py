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

import struct
from dataclasses import dataclass, field
from enum import Enum

from .an_packet_protocol import ANPacket
from .an_packets import PacketID


class GNSSManufacturerID(Enum):
    """GNSS Manufacturer ID"""

    unknown = 0
    trimble = 1
    ublox = 2
    advanced_navigation = 3
    skytraq = 5
    septentrio = 6


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


class UbloxGNSSReceiverModel(Enum):
    """u-blox GNSS Receiver Model"""

    unknown = 0
    zed_m8 = 1
    zed_m8t = 2
    zed_m8p = 3
    zed_f9p = 4
    neo_f9p = 5
    zed_x20p = 6


class AdvancedNavigationGNSSReceiverModel(Enum):
    """Advanced Navigation GNSS Receiver Model"""

    unknown = 0
    aries_f9p = 1
    aries_gc2 = 2
    aries_x90 = 3
    aries_ngs = 4
    aries_x20p = 5


class SkyTraqGNSSReceiverModel(Enum):
    """SkyTraq GNSS Receiver Model"""

    unknown = 0
    px1172rh = 1
    orion_b16 = 2


class SeptentrioGNSSReceiverModel(Enum):
    """Septentrio GNSS Receiver Model"""

    unknown = 0
    mosaic_x5 = 1


GNSSReceiverModel = (
    TrimbleGNSSReceiverModel
    | UbloxGNSSReceiverModel
    | AdvancedNavigationGNSSReceiverModel
    | SkyTraqGNSSReceiverModel
    | SeptentrioGNSSReceiverModel
    | int
)


GNSS_RECEIVER_MODEL_MAP: dict[GNSSManufacturerID, type[Enum]] = {
    GNSSManufacturerID.trimble: TrimbleGNSSReceiverModel,
    GNSSManufacturerID.ublox: UbloxGNSSReceiverModel,
    GNSSManufacturerID.advanced_navigation: AdvancedNavigationGNSSReceiverModel,
    GNSSManufacturerID.skytraq: SkyTraqGNSSReceiverModel,
    GNSSManufacturerID.septentrio: SeptentrioGNSSReceiverModel,
}


class LBandEngineMode(Enum):
    """L-Band Engine Mode"""

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
class GNSSReceiverInformationV1:
    """GNSS Receiver Information V1 (Trimble)"""

    gnss_manufacturer: GNSSManufacturerID = GNSSManufacturerID.unknown
    gnss_receiver_model: GNSSReceiverModel = 0
    serial_number: bytes = field(default_factory=lambda: bytes([0] * 10), repr=False)
    firmware_version: float = 0.0
    software_license: list[int] = field(default_factory=lambda: [0, 0, 0], repr=False)
    lband_serial_number: int = 0
    lband_subscription_start: int = 0
    lband_subscription_expiry: int = 0
    lband_engine_mode: LBandEngineMode = LBandEngineMode.inactive
    rtk_accuracy: RTKSoftwareLicenseAccuracy = RTKSoftwareLicenseAccuracy.unknown

    LENGTH = 48
    _structure = struct.Struct("<BB10sIIIIIIIBB6x")

    def unpack(self, data):
        values = self._structure.unpack_from(data)
        self.gnss_manufacturer = GNSSManufacturerID(values[0])

        model_class = GNSS_RECEIVER_MODEL_MAP.get(self.gnss_manufacturer)
        if model_class:
            try:
                self.gnss_receiver_model = model_class(values[1])
            except ValueError:
                self.gnss_receiver_model = values[1]
        else:
            self.gnss_receiver_model = values[1]

        self.serial_number = values[2]
        self.firmware_version = values[3] / 1000.0
        self.software_license = list(values[4:7])
        self.lband_serial_number = values[7]
        self.lband_subscription_start = values[8]
        self.lband_subscription_expiry = values[9]
        self.lband_engine_mode = LBandEngineMode(values[10])
        self.rtk_accuracy = RTKSoftwareLicenseAccuracy(values[11])

    def encode(self) -> bytes:
        return self._structure.pack(
            self.gnss_manufacturer.value,
            self.gnss_receiver_model.value
            if isinstance(self.gnss_receiver_model, Enum)
            else self.gnss_receiver_model,
            self.serial_number,
            int(self.firmware_version * 1000),
            *self.software_license,
            self.lband_serial_number,
            self.lband_subscription_start,
            self.lband_subscription_expiry,
            self.lband_engine_mode.value,
            self.rtk_accuracy.value,
        )


@dataclass()
class GNSSReceiverInformationV2:
    """GNSS Receiver Information V2"""

    gnss_manufacturer: GNSSManufacturerID = GNSSManufacturerID.unknown
    gnss_receiver_model: GNSSReceiverModel = 0
    gnss_serial_number: bytes = field(
        default_factory=lambda: bytes([0] * 24), repr=False
    )
    gnss_firmware_version: float = 0.0
    gnss_hardware_version: float = 0.0
    software_license: list[int] = field(default_factory=lambda: [0, 0, 0], repr=False)
    lband_serial_number: int = 0
    lband_subscription_start: int = 0
    lband_subscription_expiry: int = 0
    lband_engine_mode: LBandEngineMode = LBandEngineMode.inactive
    rtk_accuracy: RTKSoftwareLicenseAccuracy = RTKSoftwareLicenseAccuracy.unknown
    receiver_index: int = 0

    LENGTH = 68
    _structure = struct.Struct("<BB24sIIIIIIIIBBB7x")

    def unpack(self, data):
        values = self._structure.unpack_from(data)
        self.gnss_manufacturer = GNSSManufacturerID(values[0])

        model_class = GNSS_RECEIVER_MODEL_MAP.get(self.gnss_manufacturer)
        if model_class:
            try:
                self.gnss_receiver_model = model_class(values[1])
            except ValueError:
                self.gnss_receiver_model = values[1]
        else:
            self.gnss_receiver_model = values[1]

        self.gnss_serial_number = values[2]
        self.gnss_firmware_version = values[3] / 1000.0
        self.gnss_hardware_version = values[4] / 1000.0
        self.software_license = list(values[5:8])
        self.lband_serial_number = values[8]
        self.lband_subscription_start = values[9]
        self.lband_subscription_expiry = values[10]
        self.lband_engine_mode = LBandEngineMode(values[11])
        self.rtk_accuracy = RTKSoftwareLicenseAccuracy(values[12])
        self.receiver_index = values[13]

    def encode(self) -> bytes:
        return self._structure.pack(
            self.gnss_manufacturer.value,
            self.gnss_receiver_model.value
            if isinstance(self.gnss_receiver_model, Enum)
            else self.gnss_receiver_model,
            self.gnss_serial_number,
            int(self.gnss_firmware_version * 1000),
            int(self.gnss_hardware_version * 1000),
            *self.software_license,
            self.lband_serial_number,
            self.lband_subscription_start,
            self.lband_subscription_expiry,
            self.lband_engine_mode.value,
            self.rtk_accuracy.value,
            self.receiver_index,
        )


@dataclass()
class GNSSReceiverInformationPacket:
    """Packet 69 - GNSS Receiver Information Packet"""

    information: GNSSReceiverInformationV1 | GNSSReceiverInformationV2 = field(
        default_factory=GNSSReceiverInformationV2
    )

    ID = PacketID.gnss_receiver_information

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to GNSS Receiver Information Packet
        Returns 0 on success and 1 on failure"""
        if an_packet.id == self.ID:
            if len(an_packet.data) == GNSSReceiverInformationV1.LENGTH:
                self.information = GNSSReceiverInformationV1()
                self.information.unpack(an_packet.data)
                return 0
            elif len(an_packet.data) == GNSSReceiverInformationV2.LENGTH:
                self.information = GNSSReceiverInformationV2()
                self.information.unpack(an_packet.data)
                return 0
        return 1

    def encode(self) -> ANPacket:
        """Encode GNSS Receiver Information Packet to ANPacket"""
        data = b""
        if self.information:
            data = self.information.encode()

        an_packet = ANPacket()
        an_packet.encode(self.ID, len(data), data)
        return an_packet
