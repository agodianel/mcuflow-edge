from pathlib import Path

from mcuflow_edge.deploy.esp32 import deploy_esp32


class Esp32Deployer:
    @staticmethod
    def deploy(
        package_dir: Path, firmware_dir: Path | None = None, port: str | None = None
    ) -> dict:
        if firmware_dir is None:
            firmware_dir = Path("firmware/esp32-idf-template")
        if not firmware_dir.exists():
            raise FileNotFoundError(f"Firmware template not found: {firmware_dir}")
        return deploy_esp32(package_dir, firmware_dir)
