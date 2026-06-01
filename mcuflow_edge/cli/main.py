import click


@click.group()
def cli():
    """MCUflow-Edge: unified edge AI workflow for ESP32 and STM32."""


@cli.command()
@click.argument("example", default="imu-gesture")
def init(example):
    """Create a starter workspace for the given example."""
    from mcuflow_edge.cli.init import run_init
    run_init(example)


@cli.command()
@click.option("--target", required=True, type=click.Choice(["esp32", "stm32"]))
@click.option("--port", required=True)
@click.option("--label", required=True)
@click.option("--duration", type=int, default=None)
@click.option("--session-name", default=None)
@click.option("--sample-rate", type=int, default=None)
def capture(target, port, label, duration, session_name, sample_rate):
    """Connect to a board and capture labeled sensor samples."""
    from mcuflow_edge.cli.capture import run_capture
    run_capture(target, port, label, duration, session_name, sample_rate)


@cli.group()
def dataset():
    """Dataset operations."""


@dataset.command()
@click.argument("session_dir", type=click.Path(exists=True))
@click.option("--out", required=True)
def build(session_dir, out):
    """Build a training-ready dataset from session files."""
    from mcuflow_edge.cli.dataset import run_build
    run_build(session_dir, out)


@cli.command()
@click.option("--target", required=True, type=click.Choice(["esp32", "stm32"]))
@click.option("--model", required=True, type=click.Path(exists=True))
def pack(target, model):
    """Package a trained model for a target."""
    from mcuflow_edge.cli.pack import run_pack
    run_pack(target, model)


@cli.command()
@click.option("--target", required=True, type=click.Choice(["esp32", "stm32"]))
@click.option("--port", default=None)
@click.option("--project", type=click.Path(), default=None)
def deploy(target, port, project):
    """Deploy packaged artifacts into firmware template."""
    from mcuflow_edge.cli.deploy import run_deploy
    run_deploy(target, port, project)


@cli.command()
@click.option("--target", required=True, type=click.Choice(["esp32", "stm32"]))
@click.option("--port", required=True)
def bench(target, port):
    """Run benchmark and parse output from target."""
    from mcuflow_edge.cli.bench import run_bench
    run_bench(target, port)


if __name__ == "__main__":
    cli()
