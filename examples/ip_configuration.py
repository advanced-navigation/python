#!/usr/bin/env python3

################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                            ip_configuration.py                             ##
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
Read and write ANPP Packet 11 IP Configuration.

When no packet content configuration options are provided, the script queries
and prints the current settings.
When any packet content configuration options are provided, the script writes
the new settings and then queries the packet back again to check if the device
reports the new settings.
Omitted fields stay the same as last reported by the device.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import socket
import struct
import sys

from advanced_navigation.an_devices.an_device_async import AnDevice
from advanced_navigation.anpp_packets.an_packet_0 import AcknowledgeResult
from advanced_navigation.anpp_packets.an_packet_11 import (
    IPConfigurationPacket,
    LinkMode,
)

SYNTAX = """
syntax:
  ip_configuration.py (-s PORT | -i ADDRESS) [options]

examples:
  ip_configuration.py --serial /dev/ttyUSB0
  ip_configuration.py -s /dev/ttyUSB0 --baud_rate 115200
  ip_configuration.py -s /dev/ttyUSB0 --mode dhcp --automatic-dns 0 --dns-server 8.8.8.8
  ip_configuration.py -s /dev/ttyUSB0 --ethernet-disabled 1
  ip_configuration.py -s /dev/ttyUSB0 --ethernet-disabled 0 --permanent
  ip_configuration.py -s /dev/ttyUSB0 --automatic-dns 1 --link-mode auto
  ip_configuration.py -s /dev/ttyUSB0 --mode static --static-ip 192.168.1.50 --netmask 255.255.255.0 --gateway 192.168.1.1 --dns-server 8.8.8.8
  ip_configuration.py --ip 192.168.1.20
  ip_configuration.py --ip 192.168.1.20 --static-ip 192.168.1.50
""".strip()


def format_ipv4(value: int) -> str:
    # Packet 11 stores each IPv4 address little-endian. The integer value is
    # the address, and inet_ntoa expects that value in network byte order.
    return socket.inet_ntoa(struct.pack(">I", value & 0xFFFFFFFF))


def parse_ipv4(text: str) -> int:
    """Parse a dotted IPv4 address into the integer stored by packet 11."""
    try:
        return struct.unpack(">I", socket.inet_aton(text))[0]
    except OSError as exc:
        raise argparse.ArgumentTypeError(f"invalid IPv4 address: {text}") from exc


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ip_configuration.py",
        description="Read and write ANPP packet 11 IP Configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=SYNTAX,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--serial",
        "-s",
        type=str,
        help="Serial port for connection (e.g. /dev/ttyUSB0 or COM3)",
    )
    parser.add_argument(
        "--baud_rate",
        "-b",
        type=int,
        default=115200,
        help="Baud rate for a serial connection",
    )
    group.add_argument(
        "--ip",
        "-i",
        type=str,
        help="IP address for TCP network connection"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=16718,
        help="TCP port for network connection"
    )
    parser.add_argument(
        "--ethernet-disabled",
        type=int,
        choices=[0, 1],
        default=None,
        help="0 enables Ethernet, 1 disables it.",
    )
    parser.add_argument(
        "--mode",
        choices=["dhcp", "static"],
        default=None,
        help="Addressing mode. dhcp sets DHCP mode bit 0, static clears it.",
    )
    parser.add_argument(
        "--static-ip",
        type=parse_ipv4,
        default=None,
        metavar="ADDRESS",
        help="Static IPv4 address. Implies --mode static.",
    )
    parser.add_argument(
        "--automatic-dns",
        type=int,
        choices=[0, 1],
        default=None,
        help="0 disables automatic DNS, 1 enables it.",
    )
    parser.add_argument(
        "--link-mode",
        choices=[mode.name for mode in LinkMode],
        default=None,
        help="Ethernet link mode (DHCP mode bits 2-4).",
    )
    parser.add_argument(
        "--netmask",
        type=parse_ipv4,
        default=None,
        metavar="ADDRESS",
        help="IPv4 netmask.",
    )
    parser.add_argument(
        "--gateway",
        type=parse_ipv4,
        default=None,
        metavar="ADDRESS",
        help="IPv4 gateway.",
    )
    parser.add_argument(
        "--dns-server",
        type=parse_ipv4,
        default=None,
        metavar="ADDRESS",
        help="IPv4 DNS server.",
    )
    parser.add_argument(
        "--permanent",
        action="store_true",
        help="Store the written configuration in flash. Default is a temporary change.",
    )
    args = parser.parse_args(argv)
    if (args.static_ip is not None) and (args.mode == "dhcp"):
        parser.error("--static-ip cannot be used with --mode dhcp")
    if (args.static_ip is not None) and (args.mode is None):
        args.mode = "static"
    return args


