import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class CaptureSample:
    t_ms: int
    values: dict[str, float]
    label: str


AXES = ["ax", "ay", "az", "gx", "gy", "gz"]


def sample_from_record(record: dict) -> CaptureSample:
    values = {k: record[k] for k in AXES if k in record}
    return CaptureSample(
        t_ms=record["t_ms"],
        values=values,
        label=record.get("label", ""),
    )


def record_from_sample(sample: CaptureSample) -> dict:
    rec: dict = {"t_ms": sample.t_ms, "label": sample.label}
    rec.update(sample.values)
    return rec


@dataclass
class CaptureSession:
    session_id: str
    target: str
    board: str
    sensor: str
    sample_rate_hz: int
    label: str
    samples: list[CaptureSample]

    def to_metadata(self) -> dict:
        return {
            "session_id": self.session_id,
            "target": self.target,
            "board": self.board,
            "sensor": self.sensor,
            "sample_rate_hz": self.sample_rate_hz,
            "label": self.label,
            "schema_version": 1,
        }


def write_session(session: CaptureSession, path: Path) -> tuple[Path, Path]:
    jsonl_path = path / f"{session.session_id}.jsonl"
    meta_path = path / f"{session.session_id}.meta.json"

    lines = [json.dumps(record_from_sample(s)) for s in session.samples]
    jsonl_path.write_text("\n".join(lines) + "\n")
    meta_path.write_text(json.dumps(session.to_metadata(), indent=2) + "\n")

    return jsonl_path, meta_path


def read_session(jsonl_path: Path, meta_path: Path) -> CaptureSession:
    meta = json.loads(meta_path.read_text())
    samples: list[CaptureSample] = []
    for line in jsonl_path.read_text().strip().splitlines():
        line = line.strip()
        if line:
            samples.append(sample_from_record(json.loads(line)))
    session_label = meta.get("label", "")
    for s in samples:
        if not s.label:
            s.label = session_label

    return CaptureSession(
        session_id=meta["session_id"],
        target=meta["target"],
        board=meta.get("board", ""),
        sensor=meta.get("sensor", "imu"),
        sample_rate_hz=meta.get("sample_rate_hz", 100),
        label=session_label,
        samples=samples,
    )


def generate_session_id(target: str, label: str) -> str:
    ts = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%S")
    return f"{ts}_{target}_{label}"
