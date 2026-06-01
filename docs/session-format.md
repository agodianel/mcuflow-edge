# Session Format

Capture sessions use **JSON Lines** (`.jsonl`) for sample data with a separate `.meta.json` metadata file. This format is designed to be simple, inspectable, and robust — you can `cat` or `head` a session file and immediately understand its contents.

## File Naming

```
sessions/<timestamp>_<target>_<label>.jsonl
sessions/<timestamp>_<target>_<label>.meta.json
```

Example:
```
sessions/2026-06-01T21-00-00_esp32_shake.jsonl
sessions/2026-06-01T21-00-00_esp32_shake.meta.json
```

## Sample Record (JSONL)

Each line in the `.jsonl` file is one sensor sample:

```json
{"t_ms": 0, "ax": 0.02, "ay": -0.01, "az": 0.98, "gx": 0.1, "gy": 0.0, "gz": -0.2, "label": "idle"}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `t_ms` | `int` | Timestamp in milliseconds (relative to session start) |
| `ax` | `float` | Accelerometer X axis (g) |
| `ay` | `float` | Accelerometer Y axis (g) |
| `az` | `float` | Accelerometer Z axis (g) |
| `gx` | `float` | Gyroscope X axis (°/s) |
| `gy` | `float` | Gyroscope Y axis (°/s) |
| `gz` | `float` | Gyroscope Z axis (°/s) |
| `label` | `string` | Class label for this sample |

## Metadata File

```json
{
  "session_id": "2026-06-01T21-00-00Z_esp32_idle",
  "target": "esp32",
  "board": "esp32-s3-devkit",
  "sensor": "imu",
  "sample_rate_hz": 100,
  "label": "idle",
  "schema_version": 1
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | `string` | Unique session identifier (timestamp + target + label) |
| `target` | `string` | Target platform: `esp32` or `stm32` |
| `board` | `string` | Specific board identifier |
| `sensor` | `string` | Sensor type (always `imu` in V1) |
| `sample_rate_hz` | `int` | Expected sampling rate in Hz |
| `label` | `string` | Default label for all samples in this session |
| `schema_version` | `int` | Schema version for forward compatibility |

## Serial Protocol

The firmware sends sample data over serial using the `SMP` prefix:

```
SMP <t_ms>,<ax>,<ay>,<az>,<gx>,<gy>,<gz>
```

Example: `SMP 0,0.02,-0.01,0.98,0.1,0.0,-0.2`

The host CLI parses these lines and assigns the label from the `--label` argument.

## Validation Rules

Sessions are validated before dataset building:

- `session_id` must not be empty
- `target` must be `esp32` or `stm32`
- All six IMU axes (`ax`, `ay`, `az`, `gx`, `gy`, `gz`) must be present in every sample
- Every sample must have a non-empty label
- Sessions with no samples are rejected

## Schema Versioning

The `schema_version` field enables forward-compatible changes. Rules:

- **Additive fields** (new optional fields) do not bump the version
- **Breaking changes** (renamed fields, removed fields, type changes) require a version bump
- Parsers should reject sessions with unknown schema versions rather than silently misinterpreting data
