from pathlib import Path

from mcuflow_edge.deploy.stm32 import deploy_stm32


class Stm32Deployer:
    @staticmethod
    def deploy(
        package_dir: Path, firmware_dir: Path | None = None, port: str | None = None
    ) -> dict:
        if firmware_dir is None:
            firmware_dir = Path("firmware/stm32-cube-template")
        if not firmware_dir.exists():
            raise FileNotFoundError(f"Firmware template not found: {firmware_dir}")
        return deploy_stm32(package_dir, firmware_dir)
