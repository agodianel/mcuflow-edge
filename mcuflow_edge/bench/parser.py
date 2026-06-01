BENCH_LINE_PREFIX = "BNCH"

# Expected format from firmware:
# BNCH avg_latency_ms,p95_latency_ms,flash_bytes,ram_bytes
# Example: BNCH 12.4,14.2,182304,48128


def parse_bench_line(line: str) -> dict | None:
    line = line.strip()
    if not line.startswith(BENCH_LINE_PREFIX):
        return None
    payload = line.removeprefix(BENCH_LINE_PREFIX).strip()
    parts = [p.strip() for p in payload.split(",")]
    if len(parts) < 4:
        return None
    try:
        return {
            "latency_ms_avg": float(parts[0]),
            "latency_ms_p95": float(parts[1]),
            "flash_bytes": int(parts[2]),
            "ram_bytes": int(parts[3]),
        }
    except (ValueError, IndexError):
        return None


def parse_bench_output(lines: list[str]) -> dict:
    for line in lines:
        result = parse_bench_line(line)
        if result is not None:
            return result
    raise ValueError("No benchmark data found in output")
