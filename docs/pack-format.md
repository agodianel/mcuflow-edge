# Pack Format

The `mcue pack` command packages a trained `.tflite` model into a self-describing artifact folder for a specific target.

## Folder Structure

```
artifacts/pack/
├── esp32/
│   ├── model.tflite          # Copy of the packaged model
│   ├── pack_manifest.json    # Pack metadata and model hash
│   ├── model_info.json       # Model inspection results
│   └── generated/            # Target-specific generated files
└── stm32/
    ├── model.tflite
    ├── pack_manifest.json
    ├── model_info.json
    └── generated/
```

## `pack_manifest.json`

The manifest provides all metadata needed for deployment and traceability.

```json
{
  "schema_version": 1,
  "target": "esp32",
  "model_path": "model.tflite",
  "model_sha256": "a1b2c3d4e5f6...",
  "input_shape": [1, 128, 6],
  "output_labels": ["idle", "shake", "tilt_left", "tilt_right", "tap"],
  "quantized": true,
  "created_at": "2026-06-01T21:00:00Z",
  "tool_version": "0.1.0"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | `int` | Manifest schema version |
| `target` | `string` | Target platform (`esp32` or `stm32`) |
| `model_path` | `string` | Relative path to the model file within the pack directory |
| `model_sha256` | `string` | SHA-256 hash of the model file for integrity verification |
| `input_shape` | `int[]` | Expected input tensor shape |
| `output_labels` | `string[]` | Ordered list of output class labels |
| `quantized` | `bool` | Whether the model uses quantized weights |
| `created_at` | `string` | ISO 8601 UTC timestamp of pack creation |
| `tool_version` | `string` | MCUflow-Edge version that created this package |

## `model_info.json`

Results from inspecting the `.tflite` model file:

```json
{
  "size_bytes": 45200,
  "quantized": false,
  "input_shape": [1, 128, 6],
  "input_dtype": "float32"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `size_bytes` | `int` | Model file size in bytes |
| `quantized` | `bool` | Whether quantization parameters were detected |
| `input_shape` | `int[]` | Input tensor shape from the model |
| `input_dtype` | `string` | Input tensor data type (`float32`, `int8`, `uint8`, etc.) |

## Integrity Verification

The `model_sha256` field allows downstream tools and deploy commands to verify that the model has not been modified after packaging. The SHA-256 hash is computed from the original model file at pack time.
