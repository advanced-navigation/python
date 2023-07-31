################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                              certus_tcp_example.py                         ##
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

""" This example shows how to send, receive and log ANPP packets with a Certus"""

import datetime
import sys
import math

import an_devices.certus_device as certus_device
from anpp_packets.an_packet_protocol import ANPacket
from anpp_packets.an_packets import PacketID


if __name__ == "__main__":
    # Checks enough arguments in command for serial communications. Otherwise prompts user on use.
    if len(sys.argv) != 3:
        print(
            f"Usage: program com_port baud_rate\n"
            f"Windows Example: python certus_example.py COM1 115200\n"
            f"Linux Example: python certus_example.py /dev/ttyUSB0 115200"
        )
        exit()
    Address = str(sys.argv[1])
    port = int(sys.argv[2])

    certus = certus_device.Certus_tcp(Address, port)
    certus.start()

    # Checks serial port connection is open
    if certus.is_open:
        print(f"Connected to adress:{certus.address} port:{certus.port}")

        # Creates log file for received binary data from device
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logFile = open(f"CertusLog_{now}.anpp", "xb")

        an_packet = ANPacket()

        certus.get_device_and_configuration_information()

        while certus.is_open:
            # Get bytes via tcp
            data_bytes = certus.read()

            if data_bytes is not None:
                # Record in log file the raw binary of ANPP packets
                logFile.write(data_bytes)

                # Adds bytes to array for decoding
                certus.decoder.add_data(packet_bytes=data_bytes)

                # If bytes are in array then decode
                if len(certus.decoder.buffer) > 0:
                    an_packet = certus.decoder.decode()

                    # ===============================================================
                    # This example is only printing a subset of a few packets contents.
                    # Users can expand on this with any packet class imported in certus_device.py.
                    # The Packet ID and length will be printed for any other packet.
                    # ===============================================================
                    if an_packet is not None:
                        if an_packet.id == PacketID.system_state:
                            system_state_packet = certus_device.SystemStatePacket()
                            if system_state_packet.decode(an_packet) == 0:
                                print(
                                    f"System State Packet:\n"
                                    f"\tLatitude:{math.degrees(system_state_packet.latitude)}, "
                                    f"Longitude:{math.degrees(system_state_packet.longitude)}, "
                                    f"Height:{math.degrees(system_state_packet.height)}"
                                )
                                print(
                                    f"\tRoll:{math.degrees(system_state_packet.orientation[0])}, "
                                    f"Pitch:{math.degrees(system_state_packet.orientation[1])}, "
                                    f"Heading:{math.degrees(system_state_packet.orientation[2])}"
                                )
                        elif an_packet.id == PacketID.raw_sensors:
                            raw_sensor_packet = certus_device.RawSensorsPacket()
                            if raw_sensor_packet.decode(an_packet) == 0:
                                print(
                                    f"Raw Sensors Packet:\n"
                                    f"\tAccelerometers X:{raw_sensor_packet.accelerometers[0]}, "
                                    f"Y:{raw_sensor_packet.accelerometers[1]}, "
                                    f"Z:{raw_sensor_packet.accelerometers[2]}"
                                )
                                print(
                                    f"\tGyroscopes X:{math.degrees(raw_sensor_packet.gyroscopes[0])}, "
                                    f"Y:{math.degrees(raw_sensor_packet.gyroscopes[1])}, "
                                    f"Z:{math.degrees(raw_sensor_packet.gyroscopes[2])}"
                                )
                        elif an_packet.id == PacketID.external_air_data:
                            external_air_data_packet = (
                                certus_device.ExternalAirDataPacket()
                            )
                            if external_air_data_packet.decode(an_packet) == 0:
                                print(
                                    f"External Air Data Packet:\n"
                                    f"\tBarometric Altitude Set and Ready:{external_air_data_packet.flags.barometric_altitude_set_and_valid}\n "
                                    f"\tBarometric Altitude: {external_air_data_packet.barometric_altitude}m\n"
                                    f"\tAirspeed Set and Ready:{external_air_data_packet.flags.airspeed_set_and_valid}\n"
                                    f"\tAirspeed: {external_air_data_packet.airspeed}m/s"
                                )
                        elif an_packet.id == PacketID.external_odometer:
                            external_odometer_packet = (
                                certus_device.ExternalOdometerPacket()
                            )
                            if external_odometer_packet.decode(an_packet) == 0:
                                print(
                                    f"External Odometer Packet:\n"
                                    f"\tSpeed:{external_odometer_packet.speed}m/s\n"
                                    f"\tDistance Travelled:{external_odometer_packet.distance_travelled}m\n"
                                    f"\tReverse Detection Supported:{external_odometer_packet.flags.reverse_detection_supported}"
                                )
                        elif an_packet.id != 0:
                            print(
                                f"Received {an_packet.id} of length:{an_packet.length}"
                            )
    else:
        print(f"No connection.")

    certus.close()
