"""STM32 target adapter implementation."""

from pathlib import Path

from mcuflow_edge.targets.base import TargetAdapter
from mcuflow_edge.targets.stm32.deployer import Stm32Deployer
from mcuflow_edge.targets.stm32.packager import Stm32Packager


class Stm32TargetAdapter(TargetAdapter):
    """Target adapter for STM32 boards using STM32Cube.AI."""

    name = "stm32"

    def validate_environment(self) -> None:
        """STM32 environment validation (IDE-driven, no CLI requirement)."""
        pass

    def pack_model(self, model_path: Path, output_dir: Path) -> None:
        """Package a .tflite model for STM32 deployment."""
        Stm32Packager.pack(model_path, output_dir)

    def deploy(self, package_dir: Path, **kwargs) -> None:
        """Deploy packaged artifacts into the STM32 firmware template."""
        firmware_dir = kwargs.get("firmware_dir")
        Stm32Deployer.deploy(
            package_dir,
            firmware_dir=Path(firmware_dir) if firmware_dir else None,
            port=kwargs.get("port"),
        )

    def benchmark(self, **kwargs) -> dict:
        """Read benchmark output from STM32 over serial."""
        from mcuflow_edge.bench.parser import parse_bench_output
        from mcuflow_edge.bench.serial_reader import read_bench_lines

        port = kwargs.get("port", "")
        lines = read_bench_lines(port)
        return parse_bench_output(lines)
