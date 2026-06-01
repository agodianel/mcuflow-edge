# Architecture

MCUflow-Edge has three layers that work together to provide a unified workflow from sensor capture to benchmark reporting.

```mermaid
graph TB
    subgraph Host["Host Layer (Python CLI)"]
        CLI["mcue CLI"]
        CAP["capture/"]
        DS["dataset/"]
        PK["pack/"]
        DEP["deploy/"]
        BN["bench/"]
        TGT["targets/"]
    end

    subgraph Device["Device Layer (Firmware)"]
        ESP["ESP32 Template"]
        STM["STM32 Template"]
    end

    subgraph Backend["Backend Layer (Vendor Runtimes)"]
        TFLM["ESP-IDF + TFLM"]
        CUBE["STM32Cube.AI"]
    end

    CLI --> CAP
    CLI --> DS
    CLI --> PK
    CLI --> DEP
    CLI --> BN
    CLI --> TGT

    TGT --> ESP
    TGT --> STM

    ESP --> TFLM
    STM --> CUBE
```

## Layer Responsibilities

### Host Layer (Python)

The `mcue` CLI is the stable public interface. All user interaction happens here.

| Module | Responsibility |
|--------|---------------|
| `cli/` | Click command definitions and argument parsing |
| `capture/` | Serial protocol parsing, session I/O (JSONL + metadata) |
| `dataset/` | Session validation, windowed dataset building (NPZ/CSV) |
| `pack/` | Model inspection (.tflite), manifest generation, artifact packaging |
| `deploy/` | File copying into firmware templates, next-step instructions |
| `bench/` | Serial benchmark output parsing, JSON report generation |
| `targets/` | Target adapter registry and per-target implementations |
| `utils/` | Shared JSON I/O and logging |

### Device Layer (Firmware)

Target-specific firmware templates that run on real hardware:

- **ESP32**: ESP-IDF project with `app_main.c`, `imu_capture.c`, `inference_runner.c`, `benchmark.c`, and `capture_protocol.c`
- **STM32**: STM32Cube project skeleton with integration points for STM32Cube.AI

### Backend Layer (Vendor Runtimes)

MCUflow-Edge does not replace these runtimes — it wraps them:

- **ESP32**: Espressif's [esp-tflite-micro](https://github.com/espressif/esp-tflite-micro) component for TensorFlow Lite Micro inference
- **STM32**: ST's [STM32Cube.AI](https://www.st.com/en/embedded-software/x-cube-ai.html) for model optimization and code generation

## Data Flow

```mermaid
graph LR
    A["Board + IMU"] -->|serial| B["mcue capture"]
    B -->|JSONL + meta| C["sessions/"]
    C --> D["mcue dataset build"]
    D -->|NPZ + summary| E["artifacts/dataset.npz"]
    E -->|"train externally"| F["models/gesture.tflite"]
    F --> G["mcue pack"]
    G -->|"manifest + model"| H["artifacts/pack/target/"]
    H --> I["mcue deploy"]
    I -->|"copy into"| J["firmware/template/"]
    J -->|"build + flash"| K["Board"]
    K -->|serial| L["mcue bench"]
    L -->|JSON| M["reports/benchmarks/"]
```

## Target Adapter Pattern

All target-specific logic is encapsulated in adapter classes that implement `TargetAdapter`:

```python
class TargetAdapter(ABC):
    name: str
    def validate_environment(self) -> None: ...
    def pack_model(self, model_path: Path, output_dir: Path) -> None: ...
    def deploy(self, package_dir: Path, **kwargs) -> None: ...
    def benchmark(self, **kwargs) -> dict: ...
```

The central registry in `mcuflow_edge/targets/__init__.py` provides `get_adapter(name)` for CLI commands, so no command needs to know about specific target implementations.
