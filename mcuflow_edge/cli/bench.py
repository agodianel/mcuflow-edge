from pathlib import Path

import click

from mcuflow_edge.bench.parser import parse_bench_output
from mcuflow_edge.bench.report import write_bench_report


def run_bench(target: str, port: str) -> None:
    click.echo(f"Benchmarking {target} on {port}...")

    import serial

    report_dir = Path("reports/benchmarks")
    lines: list[str] = []

    try:
        with serial.Serial(port, 115200, timeout=10) as ser:
            click.echo("Reading benchmark output...")
            while True:
                raw = ser.readline()
                if not raw:
                    break
                line = raw.decode("utf-8", errors="replace").strip()
                if line:
                    click.echo(f"  {line}")
                    lines.append(line)
    except serial.SerialException as e:
        click.echo(f"Serial error: {e}", err=True)
        raise click.Abort() from None

    try:
        bench_data = parse_bench_output(lines)
    except ValueError as e:
        click.echo(f"Failed to parse benchmark: {e}", err=True)
        raise click.Abort() from None

    report_path = write_bench_report(
        target=target,
        board=f"{target}-board",
        model_name="model.tflite",
        bench_data=bench_data,
        report_dir=report_dir,
    )

    click.echo("Benchmark results:")
    click.echo(f"  Avg latency: {bench_data['latency_ms_avg']} ms")
    click.echo(f"  P95 latency: {bench_data['latency_ms_p95']} ms")
    click.echo(f"  Flash: {bench_data.get('flash_bytes', 'N/A')} bytes")
    click.echo(f"  RAM: {bench_data.get('ram_bytes', 'N/A')} bytes")
    click.echo(f"Report saved to {report_path}")
