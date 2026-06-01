"""CLI command: deploy — move packaged artifacts into firmware template."""

from pathlib import Path

import click

from mcuflow_edge.targets import get_adapter

FIRMWARE_DIRS = {
    "esp32": "firmware/esp32-idf-template",
    "stm32": "firmware/stm32-cube-template",
}


def run_deploy(target: str, port: str | None, project: str | None) -> None:
    click.echo(f"Deploying to {target}...")

    try:
        adapter = get_adapter(target)
    except KeyError as e:
        click.echo(str(e), err=True)
        raise click.Abort() from None

    package_dir = Path(f"artifacts/pack/{target}")
    if not package_dir.exists():
        click.echo(f"Package directory not found: {package_dir}", err=True)
        click.echo("Run 'mcue pack' first.", err=True)
        raise click.Abort()

    firmware_dir = project if project else FIRMWARE_DIRS.get(target)
    adapter.deploy(package_dir, firmware_dir=firmware_dir, port=port)
    click.echo("Deploy complete.")
