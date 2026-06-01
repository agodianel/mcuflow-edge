from pathlib import Path

import numpy as np
import pytest

from mcuflow_edge.capture.serial_reader import parse_sample_line
from mcuflow_edge.capture.session import (
    AXES,
    CaptureSample,
    CaptureSession,
    write_session,
)
from mcuflow_edge.dataset.builder import build_dataset
from mcuflow_edge.dataset.validators import ValidationError, assert_valid_session, validate_session


def make_session(session_id: str, label: str, n_samples: int = 10) -> CaptureSession:
    samples = [
        CaptureSample(
            t_ms=i * 10,
            values={a: float(i) for a in AXES},
            label=label,
        )
        for i in range(n_samples)
    ]
    return CaptureSession(
        session_id=session_id,
        target="esp32",
        board="esp32-s3-devkit",
        sensor="imu",
        sample_rate_hz=100,
        label=label,
        samples=samples,
    )


class TestValidators:
    def test_valid_session(self):
        session = make_session("test-1", "idle", 5)
        errors = validate_session(session)
        assert errors == []

    def test_missing_session_id(self):
        session = make_session("", "idle", 1)
        errors = validate_session(session)
        assert any("session_id" in e for e in errors)

    def test_invalid_target(self):
        session = make_session("t1", "idle", 1)
        session.target = "nrf52"
        errors = validate_session(session)
        assert any("target" in e for e in errors)

    def test_empty_samples(self):
        session = make_session("t1", "idle", 0)
        errors = validate_session(session)
        assert any("no samples" in e for e in errors)

    def test_missing_axis_in_sample(self):
        session = make_session("t1", "idle", 1)
        session.samples[0].values.pop("ax")
        errors = validate_session(session)
        assert any("ax" in e for e in errors)

    def test_assert_valid_session_raises(self):
        session = make_session("", "", 0)
        with pytest.raises(ValidationError):
            assert_valid_session(session)


class TestSerialReader:
    def test_parse_valid_line(self):
        line = "SMP 0,0.02,-0.01,0.98,0.1,0.0,-0.2"
        sample = parse_sample_line(line)
        assert sample is not None
        assert sample.t_ms == 0
        assert sample.values["ax"] == 0.02
        assert sample.values["gz"] == -0.2

    def test_parse_invalid_prefix(self):
        assert parse_sample_line("BAD 0,0.1,0.2") is None

    def test_parse_empty(self):
        assert parse_sample_line("") is None

    def test_parse_malformed_csv(self):
        assert parse_sample_line("SMP not,numbers") is None

    def test_parse_partial_axes(self):
        line = "SMP 0,0.1,0.2"
        sample = parse_sample_line(line)
        assert sample is None  # not enough parts


class TestDatasetBuilder:
    def test_build_dataset(self, tmp_path: Path):
        sessions_dir = tmp_path / "sessions"
        sessions_dir.mkdir()

        for label in ("idle", "shake"):
            for i in range(2):
                session = make_session(f"{label}-{i}", label, 130)
                write_session(session, sessions_dir)

        output_path = tmp_path / "out" / "dataset.npz"
        summary = build_dataset(sessions_dir, output_path, window_size=64)

        assert output_path.exists()
        assert (output_path.with_suffix(".summary.json")).exists()
        assert (output_path.with_name("labels.json")).exists()

        data = np.load(output_path)
        assert "X" in data
        assert "y" in data
        assert "labels" in data
        assert data["X"].shape[1] == 64
        assert data["X"].shape[2] == len(AXES)

        assert summary["total_windows"] > 0
        assert "idle" in summary["labels"]
        assert "shake" in summary["labels"]

    def test_build_no_files(self, tmp_path: Path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        with pytest.raises(FileNotFoundError):
            build_dataset(empty_dir, tmp_path / "out.npz")

    def test_build_too_few_samples(self, tmp_path: Path):
        sessions_dir = tmp_path / "sessions"
        sessions_dir.mkdir()
        session = make_session("too-short", "idle", 10)
        write_session(session, sessions_dir)
        with pytest.raises(ValueError, match="No windows"):
            build_dataset(sessions_dir, tmp_path / "out.npz", window_size=64)
