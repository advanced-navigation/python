################################################################################
##                                                                            ##
##                   Advanced Navigation Python Language SDK                  ##
##                                an_device.py                                ##
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
import logging
import struct
import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from advanced_navigation.an_devices.an_device_async_interface import AnDeviceInterface
from advanced_navigation.anpp_packets.an_packet_0 import (
    AcknowledgePacket,
    AcknowledgeResult,
)
from advanced_navigation.anpp_packets.an_packet_2 import BootMode, BootModePacket
from advanced_navigation.anpp_packets.an_packet_3 import DeviceInformationPacket
from advanced_navigation.anpp_packets.an_packet_8 import (
    FileTransferAcknowledgePacket,
    FileTransferResponse,
)
from advanced_navigation.anpp_packets.an_packet_9 import (
    FileTransferDataEncoding,
    FileTransferFirstPacket,
    FileTransferLimits,
    FileTransferMetadataType,
    FileTransferOngoingPacket,
)

logger = logging.getLogger(__name__)


class AnDevice(AnDeviceInterface):
    """
    High-level interface for Advanced Navigation devices.
    Inherits from AnDeviceInterface to provide specific functionality like boot mode management and firmware updates.
    """

    def __init__(self):
        """
        Initializes the AnDevice.
        """
        super().__init__()

    async def wait_online(self, timeout: int = 10):
        """
        Waits for the device to come online by requesting DeviceInformationPacket.

        Args:
            timeout (int): Maximum time to wait in seconds. Defaults to 10.

        Raises:
            Exception: If the device does not come online within the timeout.
        """
        start_time = time.monotonic()
        while (time.monotonic() - start_time) < timeout:
            device_info = await self.request(DeviceInformationPacket)
            if device_info is not None:
                return
        raise TimeoutError("Device offline")

    async def get_boot_mode(self) -> BootMode | None:
        """
        Retrieves the current boot mode of the device.

        Returns:
            Optional[BootMode]: The current boot mode, or None if the request fails.
        """
        response = await self.request(BootModePacket)
        if response and isinstance(response, BootModePacket):
            return response.boot_mode
        return None

    async def request_boot_mode(self, boot_mode: BootMode):
        """
        Requests the device to switch to a specific boot mode.
        Retries up to 3 times.

        Args:
            boot_mode (BootMode): The target boot mode.

        Raises:
            Exception: If the boot mode cannot be set after retries or if an error occurs.
        """
        for attempt in range(3):
            if await self.get_boot_mode() == boot_mode:
                logger.info("Already in boot mode %s", boot_mode)
                return
            packet = BootModePacket()
            packet.boot_mode = boot_mode
            ack = await self.send(packet)
            if ack and isinstance(ack, AcknowledgePacket):
                if ack.acknowledge_result == AcknowledgeResult.success:
                    await asyncio.sleep(0.5)
                    current_boot_mode = await self.get_boot_mode()
                    if current_boot_mode == boot_mode:
                        logger.info("Successfully entered boot mode %s", boot_mode)
                        return
                elif ack.acknowledge_result == AcknowledgeResult.failure_not_ready:
                    logger.debug(
                        "System not ready. Retrying entering boot mode %s", boot_mode
                    )
                else:
                    raise RuntimeError(
                        f"Unable to set bootmode: {ack.acknowledge_result}"
                    )
            await asyncio.sleep(0.5)
        raise TimeoutError("Unable to set bootmode: timeout")

    async def write_firmware(
        self,
        file_path: Path,
        on_progress: Callable[[int, int], Awaitable[None]] | None = None,
    ) -> bool:
        """
        Writes firmware to the device from a file.

        Args:
            file_path (Path): Path to the firmware file (.anfw).
            on_progress (Optional[Callable[[int, int], Awaitable[None]]]): Optional async callback
                invoked as ``await on_progress(bytes_sent, total_bytes)`` where both values are
                measured against the firmware payload (the metadata header is excluded). Fires
                once at 0 before the transfer starts, after each acknowledged fragment, and once
                at ``total_bytes`` on completion.

        Raises:
            Exception: If firmware validation fails or transfer fails.
        """
        AN_FIRMWARE_METADATA_SIZE = 48
        logger.info("Write firmware: %s", file_path)

        if not self.validate_firmware(file_path):
            raise ValueError("Invalid anfw file")

        file_data = await asyncio.to_thread(Path(file_path).read_bytes)

        # Generate a unique id for this file transfer
        transfer_id = int(time.time()) & 0x7FFFFFFF

        # Get the metadata at the beginning of the anfw file
        metadata = file_data[:AN_FIRMWARE_METADATA_SIZE]

        await self.transfer_file(
            file_data[AN_FIRMWARE_METADATA_SIZE:],
            transfer_id,
            FileTransferDataEncoding.aes256,
            FileTransferMetadataType.an_firmware,
            metadata,
            on_progress=on_progress,
        )
        return True

    def validate_firmware(self, file_path: Path) -> bool:
        """
        Validates the firmware file format.

        Args:
            file_path (Path): Path to the firmware file.

        Returns:
            bool: True if the file is a valid ANFW file, False otherwise.
        """
        AN_FIRMWARE_HEADER_LENGTH = 16
        logger.debug("Validating Firmware: %s", file_path)
        try:
            with open(file_path, "rb") as f:
                header = f.read(AN_FIRMWARE_HEADER_LENGTH)
                if len(header) < AN_FIRMWARE_HEADER_LENGTH:
                    return False

                identifier = header[0:4].decode("ascii")
                version = struct.unpack("<I", header[8:12])[0] / 1000.0
                timestamp = struct.unpack("<I", header[12:16])[0]

                if identifier == "ANFW":
                    date_str = datetime.fromtimestamp(
                        timestamp, tz=timezone.utc
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(
                        "Valid ANFW File found - Version: %s | Date: %s",
                        version,
                        date_str,
                    )
                    return True

        except (OSError, struct.error, UnicodeDecodeError) as e:
            logger.warning("Firmware validation error: %s", e)
        return False

    async def transfer_file(
        self,
        file_data: bytes,
        transfer_id: int,
        data_encoding: FileTransferDataEncoding,
        metadata_type: FileTransferMetadataType,
        metadata: bytes,
        on_progress: Callable[[int, int], Awaitable[None]] | None = None,
    ):
        """
        Transfers a file to the device using the ANPP file transfer protocol.

        Args:
            file_data (bytes): The content of the file to transfer.
            transfer_id (int): Unique ID for the transfer.
            data_encoding (FileTransferDataEncoding): Encoding of the data.
            metadata_type (FileTransferMetadataType): Type of metadata.
            metadata (bytes): Metadata bytes.
            on_progress (Optional[Callable[[int, int], Awaitable[None]]]): Optional async callback
                invoked as ``await on_progress(bytes_sent, total_bytes)`` where both values are
                measured against ``file_data`` (the metadata is excluded).

        Raises:
            Exception: If the transfer fails, times out, or receives an error response.
        """
        PACKET_RETRY_COUNT = 3

        logger.info("Transfer file start - Length: %s", len(file_data))

        retry = PACKET_RETRY_COUNT

        max_data_size = FileTransferLimits.max_data_size.value

        if len(metadata) > max_data_size:
            raise ValueError(f"Metadata to long {len(metadata)} > {max_data_size}")

        data_index = 0
        total_length = len(metadata) + len(file_data)
        payload_total = len(file_data)

        async def _emit(sent_index: int):
            if on_progress is None:
                return
            try:
                await on_progress(max(0, sent_index - len(metadata)), payload_total)
            except Exception as e:  # noqa: BLE001
                logger.warning("File transfer - progress callback raised: %s", e)

        await _emit(0)

        while data_index < total_length:
            packet: Any
            if data_index == 0:
                packet = FileTransferFirstPacket()
                packet.unique_id = transfer_id
                packet.data_index = 0
                packet.total_size = total_length
                packet.data_encoding = data_encoding
                packet.metadata_type = metadata_type
                packet.metadata_length = len(metadata)
                packet.packet_data = (
                    metadata
                    + file_data[0 : data_index + (max_data_size - len(metadata))]
                )
            else:
                packet = FileTransferOngoingPacket()
                packet.unique_id = transfer_id
                packet.data_index = data_index
                file_index = data_index - len(metadata)
                packet.packet_data = file_data[file_index : file_index + max_data_size]

            timeout = (
                10.0 if data_index == 0 else 3.0
            )  # Use a longer timeout for the very first packet
            response = await self.send(
                packet, expected_response=FileTransferAcknowledgePacket, timeout=timeout
            )

            if response and isinstance(response, FileTransferAcknowledgePacket):
                if response.unique_id != transfer_id:
                    raise ValueError(
                        f"Unexpected transfer id: {response.unique_id} expecting {transfer_id}"
                    )

                if (
                    response.response_code
                    == FileTransferResponse.completed_successfully
                ):
                    logger.info("File transfer complete")
                    await _emit(total_length)
                    return 0
                elif response.response_code == FileTransferResponse.ready:
                    data_index += len(packet.packet_data)
                    retry = PACKET_RETRY_COUNT
                    await _emit(data_index)
                elif response.response_code == FileTransferResponse.index_mismatch:
                    logger.warning(
                        "File transfer - index mismatch. Change index %s->%s",
                        data_index,
                        response.data_index,
                    )
                    data_index = response.data_index
                else:
                    raise RuntimeError(
                        f"Device returned error code: {response.response_code}"
                    )
            else:
                logger.warning(
                    "File transfer - unable to send fragment at %s", data_index
                )
                retry = retry - 1
                if retry <= 0:
                    raise TimeoutError(
                        f"File transfer - unable to send fragment at {data_index}"
                    )
