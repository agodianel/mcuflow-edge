"""Implements the `mcue init` command — creates a starter workspace."""

from pathlib import Path

import click
import yaml

_DEFAULT_CONFIG = {
    "project": {
        "name": "imu-gesture",
        "example": "imu-gesture",
    },
    "capture": {
        "sensor": "imu",
        "axes": ["ax", "ay", "az", "gx", "gy", "gz"],
        "sample_rate_hz": 100,
        "window_size": 128,
    },
    "labels": ["idle", "shake", "tilt_left", "tilt_right", "tap"],
    "targets": {
        "esp32": {
            "board": "esp32-s3-devkit",
            "port": "/dev/ttyUSB0",
        },
        "stm32": {
            "board": "stwinbox",
            "port": "/dev/tty.usbmodemXXXX",
        },
    },
    "artifacts": {
        "root": "./artifacts",
        "sessions": "./sessions",
        "reports": "./reports",
    },
}

_WORKSPACE_DIRS = [
    "sessions",
    "artifacts",
    "reports",
    "models",
]


def run_init(example: str) -> None:
    """Create a starter workspace for the given example."""
    click.echo(f"Initializing workspace for example: {example}")

    root = Path.cwd()

    # Create workspace directories
    created_dirs: list[str] = []
    for dirname in _WORKSPACE_DIRS:
        dirpath = root / dirname
        dirpath.mkdir(parents=True, exist_ok=True)
        created_dirs.append(dirname)

    # Copy labels.yaml from the bundled example if available
    labels_dst = root / "labels.yaml"
    if not labels_dst.exists():
        example_labels = (
            Path(__file__).resolve().parent.parent.parent
            / "examples" / example / "labels.yaml"
        )
        if example_labels.exists():
            labels_dst.write_text(example_labels.read_text())
            click.echo(f"  Created labels.yaml (from {example} example)")
        else:
            # Generate default labels file
            labels_data = {"labels": _DEFAULT_CONFIG["labels"]}
            labels_dst.write_text(
                yaml.dump(labels_data, default_flow_style=False, sort_keys=False)
            )
            click.echo("  Created labels.yaml (defaults)")

    # Generate mcuflow.yaml project config
    config_path = root / "mcuflow.yaml"
    if not config_path.exists():
        config = dict(_DEFAULT_CONFIG)
        config["project"]["name"] = example
        config["project"]["example"] = example
        config_path.write_text(
            yaml.dump(config, default_flow_style=False, sort_keys=False)
        )
        click.echo("  Created mcuflow.yaml")
    else:
        click.echo("  mcuflow.yaml already exists, skipping")

    click.echo(f"  Created directories: {', '.join(created_dirs)}")
    click.echo("")
    click.echo("Workspace ready. Next steps:")
    click.echo("  mcue capture --target esp32 --port /dev/ttyUSB0 --label idle")
    click.echo("  mcue capture --target esp32 --port /dev/ttyUSB0 --label shake")
