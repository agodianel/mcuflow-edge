"""Tests for the `mcue init` command."""

from pathlib import Path

import yaml


def test_init_creates_directories(tmp_path: Path, monkeypatch):
    """init should create sessions/, artifacts/, reports/, models/ directories."""
    monkeypatch.chdir(tmp_path)

    # Create a minimal examples dir so the labels copy works
    example_dir = tmp_path / "examples" / "imu-gesture"
    example_dir.mkdir(parents=True)
    (example_dir / "labels.yaml").write_text("labels:\\n  - idle\\n  - shake\\n")

    from mcuflow_edge.cli.init import run_init

    run_init("imu-gesture")

    for dirname in ["sessions", "artifacts", "reports", "models"]:
        assert (tmp_path / dirname).is_dir(), f"{dirname}/ was not created"


def test_init_creates_config(tmp_path: Path, monkeypatch):
    """init should generate an mcuflow.yaml project config."""
    monkeypatch.chdir(tmp_path)

    from mcuflow_edge.cli.init import run_init

    run_init("imu-gesture")

    config_path = tmp_path / "mcuflow.yaml"
    assert config_path.exists(), "mcuflow.yaml was not created"

    config = yaml.safe_load(config_path.read_text())
    assert config["project"]["name"] == "imu-gesture"
    assert config["project"]["example"] == "imu-gesture"
    assert "labels" in config
    assert "targets" in config
    assert "esp32" in config["targets"]
    assert "stm32" in config["targets"]


def test_init_creates_labels(tmp_path: Path, monkeypatch):
    """init should create a labels.yaml file."""
    monkeypatch.chdir(tmp_path)

    from mcuflow_edge.cli.init import run_init

    run_init("imu-gesture")

    labels_path = tmp_path / "labels.yaml"
    assert labels_path.exists(), "labels.yaml was not created"


def test_init_idempotent(tmp_path: Path, monkeypatch):
    """Running init twice should not crash or overwrite existing config."""
    monkeypatch.chdir(tmp_path)

    from mcuflow_edge.cli.init import run_init

    run_init("imu-gesture")

    # Modify config to prove it won't be overwritten
    config_path = tmp_path / "mcuflow.yaml"
    original_content = config_path.read_text()

    run_init("imu-gesture")

    assert config_path.read_text() == original_content, "mcuflow.yaml was overwritten"
