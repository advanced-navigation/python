################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                           an_device_interface.py                           ##
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

import asyncio
import copy
import serial_asyncio  # type: ignore
import logging
from typing import Callable, Dict, Any, Type, Optional, List, Tuple

from advanced_navigation.anpp_packets.an_packets import PacketID
from advanced_navigation.anpp_packets.an_packet_protocol import ANDecoder, ANPacket
from advanced_navigation.anpp_packets.an_packet_0 import AcknowledgePacket
from advanced_navigation.anpp_packets.an_packet_1 import RequestPacket


class AnDeviceInterfaceProtocol(asyncio.Protocol):
    """
    Asyncio Protocol implementation for handling Advanced Navigation Packet Protocol (ANPP) communication.
    """

    def __init__(
        self,
        on_packet_received: Callable[[ANPacket], Any],
        on_connection_state_change: Callable[[bool], Any] | None = None,
    ):
        """
        Initializes the protocol.

        Args:
            on_packet_received (Callable[[ANPacket], Any]): Callback function to handle received packets.
            on_connection_state_change (Callable[[bool], Any] | None, optional): Callback function to handle connection state changes. Defaults to None.
        """
        self._receive_queue: asyncio.Queue[ANPacket] = asyncio.Queue()
        self._on_packet_received = on_packet_received
        self._on_connection_state_change = on_connection_state_change
        self._transport: Optional[asyncio.Transport] = None
        self._decoder = ANDecoder()
        self._worker_task = asyncio.create_task(self._worker())

    async def _worker(self):
        """
        Worker coroutine that processes packets from the receive queue.
        """
        while True:
            try:
                an_packet = await self._receive_queue.get()
                await self._on_packet_received(an_packet)
                self._receive_queue.task_done()
            except Exception as e:
                logging.error(f"Worker task error: {e}")

    def connection_made(self, transport):
        """
        Called when a connection is made.

        Args:
            transport (asyncio.Transport): The transport associated with the connection.
        """
        self._transport = transport
        logging.info("Connection established!")
        if self._on_connection_state_change:
            asyncio.create_task(self._on_connection_state_change(True))

    def data_received(self, data: bytes):
        """
        Called when data is received. Handles incoming byte chunks and assemble ANPP packets.

        Args:
            data (bytes): The received data.
        """
        self._decoder.add_data(packet_bytes=data)
        while True:
            an_packet = self._decoder.decode()
            if an_packet is None:
                break
            self._receive_queue.put_nowait(copy.deepcopy(an_packet))
            self._decoder.remove_processed_data()

    def send(self, packet: ANPacket):
        """
        Sends a packet over the transport.

        Args:
            packet (ANPacket): The packet to send.
        """
        if self._transport:
            self._transport.write(packet.bytes())

    def connection_lost(self, exc):
        """
        Called when the connection is lost or closed.

        Args:
            exc (Exception): The exception that caused the connection loss, or None if closed cleanly.
        """
        logging.info(f"Connection lost: {exc}")
        self._transport = None
        if self._on_connection_state_change:
            asyncio.create_task(self._on_connection_state_change(False))


