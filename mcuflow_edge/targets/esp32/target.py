"""ESP32 target adapter implementation."""

from pathlib import Path

from mcuflow_edge.targets.base import TargetAdapter
from mcuflow_edge.targets.esp32.deployer import Esp32Deployer
from mcuflow_edge.targets.esp32.packager import Esp32Packager


class Esp32TargetAdapter(TargetAdapter):
    """Target adapter for ESP32 boards using ESP-IDF + TensorFlow Lite Micro."""

    name = "esp32"

    def validate_environment(self) -> None:
        """Check that ESP-IDF toolchain is available."""
        import shutil

        if not shutil.which("idf.py"):
            raise RuntimeError(
                "ESP-IDF not found. Install ESP-IDF and add idf.py to PATH."
            )

    def pack_model(self, model_path: Path, output_dir: Path) -> None:
        """Package a .tflite model for ESP32 deployment."""
        Esp32Packager.pack(model_path, output_dir)

    def deploy(self, package_dir: Path, **kwargs) -> None:
        """Deploy packaged artifacts into the ESP32 firmware template."""
        port = kwargs.get("port")
        firmware_dir = kwargs.get("firmware_dir")
        Esp32Deployer.deploy(
            package_dir,
            firmware_dir=Path(firmware_dir) if firmware_dir else None,
            port=port,
        )

    def benchmark(self, **kwargs) -> dict:
        """Read benchmark output from ESP32 over serial."""
        from mcuflow_edge.bench.parser import parse_bench_output
        from mcuflow_edge.bench.serial_reader import read_bench_lines

        port = kwargs.get("port", "")
        lines = read_bench_lines(port)
        return parse_bench_output(lines)
