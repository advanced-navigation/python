################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                         ntrip_client_example.py                            ##
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

"""
This example shows how to connect to an NTRIP server and send RTCM
correction data to an Advanced Navigation device. It will also periodically
send NMEA GPGGA sentences back to the NTRIP server.
"""

import argparse
import asyncio
import base64
import datetime
import logging
import math

from advanced_navigation.an_devices.an_device_async import AnDevice
from advanced_navigation.anpp_packets.an_packet_20 import SystemStatePacket
from advanced_navigation.anpp_packets.an_packet_55 import RTCMCorrectionsPacket


class NtripState:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.height = 0.0
        self.has_position = False
        self.bytes_received = 0


def generate_gpgga(latitude, longitude, altitude):
    """
    Generate an NMEA GPGGA string from latitude (radians), longitude (radians), and altitude (meters).
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    time_str = now.strftime("%H%M%S.%f")[:10]

    lat_deg = math.degrees(latitude)
    lat_char = "S" if lat_deg < 0 else "N"
    lat_abs = abs(lat_deg)
    lat_mins = (lat_abs - int(lat_abs)) * 60
    lat_str = f"{int(lat_abs):02d}{lat_mins:010.7f}"

    lon_deg = math.degrees(longitude)
    lon_char = "W" if lon_deg < 0 else "E"
    lon_abs = abs(lon_deg)
    lon_mins = (lon_abs - int(lon_abs)) * 60
    lon_str = f"{int(lon_abs):03d}{lon_mins:010.7f}"

    quality = 1
    num_sats = 10
    hdop = 2.0

    gpgga_data = f"GPGGA,{time_str},{lat_str},{lat_char},{lon_str},{lon_char},{quality},{num_sats},{hdop},{altitude:.2f},M,{altitude:.2f},M,,"

    checksum = 0
    for char in gpgga_data:
        checksum ^= ord(char)

    return f"${gpgga_data}*{checksum:02X}\r\n"


async def ntrip_client(args, device: AnDevice, state: NtripState):
    """
    Connect to NTRIP server, authenticate, send NMEA position and receive RTCM corrections.
    """
    if not args.ntrip_skip_forwarding_position:
        print("Waiting for initial device position...")
        while not state.has_position:
            await asyncio.sleep(0.5)

    auth = base64.b64encode(f"{args.ntrip_user}:{args.ntrip_pass}".encode()).decode()

    print(f"Connecting to NTRIP caster at {args.ntrip_server}:{args.ntrip_port}...")
    try:
        reader, writer = await asyncio.open_connection(
            args.ntrip_server, args.ntrip_port
        )
    except OSError as e:
        print(f"Failed to connect to NTRIP caster: {e}")
        return

    # Generate initial NMEA GGA
    ntrip_gga_header = ""
    if not args.ntrip_skip_forwarding_position:
        initial_gga = generate_gpgga(state.latitude, state.longitude, state.height)
        print(f"Initial NMEA GGA: {initial_gga.strip()}")
        ntrip_gga_header = f"Ntrip-GGA: {initial_gga.strip()}\r\n"

    # Build NTRIP 2.0 request
    request = (
        f"GET /{args.ntrip_mountpoint} HTTP/1.1\r\n"
        f"Host: {args.ntrip_server}:{args.ntrip_port}\r\n"
        f"Ntrip-Version: Ntrip/2.0\r\n"
        f"User-Agent: NTRIP AdvancedNavigation Python SDK\r\n"
        f"Authorization: Basic {auth}\r\n"
        f"{ntrip_gga_header}"
        f"Connection: close\r\n\r\n"
    )
    writer.write(request.encode())
    await writer.drain()

    # Read HTTP response headers
    response_line = await reader.readline()
    if (
        not response_line.startswith(b"HTTP")
        and b"200 OK" not in response_line
        and b"ICY 200 OK" not in response_line
        and b"SOURCETABLE 200 OK" not in response_line
    ):
        print(f"Failed to connect to mountpoint: {response_line.decode().strip()}")
        writer.close()
        await writer.wait_closed()
        return

    # Read remaining headers
    while True:
        line = await reader.readline()
        if line == b"\r\n" or not line:
            break

    print(
        f"Connected to NTRIP mountpoint '{args.ntrip_mountpoint}'. Receiving RTCM corrections..."
    )

    # Periodic task to print the byte statistics
    async def print_stats_task():
        try:
            while True:
                await asyncio.sleep(1.0)
                print(
                    f"\r[NTRIP] Bytes Received: {state.bytes_received} B",
                    end="",
                    flush=True,
                )
        except asyncio.CancelledError:
            print()  # Print a newline so the terminal prompt isn't messed up

    stats_task = asyncio.create_task(print_stats_task())

    # Periodic NMEA sending task
    async def send_nmea_task():
        try:
            while True:
                await asyncio.sleep(15.0)
                if state.has_position:
                    gga = generate_gpgga(state.latitude, state.longitude, state.height)
                    writer.write(gga.encode())
                    await writer.drain()
        except asyncio.CancelledError:
            pass
        except OSError as e:
            print(f"Error sending NMEA: {e}")

    nmea_task = None
    if not args.ntrip_skip_forwarding_position:
        nmea_task = asyncio.create_task(send_nmea_task())

    try:
        while True:
            chunk = await reader.read(255)
            if not chunk:
                print("\nNTRIP connection closed by server.")
                break

            state.bytes_received += len(chunk)

            # Send RTCM chunk to the device
            rtcm_packet = RTCMCorrectionsPacket(packet_data=chunk)
            # Use expected_response=None so we don't wait/block on ACKs for RTCM packets
            await device.send(rtcm_packet, expected_response=None)

    except asyncio.CancelledError:
        pass
    except OSError as e:
        print(f"\nNTRIP client error: {e}")
    finally:
        stats_task.cancel()
        if nmea_task:
            nmea_task.cancel()
        writer.close()
        await writer.wait_closed()


async def fetch_sourcetable(args):
    """
    Connect to NTRIP server and retrieve the sourcetable to list available mountpoints.
    """
    print(f"Retrieving sourcetable from {args.ntrip_server}:{args.ntrip_port}...")
    try:
        reader, writer = await asyncio.open_connection(
            args.ntrip_server, args.ntrip_port
        )
    except OSError as e:
        print(f"Failed to connect to NTRIP caster: {e}")
        return []

    auth = base64.b64encode(f"{args.ntrip_user}:{args.ntrip_pass}".encode()).decode()

    request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {args.ntrip_server}:{args.ntrip_port}\r\n"
        f"Ntrip-Version: Ntrip/2.0\r\n"
        f"User-Agent: NTRIP AdvancedNavigation Python SDK\r\n"
        f"Authorization: Basic {auth}\r\n"
        f"Accept: */*\r\n"
        f"Connection: close\r\n\r\n"
    )
    writer.write(request.encode())
    await writer.drain()

    mountpoints = []
    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            line_str = line.decode("utf-8", errors="ignore").strip()
            if line_str.startswith("STR;"):
                parts = line_str.split(";")
                if len(parts) > 1:
                    nmea_required = False
                    if len(parts) > 11 and parts[11] == "1":
                        nmea_required = True
                    mountpoints.append({
                        "mountpoint": parts[1],
                        "nmea_required": nmea_required
                    })
        except OSError:
            break

    writer.close()
    await writer.wait_closed()
    return mountpoints


async def main():
    parser = argparse.ArgumentParser(
        description="Advanced Navigation NTRIP Client Example"
    )
    # Device connection args
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--serial",
        "-s",
        type=str,
        help="Serial communication port (e.g. /dev/ttyUSB0 or COM3)",
    )
    group.add_argument(
        "--ip",
        "-i",
        type=str,
        help="Device IP address (Connect via TCP)"
    )
    parser.add_argument(
        "--baud_rate",
        "-b",
        type=int,
        default=115200,
        help="Baud rate for Serial connection",
    )
    parser.add_argument("--port", "-p", type=int, default=16718, help="Device TCP port")

    # NTRIP server args
    parser.add_argument(
        "--ntrip_server",
        "-n",
        required=True,
        type=str,
        help="NTRIP server hostname or IP",
    )
    parser.add_argument(
        "--ntrip_port",
        "-r",
        type=int,
        default=2101,
        help="NTRIP server port (default: 2101)",
    )
    parser.add_argument(
        "--ntrip_user",
        "-u",
        required=True,
        type=str,
        help="NTRIP username"
    )
    parser.add_argument(
        "--ntrip_pass",
        "-x",
        required=True,
        type=str,
        help="NTRIP password"
    )
    parser.add_argument(
        "--ntrip_mountpoint",
        "-m",
        type=str,
        help="NTRIP mountpoint"
    )
    parser.add_argument(
        "--ntrip_skip_forwarding_position",
        "-f",
        action="store_true",
        help="Skip forwarding the device position to the NTRIP server",
    )

    args = parser.parse_args()

    if not args.ntrip_mountpoint:
        mountpoints = await fetch_sourcetable(args)
        if not mountpoints:
            print("No mountpoints found or failed to retrieve sourcetable.")
            return
        
        print("\nAvailable Mountpoints:")
        for i, mp in enumerate(mountpoints):
            print(f"{i + 1}. {mp['mountpoint']}")
        
        while True:
            try:
                choice_str = input("\nSelect a mountpoint number: ")
                choice = int(choice_str)
                if 1 <= choice <= len(mountpoints):
                    selected = mountpoints[choice - 1]
                    args.ntrip_mountpoint = selected["mountpoint"]
                    args.ntrip_skip_forwarding_position = not selected["nmea_required"]
                    print(f"Selected mountpoint: {args.ntrip_mountpoint}")
                    print(f"NMEA required by mountpoint: {selected['nmea_required']}\n")
                    break
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Please enter a valid number.")

    device = AnDevice()
    ntrip_state = NtripState()

    try:
        if args.ip is not None:
            print(f"Connecting via TCP to {args.ip}:{args.port}...")
            await device.connect_tcp(args.ip, args.port)
        else:
            print(f"Connecting via Serial to {args.serial} at {args.baud_rate} baud...")
            await device.connect_serial(args.serial, args.baud_rate)

        print("Waiting for device to come online...")
        await device.wait_online()
        print("Device is online.")

        # Register callback for SystemStatePacket to update position
        async def on_system_state(packet: SystemStatePacket):
            if packet.filter_status.ins_filter_initialised and (packet.latitude != 0.0 or packet.longitude != 0.0):
                ntrip_state.latitude = packet.latitude
                ntrip_state.longitude = packet.longitude
                ntrip_state.height = packet.height
                ntrip_state.has_position = True

        device.register_callback(SystemStatePacket, on_system_state)

        # Start NTRIP client
        await ntrip_client(args, device, ntrip_state)

    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    except (OSError, TimeoutError, RuntimeError, ValueError) as e:
        print(f"\nError: {e}")
    finally:
        device.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
