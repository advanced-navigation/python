################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                           air_data_unit_device.py                          ##
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

from anpp_packets.devices.air_data_unit_packets import AirDataUnitPackets
from advanced_navigation_device import AdvancedNavigationDevice

""" Air Data Unit object with high level functions for setting and receiving values """
class AirDataUnit(AdvancedNavigationDevice, AirDataUnitPackets):
    ''' Returns Air Data Unit's Device Information and Configuration packets as
        all Advanced Navigation devices have different packets available '''
    def return_device_information_and_configuration_packets(self):
        return [self.PacketID.device_information.value
                ]