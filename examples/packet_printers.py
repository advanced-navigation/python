################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              packet_printers.py                            ##
##                     Copyright 2026, Advanced Navigation                    ##
##                                                                            ##
################################################################################
#                                                                              #
# Copyright (C) 2026 Advanced Navigation                                       #
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

import json
from dataclasses import asdict
from advanced_navigation.anpp_packets.an_packet_protocol import ANPacket
from advanced_navigation.anpp_packets.an_packets import PacketID
from advanced_navigation.anpp_packets.an_packet_3 import DeviceID
from advanced_navigation.anpp_packets.an_packet_23 import StatusPacket, StatusPacketAdu2
from advanced_navigation.anpp_packets.an_packet_28 import RawSensorsPacket, RawSensorsPacketAdu
from advanced_navigation.anpp_packets import __all__ as anpp_all
import importlib
import inspect


def get_device_specific_packet_obj(an_packet_id: int, device_id: DeviceID):
    """
    Returns the appropriate un-decoded packet object based on the packet ID and the connected device ID.
    This handles devices that overload the same packet ID with different packet structures.
    For instance, packet ID 23 (Status) or 28 (RawSensors) has a different layout for the Air Data Unit.
    """
    packet_id_enum = PacketID(an_packet_id)

    # Handle packet overrides based on specific devices
    if packet_id_enum == PacketID.status:
        if device_id == DeviceID.air_data_unit_v2:
            return StatusPacketAdu2()
        else:
            return StatusPacket()

    if packet_id_enum == PacketID.raw_sensors:
        if device_id == DeviceID.air_data_unit:
            return RawSensorsPacketAdu()
        else:
            return RawSensorsPacket()

    # For all other packets, use the generic mapping
    return get_obj_from_enum(packet_id_enum)

def print_packet(packet):
    """
    Prints the decoded packet.
    """
    try:
        name = packet.__class__.__name__
        # default=str handles Enums, bytes, and other non-serializable objects
        print(f"[{name}] {json.dumps(asdict(packet), default=str)}")
    except Exception:
        print(f"Received Packet ID {packet.ID.value} (Length: {packet.LENGTH})")

def handle_raw_an_packet(an_packet: ANPacket, device_id: DeviceID):
    """
    Takes a raw ANPacket, looks up the correct packet object definition for the current device,
    decodes it, and prints it in a human-readable format.
    """
    try:
        pkt_obj = get_device_specific_packet_obj(an_packet.id, device_id)

        if pkt_obj is None:
            return # No class mapping available for this packet ID

        # decode() returns 0 on success, non-zero on failure (e.g. invalid length/CRC)
        if pkt_obj.decode(an_packet) == 0:
            print_packet(pkt_obj)
        else:
            print(f"Failed to decode Packet ID {an_packet.id} of length {an_packet.length}")
    except ValueError:
        pass # Unknown enum value or unhandled packet


_packet_classes_cache = None

def get_obj_from_enum(packet_enum):
    # This function dynamically discovers and caches packet classes by inspecting SDK modules.
    # It avoids having to manually maintain a giant dictionary mapping Packet IDs to Classes.
    global _packet_classes_cache
    if _packet_classes_cache is None:
        _packet_classes_cache = {}
        # Iterate over all exported module names in advanced_navigation.anpp_packets
        for module_name in anpp_all:
            if not module_name.startswith('an_packet_'):
                continue
            module = importlib.import_module(f'advanced_navigation.anpp_packets.{module_name}')
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, 'ID') and obj.__module__ == module.__name__:
                    # Skip specific overloaded classes because their packet IDs conflict with generic ones.
                    # They are handled explicitly in `get_device_specific_packet_obj` or manually below.
                    if name in ['StatusPacketAdu2', 'RawSensorsPacketAdu', 'FileTransferFirstPacket', 'AcknowledgePacket']:
                        continue
                    _packet_classes_cache[obj.ID.value] = obj

        import advanced_navigation.anpp_packets.an_packet_0 as an_packet_0
        import advanced_navigation.anpp_packets.an_packet_7 as an_packet_7
        _packet_classes_cache[0] = an_packet_0.AcknowledgePacket
        _packet_classes_cache[7] = an_packet_7.FileTransferFirstPacket

    packet_class = _packet_classes_cache.get(packet_enum.value)
    if packet_class:
        return packet_class()
    return None
