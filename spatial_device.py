################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                             spatial_device.py                              ##
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

from anpp_packets.spatial_packets import SpatialPackets
from advanced_navigation_device import AdvancedNavigationDevice

""" Spatial object with high level functions for setting and receiving values """
class Spatial(AdvancedNavigationDevice, SpatialPackets):
    ''' Returns Spatial's Device Information and Configuration packets as 
        all Advanced Navigation devices have different packets available '''
    def return_device_information_and_configuration_packets(self):
        return [self.PacketID.device_information.value,
                self.PacketID.packet_timer_period.value,
                self.PacketID.packets_period.value,
                self.PacketID.baud_rates.value,
                self.PacketID.sensor_ranges.value,
                self.PacketID.installation_alignment.value,
                self.PacketID.filter_options.value,
                self.PacketID.gpio_configuration.value,
                self.PacketID.magnetic_calibration_values.value,
                self.PacketID.magnetic_calibration_status.value,
                self.PacketID.odometer_configuration.value,
                self.PacketID.reference_point_offsets.value,
                self.PacketID.gpio_output_configuration.value,
                self.PacketID.user_data.value,
                self.PacketID.gpio_input_configuration.value
                ]