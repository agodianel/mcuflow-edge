from mcuflow_edge.capture.protocol import SAMPLE_LINE_PREFIX
from mcuflow_edge.capture.session import AXES, CaptureSample


def parse_sample_line(line: str) -> CaptureSample | None:
    line = line.strip()
    if not line.startswith(SAMPLE_LINE_PREFIX):
        return None
    payload = line.removeprefix(SAMPLE_LINE_PREFIX).strip()
    parts = [p.strip() for p in payload.split(",")]
    if len(parts) < 1 + len(AXES):
        return None
    try:
        t_ms = int(parts[0])
        values = {}
        for i, axis in enumerate(AXES):
            values[axis] = float(parts[1 + i])
    except (ValueError, IndexError):
        return None
    return CaptureSample(t_ms=t_ms, values=values, label="")
