from pathlib import Path

from mcuflow_edge.capture.session import (
    AXES,
    CaptureSample,
    CaptureSession,
    generate_session_id,
    read_session,
    record_from_sample,
    sample_from_record,
    write_session,
)


def test_capture_session_to_metadata():
    session = CaptureSession(
        session_id="test-session",
        target="esp32",
        board="esp32-s3-devkit",
        sensor="imu",
        sample_rate_hz=100,
        label="idle",
        samples=[],
    )
    meta = session.to_metadata()
    assert meta["session_id"] == "test-session"
    assert meta["schema_version"] == 1
    assert meta["label"] == "idle"


def test_capture_sample_dataclass():
    sample = CaptureSample(t_ms=0, values={"ax": 0.0, "ay": 0.0}, label="idle")
    assert sample.t_ms == 0
    assert sample.label == "idle"


def test_record_roundtrip():
    sample = CaptureSample(
        t_ms=100,
        values={"ax": 0.1, "ay": -0.2, "az": 0.98, "gx": 0.0, "gy": 0.0, "gz": 0.0},
        label="shake",
    )
    rec = record_from_sample(sample)
    restored = sample_from_record(rec)
    assert restored.t_ms == sample.t_ms
    assert restored.label == sample.label
    assert restored.values == sample.values


def test_write_and_read_session(tmp_path: Path):
    samples = [
        CaptureSample(t_ms=i * 10, values={a: float(i) for a in AXES}, label="idle")
        for i in range(3)
    ]
    session = CaptureSession(
        session_id="test-write-read",
        target="esp32",
        board="esp32-s3-devkit",
        sensor="imu",
        sample_rate_hz=100,
        label="idle",
        samples=samples,
    )
    jsonl_path, meta_path = write_session(session, tmp_path)

    assert jsonl_path.exists()
    assert meta_path.exists()

    restored = read_session(jsonl_path, meta_path)
    assert restored.session_id == "test-write-read"
    assert len(restored.samples) == 3
    assert restored.samples[0].t_ms == 0


def test_generate_session_id():
    sid = generate_session_id("esp32", "shake")
    assert "esp32" in sid
    assert "shake" in sid


def test_sample_from_record_missing_axes():
    rec = {"t_ms": 0, "ax": 0.1, "gy": 0.2, "label": "test"}
    sample = sample_from_record(rec)
    assert "ax" in sample.values
    assert "gy" in sample.values
    assert "az" not in sample.values
