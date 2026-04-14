# Advanced Navigation Python SDK - Test Suite

This directory contains the automated testing suite for the Advanced Navigation Python SDK. These tests are essential for maintaining the reliability, correctness, and stability of the SDK, particularly for the Advanced Navigation Packet Protocol (ANPP) encoding and decoding logic.

While these tests are automatically executed by our Continuous Integration (CI) pipeline.

## Running the Tests

The test suite is built using [`pytest`](https://docs.pytest.org/). To run the tests locally, ensure you have the testing dependencies installed in your Python environment.

### Prerequisites

You can install the required dependencies via pip:

```bash
pip install pytest
```

### Execution

To execute the test suite, simply run the following command from the root directory of the repository:

```bash
pytest tests/
```

This will automatically discover and run all the tests, providing a summary of passes and failures.

## Directory Structure

* **`anpp_packets_tests/`**: Contains comprehensive unit tests for the ANPP packets.
  * `encode_test.py`: Validates that Python packet objects correctly encode into raw binary data.
  * `decode_test.py`: Validates that raw binary data (such as the data stored in `Log.anpp`) correctly parses into Python packet objects.
  * `encode_decode_test.py`: Validates roundtrip serialization (encoding a packet and immediately decoding it yields the exact same data).
  * `test_utils.py`: Shared helper utilities and class mappings used across the test suite.
  * `Log.anpp`: A sample binary log file containing real-world sensor data used to test the decoding logic.
