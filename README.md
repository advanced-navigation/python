# Advanced Navigation Python SDK

Welcome to the **Advanced Navigation Python SDK**!

This SDK provides a comprehensive suite of tools for interfacing with Advanced Navigation Inertial Navigation Systems (INS). It simplifies the process of establishing communication over Serial, TCP, or UDP, decoding Advanced Navigation Packet Protocol (ANPP) packets, and programmatically configuring Advanced Navigation devices.

## Features
- **ANPP Protocol Support**: Complete implementation of the Advanced Navigation Packet Protocol (ANPP) for encoding and decoding binary data streams.
- **Asynchronous & Synchronous I/O**: Supports both `asyncio` for high-performance concurrent applications, and synchronous serial/TCP communication for simpler scripts.
- **Device Management**: Easily configure sensors, offsets, baud rates, and request state variables.
- **Cross-Platform**: Works on Linux, Windows, and macOS.

---

## Installation

The SDK is available on PyPI and can be installed via pip:

```bash
pip install advanced_navigation
```

*(Note: Requires Python 3.10+)*

---

## Quickstart

Here is a quick example of how to connect to an Advanced Navigation device (such as Certus or Spatial) over a serial port, read the device information, and continuously listen to the system state asynchronously using the `AnDevice` interface:

```python
import asyncio
from datetime import datetime, timezone
from advanced_navigation.an_devices.an_device_async import AnDevice
from advanced_navigation.anpp_packets.an_packet_3 import DeviceInformationPacket
from advanced_navigation.anpp_packets.an_packet_20 import SystemStatePacket

async def handle_state_packet(state: SystemStatePacket):
    """Callback function triggered every time a SystemStatePacket is received."""
    device_time = datetime.fromtimestamp(
        state.unix_time_seconds + (state.microseconds / 1000000), 
        tz=timezone.utc
    )
    print(f"[{device_time}] Lat: {state.latitude:.6f}, Lon: {state.longitude:.6f}, Height: {state.height:.2f}m")

async def main():
    # Initialize the device
    device = AnDevice()
    
    # Connect via Serial Port (replace with your port, e.g. COM3 or /dev/ttyUSB0)
    await device.connect_serial(port="/dev/ttyUSB0", baud_rate=115200)
    
    print("Connecting to device...")
    await device.wait_online()
    
    # Request Device Information (Packet 3)
    info = await device.request(DeviceInformationPacket)
    if info:
        print(f"Connected! Device ID {info.device_id} | Hardware v{info.hardware_revision/1000} | Software v{info.software_version/1000}")

    # Register a callback to listen to the continuous System State stream (Packet 20)
    device.register_callback(SystemStatePacket, handle_state_packet)
    
    print("Listening for state updates... (Press Ctrl+C to stop)")
    try:
        # Keep the event loop running
        await asyncio.Future()
    except asyncio.CancelledError:
        pass
    finally:
        device.close()

if __name__ == "__main__":
    asyncio.run(main())
```

For more comprehensive examples—including synchronous operations, TCP logging, firmware updating, and specific device configurations—check out the `examples/` directory in this repository.

---

## Product Manuals

The Advanced Navigation SDK supports all INS devices using the ANPP protocol. For further detail on specific product configurations, mounting instructions, and operational capabilities, please see the following documentation:

- [Air Data Unit](https://www.advancednavigation.com/accessories/speed-sensors/air-data-unit/)
- [Boreas A50/D50](https://www.advancednavigation.com/inertial-navigation-systems/fog-gnss-ins/boreas-50/)
- [Boreas A70/A90](https://www.advancednavigation.com/imu-ahrs/fog-imu/boreas-a/)
- [Boreas D70/D90](https://www.advancednavigation.com/inertial-navigation-systems/fog-gnss-ins/boreas/)
- [Certus](https://www.advancednavigation.com/inertial-navigation-systems/mems-gnss-ins/certus/)
- [Certus Evo](https://www.advancednavigation.com/inertial-navigation-systems/mems-gnss-ins/certus-evo/)
- [Certus Mini A](https://www.advancednavigation.com/imu-ahrs/mems-imu/certus-mini-a/)
- [Certus Mini D](https://www.advancednavigation.com/inertial-navigation-systems/mems-gnss-ins/certus-mini-d/)
- [Certus Mini N](https://www.advancednavigation.com/inertial-navigation-systems/mems-gnss-ins/certus-mini-n/)
- [GNSS Compass](https://www.advancednavigation.com/inertial-navigation-systems/satellite-compass/gnss-compass/)
- [Motus](https://www.advancednavigation.com/imu-ahrs/mems-imu/motus/)
- [Orientus](https://www.advancednavigation.com/imu-ahrs/mems-imu/orientus/)
- [Spatial](https://www.advancednavigation.com/inertial-navigation-systems/mems-gnss-ins/spatial/)
- [Spatial Fog Dual](https://www.advancednavigation.com/inertial-navigation-systems/fog-gnss-ins/spatial-fog-dual/)

---

## Contributing

We welcome contributions to the Advanced Navigation Python SDK! 

If you are developing a new feature, or addressing a bug:

1. **Fork the repository** and create a feature branch.
2. **Implement your changes**.
3. **Run the tests locally** to verify that your changes pass successfully without breaking existing logic:
   ```bash
   pip install pytest
   pytest tests/
   ```
4. **Format and lint** your code (we use standard Python linting like `ruff`).
5. **Open a Pull Request** describing your changes.

For deeper insights into how the testing suite operates, refer to `tests/README.md`.
