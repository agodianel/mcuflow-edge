"""CLI command: pack — package a trained model for a target."""

from pathlib import Path

import click

from mcuflow_edge.targets import get_adapter


def run_pack(target: str, model: str) -> None:
    model_path = Path(model)
    if not model_path.exists():
        click.echo(f"Model not found: {model}", err=True)
        raise click.Abort()

    try:
        adapter = get_adapter(target)
    except KeyError as e:
        click.echo(str(e), err=True)
        raise click.Abort() from None

    output_dir = Path("artifacts/pack")
    click.echo(f"Packaging {model} for {target}...")
    adapter.pack_model(model_path, output_dir)

    target_dir = output_dir / target
    click.echo(f"Package created at {target_dir}")
    click.echo(f"  manifest: {target_dir / 'pack_manifest.json'}")
    click.echo(f"  model:    {target_dir / 'model.tflite'}")
    click.echo(f"  info:     {target_dir / 'model_info.json'}")
