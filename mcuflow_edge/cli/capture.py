import time
from pathlib import Path

import click

from mcuflow_edge.capture.serial_reader import parse_sample_line
from mcuflow_edge.capture.session import (
    CaptureSample,
    CaptureSession,
    generate_session_id,
    write_session,
)


def run_capture(
    target: str,
    port: str,
    label: str,
    duration: int | None,
    session_name: str | None,
    sample_rate: int | None,
) -> None:
    import serial

    session_id = session_name or generate_session_id(target, label)
    samples: list[CaptureSample] = []

    click.echo(f"Capturing {label} from {target} on {port}...")
    click.echo("Press Ctrl+C to stop.")

    session_path = Path("sessions")
    session_path.mkdir(parents=True, exist_ok=True)

    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            start_time = time.monotonic()
            while True:
                if duration and (time.monotonic() - start_time) >= duration:
                    break
                raw = ser.readline()
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="replace").strip()
                sample = parse_sample_line(line)
                if sample is not None:
                    sample.label = label
                    samples.append(sample)

    except serial.SerialException as e:
        click.echo(f"Serial error: {e}", err=True)
        raise click.Abort() from None
    except KeyboardInterrupt:
        click.echo("\nCapture stopped.")

    if not samples:
        click.echo("No samples captured.", err=True)
        raise click.Abort()

    session = CaptureSession(
        session_id=session_id,
        target=target,
        board=f"{target}-board",
        sensor="imu",
        sample_rate_hz=sample_rate or 100,
        label=label,
        samples=samples,
    )

    jsonl_path, meta_path = write_session(session, session_path)
    click.echo(f"Saved {len(samples)} samples to:")
    click.echo(f"  {jsonl_path}")
    click.echo(f"  {meta_path}")
