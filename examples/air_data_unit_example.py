################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                          air_data_unit_example.py                          ##
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

""" This example shows how to send, receive and log ANPP packets with an Air Data Unit """

import datetime
import sys

import an_devices.air_data_unit_device as adu_device
from anpp_packets.an_packet_protocol import ANPacket
from anpp_packets.an_packets import PacketID


if __name__ == '__main__':
    # Checks enough arguments in command for serial communications. Otherwise, prompts user on use.
    if len(sys.argv) != 3:
        print(
            f"Usage: program com_port baud_rate\n"
            f"Windows Example: python air_data_unit_example.py COM1 115200\n"
            f"Linux Example: python air_data_unit_example.py /dev/ttyUSB0 115200"
        )
        exit()
    comport = str(sys.argv[1])
    baudrate = sys.argv[2]

    air_data_unit = adu_device.AirDataUnit(comport, baudrate)
    air_data_unit.start()

    # Checks serial port connection is open
    if air_data_unit.is_open:
        print(f"Connected to port:{air_data_unit.port} with baud:{air_data_unit.baud}")
        air_data_unit.flush()

        # Creates log file for received binary data from device
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logFile = open(f"AirDataUnitLog_{now}.anpp", 'xb')

        an_packet = ANPacket()

        air_data_unit.get_device_and_configuration_information()

        while air_data_unit.is_open:
            if air_data_unit.in_waiting():
                # Get bytes in serial buffer
                bytes_in_buffer = air_data_unit.in_waiting()
                data_bytes = air_data_unit.read(bytes_in_buffer)

                # Record in log file the raw binary of ANPP packets
                logFile.write(data_bytes)

                # Adds bytes to array for decoding
                air_data_unit.decoder.add_data(packet_bytes=data_bytes)

            # If bytes are in array then decode
            if len(air_data_unit.decoder.buffer) > 0:
                an_packet = air_data_unit.decoder.decode()

                # ===============================================================
                # This example is only printing a subset of a few packets contents.
                # Users can expand on this with any packet class imported in air_data_unit_device.py.
                # The Packet ID and length will be printed for any other packet.
                # ===============================================================
                if an_packet is not None:
                    if an_packet.id == PacketID.raw_sensors:
                        raw_sensor_packet = adu_device.RawSensorsPacket()
                        if raw_sensor_packet.decode(an_packet) == 0:
                            print(
                                f"Raw Sensors Packet:\n"
                                f"\tAbsolute Pressure: {raw_sensor_packet.absolute_pressure} Pa\n"
                                f"\tDifferential Pressure: {raw_sensor_packet.differential_pressure} Pa\n"
                                f"\tRaw Sensor Status: \n"
                                f"\t\tabsolute_pressure_valid: {raw_sensor_packet.raw_sensors_status.absolute_pressure_valid}\n"
                                f"\t\tdifferential_pressure_valid: {raw_sensor_packet.raw_sensors_status.differential_pressure_valid}\n"
                                f"\tTemperature: {raw_sensor_packet.temperature} degrees C"
                            )
                    elif an_packet.id == PacketID.external_air_data:
                        air_data_packet = adu_device.AirDataPacket()
                        if air_data_packet.decode(an_packet) == 0:
                            print(
                                f"Air Data Packet:\n"
                                f"\tBarometric Altitude: {air_data_packet.barometric_altitude} m\n"
                                f"\tBarometric Altitude Standard Deviation: {air_data_packet.barometric_altitude_standard_deviation} m\n"
                                f"\tAirspeed: {air_data_packet.airspeed} m/s\n"
                                f"\tAirspeed Standard Deviation: {air_data_packet.airspeed_standard_deviation} m/s"
                            )
                    elif an_packet.id != 0:
                        print(f"Received {an_packet.id} of length:{an_packet.length}")
    else:
        print(f"No connection.")

    air_data_unit.close()
