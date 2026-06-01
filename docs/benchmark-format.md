# Benchmark Report Format

Each `mcue bench` run produces a JSON report in `reports/benchmarks/`. The report schema is the same for all targets, even though field collection may differ internally.

## Report File

```
reports/benchmarks/bench_<target>_<timestamp>.json
```

Example: `reports/benchmarks/bench_esp32_20260601T210000.json`

## Schema

```json
{
  "target": "esp32",
  "board": "esp32-s3-devkit",
  "model_name": "gesture.tflite",
  "latency_ms_avg": 12.4,
  "latency_ms_p95": 14.2,
  "input_shape": [1, 128, 6],
  "flash_bytes": 182304,
  "ram_bytes": 48128,
  "tool_version": "0.1.0",
  "timestamp": "2026-06-01T21:00:00Z"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `target` | `string` | Target platform (`esp32` or `stm32`) |
| `board` | `string` | Specific board identifier |
| `model_name` | `string` | Name of the benchmarked model file |
| `latency_ms_avg` | `float` | Average inference latency in milliseconds |
| `latency_ms_p95` | `float` | 95th percentile inference latency in milliseconds |
| `input_shape` | `int[]` | Model input tensor shape (e.g. `[1, 128, 6]`) |
| `flash_bytes` | `int` | Flash memory usage in bytes |
| `ram_bytes` | `int` | RAM usage in bytes |
| `tool_version` | `string` | MCUflow-Edge version that generated this report |
| `timestamp` | `string` | ISO 8601 UTC timestamp of the benchmark run |

## Serial Protocol

The firmware emits benchmark results using the `BNCH` prefix:

```
BNCH <avg_latency_ms>,<p95_latency_ms>,<flash_bytes>,<ram_bytes>
```

Example: `BNCH 12.4,14.2,182304,48128`

The host CLI reads serial output, parses the `BNCH` line, and combines it with target metadata to produce the full report.

## Example Reports

### ESP32

```json
{
  "target": "esp32",
  "board": "esp32-s3-devkit",
  "model_name": "gesture.tflite",
  "latency_ms_avg": 12.4,
  "latency_ms_p95": 14.2,
  "input_shape": [1, 128, 6],
  "flash_bytes": 182304,
  "ram_bytes": 48128,
  "tool_version": "0.1.0",
  "timestamp": "2026-06-01T21:00:00Z"
}
```

### STM32

```json
{
  "target": "stm32",
  "board": "stwinbox",
  "model_name": "gesture.tflite",
  "latency_ms_avg": 8.1,
  "latency_ms_p95": 9.3,
  "input_shape": [1, 128, 6],
  "flash_bytes": 156200,
  "ram_bytes": 42800,
  "tool_version": "0.1.0",
  "timestamp": "2026-06-01T21:05:00Z"
}
```
