import csv
from pathlib import Path

from mcuflow_edge.capture.session import AXES, read_session


def export_csv(session_dir: Path, output_path: Path) -> None:
    jsonl_files = sorted(session_dir.glob("*.jsonl"))
    if not jsonl_files:
        raise FileNotFoundError(f"No .jsonl files found in {session_dir}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["t_ms", *AXES, "label", "session_id"]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for jf in jsonl_files:
            mf = jf.with_suffix(".meta.json")
            if not mf.exists():
                continue
            session = read_session(jf, mf)
            for s in session.samples:
                row = {"t_ms": s.t_ms, "label": s.label, "session_id": session.session_id}
                for axis in AXES:
                    row[axis] = s.values.get(axis, 0.0)
                writer.writerow(row)
