"""Base target adapter interface.

All target-specific adapters (ESP32, STM32, etc.) must subclass
TargetAdapter and implement its abstract methods.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class TargetAdapter(ABC):
    """Abstract base class for MCU target adapters.

    Each target adapter encapsulates the target-specific logic for
    environment validation, model packaging, firmware deployment,
    and benchmark data collection.
    """

    name: str

    @abstractmethod
    def validate_environment(self) -> None:
        """Check that required tools and SDKs are available.

        Raises:
            RuntimeError: If the environment is not properly configured.
        """
        ...

    @abstractmethod
    def pack_model(self, model_path: Path, output_dir: Path) -> None:
        """Package a trained model for this target.

        Args:
            model_path: Path to the .tflite model file.
            output_dir: Directory to write packaged artifacts into.
        """
        ...

    @abstractmethod
    def deploy(self, package_dir: Path, **kwargs) -> None:
        """Deploy packaged artifacts into a firmware template.

        Args:
            package_dir: Path to the pack output directory.
            **kwargs: Target-specific options (port, firmware_dir, etc.).
        """
        ...

    @abstractmethod
    def benchmark(self, **kwargs) -> dict:
        """Run benchmark and return parsed results.

        Args:
            **kwargs: Target-specific options (port, etc.).

        Returns:
            Dictionary with benchmark metrics (latency, memory, etc.).
        """
        ...
