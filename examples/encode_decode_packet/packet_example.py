################################################################################
##                                                                            ##
##                 Advanced Navigation Packet Protocol Library                ##
##                  Python Language Spatial SDK, Version 0.02                 ##
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


""" This example shows how to send, receive and log Spatial ANPP packets """

import os
import datetime
import sys
import math

from spatial_packets import SensorRangesPacket, AccelerometerRange, GyroscopeRange, MagnetometerRange, SystemStatePacket, RawSensorsPacket, PacketID
from an_packet_protocol import AN_Decoder, AN_Packet, an_packet_decode
import serial
import serial.serialutil as serialutil

TRUE = 1
FALSE = 0

# Example function encoding an ANPP packet to be sent.
def set_sensor_ranges():
    sensor_ranges_packet = SensorRangesPacket()

    sensor_ranges_packet.permanent = TRUE
    sensor_ranges_packet.accelerometers_range = AccelerometerRange.accelerometer_range_4g.value
    sensor_ranges_packet.gyroscopes_range = GyroscopeRange.gyroscope_range_500dps.value
    sensor_ranges_packet.magnetometers_range = MagnetometerRange.magnetometer_range_8g.value

    return(sensor_ranges_packet.encode().bytes())

if __name__ == '__main__':
    # Checks enough arguments in command for serial communications. Otherwise prompts user on use.
    if (len(sys.argv) != 3):
        print(f"Usage - program com_port baud_rate\nExample - packet_example.exe COM1 115200")
        exit()        
    comport = str(sys.argv[1])
    baudrate = sys.argv[2]

    # Checks if operating system is Windows or Linux
    if ((os.name == 'nt') or (os.name == 'posix')):
        # Connects to serial port
        ser = serial.Serial(port=comport,
                         baudrate=baudrate,
                         bytesize=serialutil.EIGHTBITS,
                         parity=serialutil.PARITY_NONE,
                         stopbits=serialutil.STOPBITS_ONE,
                         timeout=None,
                         xonxoff=False,
                         rtscts=False,
                         write_timeout=None,
                         dsrdtr=False,
                         inter_byte_timeout=None
                         )
    else:
        print(f"Packet_example currently only supports Windows and Linux operating systems.")
        exit()

    # Checks serial port connection is open
    if ser.is_open:
        print(f"Connected to port:{comport} with baud:{baudrate}")
        ser.flush()

        # Creates log file for received binary data from device
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = ('SpatialLog_%s.anpp' %now)
        logFile = open(filename, 'xb')

        decoder_array = AN_Decoder()
        byteIndex = 0
        an_packet = AN_Packet()

        system_state_packet = SystemStatePacket()
        raw_sensor_packet = RawSensorsPacket()

        # Sets sensor ranges as an example of sending an ANPP packet
        ser.write(set_sensor_ranges())

        while(1):
            if (ser.in_waiting > 0):
                # Get bytes in serial buffer
                bytes_in_buffer = ser.in_waiting
                data_bytes = ser.read(bytes_in_buffer)

                # Record in log file the raw binary of ANPP packets
                logFile.write(data_bytes)

                # Adds bytes to array for decoding
                decoder_array.add_data(packet_bytes = data_bytes)

            # If bytes are in array then decode
            if (len(decoder_array.buffer) > 0):
                an_packet, decoder_array = an_packet_decode(decoder_array)
 
                #===============================================================
                # This example is only looking for two ANPP packets and printing a subset 
                # of their contents. Users can expand on this with any packet in spatial_packets.py.
                # Any other packets received from the Advanced Navigation product will have their
                # Packet ID and Length printed in this example.
                #===============================================================
                if (an_packet is not None):
                    if(an_packet.id == PacketID.system_state.value):
                        if (system_state_packet.decode(an_packet) == 0):
                            print(f"System State Packet:\n"
                                f"\tLatitude:{math.degrees(system_state_packet.latitude)}, "
                                f"Longitude:{math.degrees(system_state_packet.longitude)}, "
                                f"Height:{math.degrees(system_state_packet.height)}")
                            print(f"\tRoll:{math.degrees(system_state_packet.orientation[0])}, "
                                f"Pitch:{math.degrees(system_state_packet.orientation[1])}, "
                                f"Heading:{math.degrees(system_state_packet.orientation[2])}")
                    elif(an_packet.id == PacketID.raw_sensors.value):
                        if(raw_sensor_packet.decode(an_packet) == 0):
                            print(f"Raw Sensors Packet: \n"
                                f"\tAccelerometers X:{raw_sensor_packet.accelerometers[0]}, "
                                f"Y:{raw_sensor_packet.accelerometers[1]}, "
                                f"Z:{raw_sensor_packet.accelerometers[2]}")
                            print(f"\tGyroscopes X:{math.degrees(raw_sensor_packet.gyroscopes[0])}, "
                                f"Y:{math.degrees(raw_sensor_packet.gyroscopes[1])}, "
                                f"Z:{math.degrees(raw_sensor_packet.gyroscopes[2])}")
                    else:
                        print(f"Packet ID:{an_packet.id} of Length:{an_packet.length}")

    else:
        print(f"No connection. :( ")

    ser.close()