def configuration_requested(args: argparse.Namespace) -> bool:
    return (
        (args.ethernet_disabled is not None)
        or (args.mode is not None)
        or (args.static_ip is not None)
        or (args.automatic_dns is not None)
        or (args.link_mode is not None)
        or (args.netmask is not None)
        or (args.gateway is not None)
        or (args.dns_server is not None)
    )


def verify_configuration(args: argparse.Namespace, packet: IPConfigurationPacket) -> int:
    """Return 0 when the device reports every requested setting."""
    mode = packet.dhcp_mode
    if (args.mode == "dhcp") and (not mode.dhcp_enabled):
        print("Device reported static addressing after a DHCP request.")
        return 1
    if (args.mode == "static") and mode.dhcp_enabled:
        print("Device reported DHCP after a static request.")
        return 1
    if (args.static_ip is not None) and (packet.ip_address != args.static_ip):
        print("Device reported IP "
            f"{format_ipv4(packet.ip_address)}, expected {format_ipv4(args.static_ip)}.")
        return 1
    if ((args.ethernet_disabled is not None)
        and (mode.ethernet_disabled != bool(args.ethernet_disabled))):
        print("Device reported a different ethernet_disabled value than requested.")
        return 1
    if ((args.automatic_dns is not None)
        and (mode.automatic_dns != bool(args.automatic_dns))):
        print("Device reported automatic_dns "
            f"{int(mode.automatic_dns)}, expected {args.automatic_dns}.")
        return 1
    if (args.link_mode is not None) and (mode.link_mode.name != args.link_mode):
        print(f"Device reported link_mode {mode.link_mode.name}, expected {args.link_mode}.")
        return 1
    if (args.netmask is not None) and (packet.ip_netmask != args.netmask):
        print("Device reported netmask "
            f"{format_ipv4(packet.ip_netmask)}, expected {format_ipv4(args.netmask)}.")
        return 1
    if (args.gateway is not None) and (packet.ip_gateway != args.gateway):
        print("Device reported gateway "
            f"{format_ipv4(packet.ip_gateway)}, expected {format_ipv4(args.gateway)}.")
        return 1
    if (args.dns_server is not None) and (packet.dns_server != args.dns_server):
        print("Device reported DNS server "
            f"{format_ipv4(packet.dns_server)}, expected {format_ipv4(args.dns_server)}.")
        return 1
    return 0


def print_ip_configuration(packet: IPConfigurationPacket) -> None:
    mode = packet.dhcp_mode
    addressing = "dhcp" if mode.dhcp_enabled else "static"
    print("IP Configuration (packet 11)")
    print(f"  permanent:         {packet.permanent}")
    print(f"  mode:              {addressing}")
    print(f"  dhcp_enabled:      {int(mode.dhcp_enabled)}")
    print(f"  automatic_dns:     {int(mode.automatic_dns)}")
    print(f"  link_mode:         {mode.link_mode.name}")
    print(f"  ethernet_disabled: {int(mode.ethernet_disabled)}")
    print(f"  ip_address:        {format_ipv4(packet.ip_address)}")
    print(f"  ip_netmask:        {format_ipv4(packet.ip_netmask)}")
    print(f"  ip_gateway:        {format_ipv4(packet.ip_gateway)}")
    print(f"  dns_server:        {format_ipv4(packet.dns_server)}")
    print(f"  serial_number:     {packet.serial_number}")


