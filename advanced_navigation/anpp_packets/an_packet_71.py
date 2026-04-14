################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                               an_packet_71.py                              ##
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
import struct
from .an_packets import PacketID
from .an_packet_protocol import ANPacket


@dataclass()
class NorthSeekingInitialisationStatusFlags:
    """North Seeking Initialisation Status Flags"""

    north_seeking_initialised: bool = False
    position_not_ready: bool = False
    excessive_roll: bool = False
    excessive_pitch: bool = False
    excessive_movement: bool = False
    latitude_change: bool = False
    lever_arm_offset_change: bool = False
    latitude_check_failed: bool = False

    def unpack(self, data):
        """Unpack data bytes"""
        self.north_seeking_initialised = (data & (1 << 0)) != 0
        self.position_not_ready = (data & (1 << 1)) != 0
        self.excessive_roll = (data & (1 << 2)) != 0
        self.excessive_pitch = (data & (1 << 3)) != 0
        self.excessive_movement = (data & (1 << 4)) != 0
        self.latitude_change = (data & (1 << 5)) != 0
        self.lever_arm_offset_change = (data & (1 << 6)) != 0
        self.latitude_check_failed = (data & (1 << 7)) != 0

    def pack(self):
        return (
            (self.north_seeking_initialised << 0)
            & (self.position_not_ready << 1)
            & (self.excessive_roll << 2)
            & (self.excessive_pitch << 3)
            & (self.excessive_movement << 4)
            & (self.latitude_change << 5)
            & (self.lever_arm_offset_change << 6)
            & (self.latitude_check_failed << 7)
        )


@dataclass()
class NorthSeekingInitialisationStatusPacket:
    """Packet 71 - North Seeking Initialisation Status Packet"""

    flags: NorthSeekingInitialisationStatusFlags = field(
        default_factory=NorthSeekingInitialisationStatusFlags, repr=False
    )
    version: int = 0
    progress: int = 0
    alignment_attempts: int = 0
    coarse_alignment_heading: float = 0
    predicted_accuracy: float = 0

    ID = PacketID.north_seeking_initialisation_status
    LENGTH = 28

    _structure = struct.Struct("<HHBBxxff12x")

    def decode(self, an_packet: ANPacket) -> int:
        """Decode ANPacket to North Seeking Initialisation Status Packet
        Returns 0 on success and 1 on failure"""
        if (an_packet.id == self.ID) and (len(an_packet.data) == self.LENGTH):
            (
                flags_value,
                self.version,
                self.progress,
                self.alignment_attempts,
                self.coarse_alignment_heading,
                self.predicted_accuracy,
            ) = self._structure.unpack_from(an_packet.data)
            self.flags.unpack(flags_value)
            return 0
        else:
            return 1

    def encode(self) -> ANPacket:
        """Encode North Seeking Initialisation Status Packet to ANPacket
        Returns the ANPacket"""
        data = self._structure.pack(
            self.flags.pack(),
            self.version,
            self.progress,
            self.alignment_attempts,
            self.coarse_alignment_heading,
            self.predicted_accuracy,
        )

        an_packet = ANPacket()
        an_packet.encode(self.ID, self.LENGTH, data)

        return an_packet
