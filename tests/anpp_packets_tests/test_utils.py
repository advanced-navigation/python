################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              test_utils.py                                 ##
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

import importlib
import inspect
from advanced_navigation.anpp_packets import __all__ as anpp_all

_packet_classes_cache = None

def get_obj_from_enum(packet_enum):
    global _packet_classes_cache
    if _packet_classes_cache is None:
        _packet_classes_cache = {}
        for module_name in anpp_all:
            if not module_name.startswith('an_packet_'):
                continue
            module = importlib.import_module(f'advanced_navigation.anpp_packets.{module_name}')
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, 'ID') and obj.__module__ == module.__name__:
                    if name in ['StatusPacketAdu2', 'RawSensorsPacketAdu', 'FileTransferFirstPacket', 'AcknowledgePacket']:
                        continue
                    _packet_classes_cache[obj.ID.value] = obj
                    
        import advanced_navigation.anpp_packets.an_packet_0 as an_packet_0
        import advanced_navigation.anpp_packets.an_packet_7 as an_packet_7
        _packet_classes_cache[0] = an_packet_0.AcknowledgePacket
        _packet_classes_cache[7] = an_packet_7.FileTransferFirstPacket
        
    packet_class = _packet_classes_cache.get(packet_enum.value if hasattr(packet_enum, "value") else packet_enum)
    if packet_class:
        return packet_class()
    return None
