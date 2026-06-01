"""Deploy logic for ESP32 targets.

Copies packaged model artifacts into the ESP32 firmware template
and prints next-step build/flash instructions.
"""

from pathlib import Path

import click

from mcuflow_edge.deploy.copier import copy_file
from mcuflow_edge.utils.jsonio import read_json


def deploy_esp32(package_dir: Path, firmware_dir: Path) -> dict:
    """Deploy packaged artifacts to the ESP32 firmware template.

    Args:
        package_dir: Directory containing pack artifacts.
        firmware_dir: Path to the ESP32 IDF project template.

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

    main_dir = firmware_dir / "main"
    copy_file(model_src, main_dir / "model.tflite")

    click.echo(f"  Copied model -> {main_dir / 'model.tflite'}")
    click.echo()
    click.echo("Next steps:")
    click.echo("  cd firmware/esp32-idf-template")
    click.echo("  idf.py set-target esp32s3")
    click.echo("  idf.py build")
    click.echo("  idf.py -p PORT flash monitor")

    return manifest
