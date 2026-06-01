import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from mcuflow_edge.capture.session import AXES, read_session
from mcuflow_edge.dataset.validators import assert_valid_session


def build_dataset(
    session_dir: Path,
    output_path: Path,
    window_size: int = 128,
) -> dict:
    jsonl_files = sorted(session_dir.glob("*.jsonl"))
    if not jsonl_files:
        raise FileNotFoundError(f"No .jsonl files found in {session_dir}")

    sessions = []
    for jf in jsonl_files:
        mf = jf.with_suffix(".meta.json")
        if not mf.exists():
            continue
        session = read_session(jf, mf)
        assert_valid_session(session)
        sessions.append(session)

    all_X: list[np.ndarray] = []
    all_y: list[str] = []
    label_counts: Counter = Counter()

    for session in sessions:
        samples = session.samples
        label = session.label
        if len(samples) < window_size:
            continue
        for start in range(0, len(samples) - window_size + 1, window_size):
            window = samples[start : start + window_size]
            X_row = np.array([[s.values[a] for a in AXES] for s in window], dtype=np.float32)
            all_X.append(X_row)
            all_y.append(label)
            label_counts[label] += 1

    if not all_X:
        raise ValueError("No windows could be formed from the sessions")

    X = np.stack(all_X, axis=0)
    labels_unique = sorted(set(all_y))
    label_to_int = {lbl: i for i, lbl in enumerate(labels_unique)}
    y = np.array([label_to_int[lbl] for lbl in all_y], dtype=np.int32)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(output_path, X=X, y=y, labels=labels_unique)

    summary = {
        "labels": {lbl: label_counts[lbl] for lbl in labels_unique},
        "features": list(AXES),
        "window_size": window_size,
        "total_windows": len(all_X),
        "source_sessions": [s.session_id for s in sessions],
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    summary_path = output_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    labels_path = output_path.with_name("labels.json")
    labels_path.write_text(json.dumps(labels_unique, indent=2) + "\n")

    return summary
