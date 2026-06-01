from datetime import UTC, datetime
from pathlib import Path

from mcuflow_edge.utils.jsonio import write_json


def write_bench_report(
    target: str,
    board: str,
    model_name: str,
    bench_data: dict,
    report_dir: Path,
    tool_version: str = "0.1.0",
) -> Path:
    report = {
        "target": target,
        "board": board,
        "model_name": model_name,
        "latency_ms_avg": bench_data.get("latency_ms_avg"),
        "latency_ms_p95": bench_data.get("latency_ms_p95"),
        "input_shape": bench_data.get("input_shape", []),
        "flash_bytes": bench_data.get("flash_bytes"),
        "ram_bytes": bench_data.get("ram_bytes"),
        "tool_version": tool_version,
        "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    report_path = report_dir / f"bench_{target}_{timestamp}.json"
    write_json(report_path, report)
    return report_path