async def main(args: argparse.Namespace) -> int:
    device = AnDevice()
    try:
        try:
            if args.ip is not None:
                print(f"Connecting via TCP to {args.ip}:{args.port}...")
                await device.connect_tcp(args.ip, args.port)
            else:
                print(f"Connecting via Serial to {args.serial} at {args.baud_rate} baud...")
                await device.connect_serial(args.serial, args.baud_rate)
        except ConnectionRefusedError:
            print(
                f"Could not connect to {args.ip}:{args.port}. "
                "The host is reachable, but that TCP port is refused. "
                "Pass --port if the device listens on a different port."
            )
            return 1
        except OSError as exc:
            print(f"Could not connect: {exc}")
            return 1

        try:
            await device.wait_online()
        except TimeoutError:
            print(
                "Device did not respond. Check the serial port, baud rate, "
                "and that no other program has the port open."
            )
            return 1

        packet = await device.request(IPConfigurationPacket)
        if packet is None:
            print("Failed to read IP Configuration (packet 11).")
            return 1

        print("Current configuration:")
        print_ip_configuration(packet)

        if not configuration_requested(args):
            return 0

        if (args.mode == "dhcp"):
            packet.dhcp_mode.dhcp_enabled = True
        elif (args.mode == "static"):
            packet.dhcp_mode.dhcp_enabled = False
        if (args.static_ip is not None):
            packet.ip_address = args.static_ip
        if (args.ethernet_disabled is not None):
            packet.dhcp_mode.ethernet_disabled = bool(args.ethernet_disabled)
        if (args.automatic_dns is not None):
            packet.dhcp_mode.automatic_dns = bool(args.automatic_dns)
        if (args.link_mode is not None):
            packet.dhcp_mode.link_mode = LinkMode[args.link_mode]
        if (args.netmask is not None):
            packet.ip_netmask = args.netmask
        if (args.gateway is not None):
            packet.ip_gateway = args.gateway
        if (args.dns_server is not None):
            packet.dns_server = args.dns_server
        packet.permanent = 1 if args.permanent else 0

        changes = []
        if (args.mode is not None):
            changes.append(f"mode={args.mode}")
        if (args.static_ip is not None):
            changes.append(f"ip_address={format_ipv4(args.static_ip)}")
        if (args.ethernet_disabled is not None):
            changes.append(
                "ethernet_disabled="
                f"{int(packet.dhcp_mode.ethernet_disabled)}"
            )
        if (args.automatic_dns is not None):
            changes.append(f"automatic_dns={args.automatic_dns}")
        if (args.link_mode is not None):
            changes.append(f"link_mode={args.link_mode}")
        if (args.netmask is not None):
            changes.append(f"ip_netmask={format_ipv4(args.netmask)}")
        if (args.gateway is not None):
            changes.append(f"ip_gateway={format_ipv4(args.gateway)}")
        if (args.dns_server is not None):
            changes.append(f"dns_server={format_ipv4(args.dns_server)}")
        changes.append(f"permanent={packet.permanent}")
        print()
        print("Writing " + ", ".join(changes) + "...")
        ack = await device.send(packet)
        if (ack is None):
            print("No acknowledgement received.")
            return 1
        if (ack.acknowledge_result != AcknowledgeResult.success):
            print(f"Device rejected the packet: {ack.acknowledge_result.name}")
            return 1

        print("Write acknowledged.\n\nReading configuration again...")
        updated = await device.request(IPConfigurationPacket)
        if (updated is None):
            print("Write succeeded, but the follow-up read failed.")
            return 1

        print_ip_configuration(updated)
        return verify_configuration(args, updated)
    finally:
        device.close()


if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(level=logging.WARNING)
    try:
        sys.exit(asyncio.run(main(args)))
    except KeyboardInterrupt:
        sys.exit(130)