class AnDeviceInterface:
    """
    Interface for communicating with Advanced Navigation devices via TCP or Serial.
    """

    def __init__(self):
        """
        Initializes the AnDeviceInterface.
        """
        self._protocol: Optional[AnDeviceInterfaceProtocol] = None
        self._callbacks: Dict[PacketID, List[Tuple[Callable, Type]]] = {}
        self._raw_callbacks: List[Callable] = []

    def register_callback(self, packet_type: Type, callback: Callable):
        """
        Registers a callback for a specific packet type.

        Args:
            packet_type (Type): The class of the packet to listen for.
            callback (Callable): The function to call when the packet is received.
        """
        if packet_type.ID not in self._callbacks:
            self._callbacks[packet_type.ID] = []
        self._callbacks[packet_type.ID].append((callback, packet_type))

    def register_raw_callback(self, callback: Callable):
        """
        Registers a callback for all received raw ANPackets.

        Args:
            callback (Callable): The function to call when any raw packet is received.
        """
        self._raw_callbacks.append(callback)

    async def connect_tcp(self, host: str, port: int):
        """
        Connects to a device via TCP.

        Args:
            host (str): The hostname or IP address.
            port (int): The port number.
        """
        loop = asyncio.get_running_loop()
        _, protocol = await loop.create_connection(
            lambda: AnDeviceInterfaceProtocol(
                self._handle_recv_packet, self._handle_connection_state_change
            ),
            host,
            port,
        )
        self._protocol = protocol

    async def connect_serial(self, com_port: str, baudrate: int = 115200):
        """
        Connects to a device via Serial.

        Args:
            com_port (str): The COM port (e.g., 'COM1', '/dev/ttyUSB0').
            baudrate (int, optional): The baud rate. Defaults to 115200.
        """
        loop = asyncio.get_running_loop()
        _, protocol = await serial_asyncio.create_serial_connection(
            loop,
            lambda: AnDeviceInterfaceProtocol(
                self._handle_recv_packet, self._handle_connection_state_change
            ),
            com_port,
            baudrate=baudrate,
        )
        self._protocol = protocol

    def close(self):
        """
        Closes the connection.
        """
        if self._protocol and self._protocol._transport:
            self._protocol._transport.close()

    async def _handle_connection_state_change(self, connected_state: bool):
        """
        Internal handler for connection state changes.

        Args:
            connected_state (bool): True if connected, False otherwise.
        """
        pass

    async def _handle_recv_packet(self, an_packet: ANPacket):
        """
        Internal handler for received raw ANPackets. Decodes them and triggers callbacks.

        Args:
            an_packet (ANPacket): The received raw packet.
        """
        # Generic handler for raw packets
        for callback in self._raw_callbacks:
            try:
                await callback(an_packet)
            except Exception as e:
                logging.warning(f"Failed to handle raw callback: {e}")

        try:
            packet_id = PacketID(an_packet.id)
        except ValueError:
            logging.warning(f"Received unknown packet ID: {an_packet.id}")
            return

        if packet_id in self._callbacks:
            callbacks = self._callbacks[packet_id]
            for callback, packet_type in callbacks:
                try:
                    if packet_type is not None:
                        packet = packet_type()
                        if packet.decode(an_packet) == 0:
                            await callback(packet)
                        else:
                            logging.warning(f"Failed to decode packet {packet_id}")
                except Exception as e:
                    logging.warning(f"Failed to handle packet {packet_id}: {e}")
        else:
            # We don't have a specific handler for this packet ID
            if not self._raw_callbacks:
                logging.debug(f"Packet {an_packet.id} not handled")

    # System Packets
    async def request(self, packet_type: Any, timeout: float = 1.0) -> Optional[Any]:
        """
        Request a packet and wait for the response.

        Args:
            packet_type (type): The class of the packet to request.
            timeout (float, optional): Timeout in seconds. Defaults to 1.0.

        Returns:
            Optional[Any]: The decoded packet object or None if timeout/error occurs.
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        async def one_shot_callback(packet):
            if not future.done():
                future.set_result(packet)

        self.register_callback(packet_type, one_shot_callback)

        try:
            self.send_request_packet(packet_type.ID)
            return await asyncio.wait_for(future, timeout)
        except Exception:
            return None
        finally:
            if packet_type.ID in self._callbacks:
                self._callbacks[packet_type.ID] = [
                    cb
                    for cb in self._callbacks[packet_type.ID]
                    if cb[0] != one_shot_callback
                ]

    async def send(
        self,
        send_packet: Any,
        expected_response: Optional[Any] = AcknowledgePacket,
        timeout: float = 1.0,
    ) -> Optional[AcknowledgePacket]:
        """
        Sends a packet and optionally waits for an acknowledgement or specific response.

        Args:
            send_packet (Any): The packet object to send.
            expected_response (Optional[Any], optional): The class of the expected response packet. Defaults to AcknowledgePacket.
            timeout (float, optional): Timeout in seconds. Defaults to 1.0.

        Returns:
            Optional[AcknowledgePacket]: The received response packet or None if timeout/error occurs.
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        async def one_shot_callback(recev_packet):
            if isinstance(recev_packet, AcknowledgePacket):
                # Does this ack belong to the sent packet?
                if recev_packet.packet_id == send_packet.ID:
                    if not future.done():
                        future.set_result(recev_packet)
            else:
                if not future.done():
                    future.set_result(recev_packet)

        if expected_response is not None:
            self.register_callback(expected_response, one_shot_callback)

        try:
            if self._protocol:
                self._protocol.send(send_packet.encode())

            if expected_response is not None:
                return await asyncio.wait_for(future, timeout)
            return None
        except Exception as ex:
            logging.warning(f"Failed to send packet: {ex}")
            return None
        finally:
            if (
                expected_response
                and hasattr(expected_response, "ID")
                and expected_response.ID in self._callbacks
            ):
                self._callbacks[expected_response.ID] = [
                    cb
                    for cb in self._callbacks[expected_response.ID]
                    if cb[0] != one_shot_callback
                ]

    def send_request_packet(self, packet_id: PacketID):
        """
        Sends a request packet for a specific packet ID.

        Args:
            packet_id (PacketID): The ID of the packet to request.
        """
        request = RequestPacket()
        request.requested_packets = [packet_id]
        if self._protocol:
            self._protocol.send(request.encode())
