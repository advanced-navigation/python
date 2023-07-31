################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                           air_data_unit_device.py                          ##
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

from .advanced_navigation_device_serial import (
    AdvancedNavigationDeviceSerial as _AdvancedNavigationDevice,
)
from anpp_packets.an_packets import PacketID as _PacketID

from anpp_packets.an_packet_0 import AcknowledgePacket, AcknowledgeResult
from anpp_packets.an_packet_1 import RequestPacket
from anpp_packets.an_packet_2 import BootModePacket, BootMode
from anpp_packets.an_packet_3 import DeviceInformationPacket
from anpp_packets.an_packet_4 import RestoreFactorySettingsPacket
from anpp_packets.an_packet_5 import ResetPacket, ResetVerification
from anpp_packets.an_packet_7 import (
    FileTransferFirstPacket,
    DataEncoding,
    FileTransferMetadata,
)
from anpp_packets.an_packet_8 import FileTransferAcknowledgePacket, FileTransferResponse
from anpp_packets.an_packet_9 import FileTransferOngoingPacket
from anpp_packets.an_packet_28 import RawSensorsPacketAdu as RawSensorsPacket
from anpp_packets.an_packet_68 import AirDataPacket


class AirDataUnit(_AdvancedNavigationDevice):
    """Air Data Unit object with high level functions for setting and receiving values"""

    valid_baud_rates = [115200]

    def return_device_information_and_configuration_packets(self):
        """Returns Air Data Unit's Device Information and Configuration packets as
        all Advanced Navigation devices have different packets available"""
        return [_PacketID.device_information]
