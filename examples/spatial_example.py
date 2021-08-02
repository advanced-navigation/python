################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                             spatial_example.py                             ##
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

""" This example shows how to send, receive and log ANPP packets with a Spatial"""

import datetime
import sys
import math

from spatial_device import Spatial
from anpp_packets.an_packet_protocol import AN_Packet, an_packet_decode

TRUE = 1
FALSE = 0

if __name__ == '__main__':
    # Checks enough arguments in command for serial communications. Otherwise prompts user on use.
    if (len(sys.argv) != 3):
        print(f"Usage - program com_port baud_rate\nExample - packet_example.exe COM1 115200")
        exit()        
    comport = str(sys.argv[1])
    baudrate = sys.argv[2]

    spatial = Spatial(comport, baudrate, log = True)
    spatial.start_serial()

    # Checks serial port connection is open
    if spatial.is_open:
        print(f"Connected to port:{spatial.port} with baud:{spatial.baud}")
        spatial.flush()

        # Creates log file for received binary data from device
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logFile = open(f"SpatialLog_{now}.anpp", 'xb')

        an_packet = AN_Packet()

        # Sets sensor ranges
        spatial.set_sensor_ranges(TRUE,
                                  spatial.AccelerometerRange.accelerometer_range_4g.value,
                                  spatial.GyroscopeRange.gyroscope_range_500dps.value,
                                  spatial.MagnetometerRange.magnetometer_range_8g.value)

        spatial.get_device_and_configuration_information()

        while(spatial.is_open):
            if (spatial.in_waiting() > 0):
                # Get bytes in serial buffer
                bytes_in_buffer = spatial.in_waiting()
                data_bytes = spatial.read(bytes_in_buffer)

                # Record in log file the raw binary of ANPP packets
                logFile.write(data_bytes)

                # Adds bytes to array for decoding
                spatial.bytes_waiting.add_data(packet_bytes = data_bytes)

            # If bytes are in array then decode
            if (len(spatial.bytes_waiting.buffer) > 0):
                an_packet, spatial.bytes_waiting = an_packet_decode(spatial.bytes_waiting)
 
                #===============================================================
                # This example is only looking for two ANPP packets and printing a subset 
                # of their contents. Users can expand on this with any packet in spatial_packets.py.
                # Any other packets received from the Advanced Navigation product will have their
                # Packet ID and Length printed in this example.
                #===============================================================
                if (an_packet is not None):
                    if(an_packet.id == spatial.PacketID.system_state.value):
                        system_state_packet = spatial.SystemStatePacket()
                        if (system_state_packet.decode(an_packet) == 0):
                            print(f"System State Packet:\n"
                                f"\tLatitude:{math.degrees(system_state_packet.latitude)}, "
                                f"Longitude:{math.degrees(system_state_packet.longitude)}, "
                                f"Height:{math.degrees(system_state_packet.height)}")
                            print(f"\tRoll:{math.degrees(system_state_packet.orientation[0])}, "
                                f"Pitch:{math.degrees(system_state_packet.orientation[1])}, "
                                f"Heading:{math.degrees(system_state_packet.orientation[2])}")
                    elif(an_packet.id == spatial.PacketID.raw_sensors.value):
                        raw_sensor_packet = spatial.RawSensorsPacket()
                        if(raw_sensor_packet.decode(an_packet) == 0):
                            print(f"Raw Sensors Packet:\n"
                                f"\tAccelerometers X:{raw_sensor_packet.accelerometers[0]}, "
                                f"Y:{raw_sensor_packet.accelerometers[1]}, "
                                f"Z:{raw_sensor_packet.accelerometers[2]}")
                            print(f"\tGyroscopes X:{math.degrees(raw_sensor_packet.gyroscopes[0])}, "
                                f"Y:{math.degrees(raw_sensor_packet.gyroscopes[1])}, "
                                f"Z:{math.degrees(raw_sensor_packet.gyroscopes[2])}")
                    elif(an_packet.id == spatial.PacketID.external_air_data.value):
                        external_air_data_packet = spatial.ExternalAirDataPacket()
                        if(external_air_data_packet.decode(an_packet) == 0):
                            print(f"External Air Data Packet:\n"
                                  f"\tBarometric Altitude Set and Ready:{external_air_data_packet.flags.barometric_altitude_set_and_valid}\n "
                                  f"\tBarometric Altitude: {external_air_data_packet.barometric_altitude}m\n"
                                  f"\tAirspeed Set and Ready:{external_air_data_packet.flags.airspeed_set_and_valid}\n"
                                  f"\tAirspeed: {external_air_data_packet.airspeed}m/s")
                    elif(an_packet.id == spatial.PacketID.external_odometer.value):
                        external_odometer_packet = spatial.ExternalOdometerPacket()
                        if(external_odometer_packet.decode(an_packet) == 0):
                            print(f"External Odometer Packet:\n"
                                  f"\tSpeed:{external_odometer_packet.speed}m/s\n"
                                  f"\tDistance Travelled:{external_odometer_packet.distance_travelled}m\n"
                                  f"\tReverse Detection Supported:{external_odometer_packet.flags.reverse_detection_supported}")
                    else:
                        print(f"Packet ID:{an_packet.id} of Length:{an_packet.length}")
    else:
        print(f"No connection.")

    spatial.close()