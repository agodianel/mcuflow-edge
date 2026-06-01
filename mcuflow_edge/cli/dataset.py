from pathlib import Path

import click

from mcuflow_edge.dataset.builder import build_dataset
from mcuflow_edge.dataset.export import export_csv


def run_build(session_dir: str, out: str) -> None:
    session_path = Path(session_dir)
    output_path = Path(out)

    if not session_path.is_dir():
        click.echo(f"Session directory not found: {session_dir}", err=True)
        raise click.Abort()

    click.echo(f"Building dataset from {session_dir} -> {out}")

    if output_path.suffix == ".csv":
        export_csv(session_path, output_path)
        click.echo(f"CSV dataset written to {output_path}")
    else:
        summary = build_dataset(session_path, output_path)
        click.echo("Dataset build complete.")
        click.echo(f"  Windows: {summary['total_windows']}")
        click.echo(f"  Labels: {summary['labels']}")
        click.echo(f"  Source sessions: {len(summary['source_sessions'])}")
