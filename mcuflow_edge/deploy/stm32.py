"""Deploy logic for STM32 targets.

Copies packaged model artifacts into the STM32 firmware template
and prints next-step build/flash instructions.
"""

from pathlib import Path

import click

from mcuflow_edge.deploy.copier import copy_file
from mcuflow_edge.utils.jsonio import read_json


def deploy_stm32(package_dir: Path, firmware_dir: Path) -> dict:
    """Deploy packaged artifacts to the STM32 firmware template.

    Args:
        package_dir: Directory containing pack artifacts.
        firmware_dir: Path to the STM32 Cube project template.

    Returns:
        The parsed pack manifest dictionary.
    """
    manifest_path = package_dir / "pack_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Package manifest not found: {manifest_path}")

    manifest = read_json(manifest_path)
    model_src = package_dir / "model.tflite"
    if not model_src.exists():
        raise FileNotFoundError(f"Model not found: {model_src}")

    ai_dir = firmware_dir / "X-CUBE-AI"
    ai_dir.mkdir(parents=True, exist_ok=True)
    copy_file(model_src, ai_dir / "model.tflite")

    click.echo(f"  Copied model -> {ai_dir / 'model.tflite'}")
    click.echo()
    click.echo("Next steps:")
    click.echo("  1. Open the STM32CubeIDE project in firmware/stm32-cube-template")
    click.echo("  2. Run STM32Cube.AI to regenerate integration files")
    click.echo("  3. Build and flash the project")

    return manifest
