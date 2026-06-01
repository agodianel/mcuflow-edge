"""Shared serial benchmark reader for target adapters."""

import serial


def read_bench_lines(port: str, baudrate: int = 115200, timeout: int = 10) -> list[str]:
    """Read lines from a serial port until no more data arrives.

    Args:
        port: Serial port path (e.g. /dev/ttyUSB0).
        baudrate: Serial baud rate.
        timeout: Read timeout in seconds.

    Returns:
        List of decoded, stripped lines.
    """
    lines: list[str] = []
    with serial.Serial(port, baudrate, timeout=timeout) as ser:
        while True:
            raw = ser.readline()
            if not raw:
                break
            line = raw.decode("utf-8", errors="replace").strip()
            if line:
                lines.append(line)
    return lines
