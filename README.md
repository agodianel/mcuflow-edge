# MCUflow-Edge

One workflow for edge AI on ESP32 and STM32.

MCUflow-Edge helps embedded developers capture sensor data, build reproducible datasets, package tiny models, deploy them to real boards, and benchmark the result with one consistent CLI.

Instead of replacing vendor runtimes, MCUflow-Edge builds on proven target-native paths:
- **ESP32** via ESP-IDF + TensorFlow Lite Micro
- **STM32** via STM32Cube.AI

## Quick start

```bash
uv add mcuflow-edge
# or from source:
# uv sync && uv run mcue --help
```

## V1 workflow

```bash
# Initialize a workspace
mcue init imu-gesture

# Capture labeled IMU data from boards
mcue capture --target esp32 --port /dev/ttyUSB0 --label shake
mcue capture --target stm32 --port /dev/tty.usbmodemXXXX --label idle

# Build a dataset from sessions
mcue dataset build ./sessions --out ./artifacts/dataset.npz

# Package a model for a target
mcue pack --target esp32 --model ./models/gesture.tflite
mcue pack --target stm32 --model ./models/gesture.tflite

# Deploy into firmware templates
mcue deploy --target esp32 --port /dev/ttyUSB0
mcue deploy --target stm32 --project ./firmware/stm32-cube-template

# Benchmark on real hardware
mcue bench --target esp32 --port /dev/ttyUSB0
mcue bench --target stm32 --port /dev/tty.usbmodemXXXX
```

## Repository structure

```
mcuflow-edge/
├── mcuflow_edge/       # Python CLI package
│   ├── cli/            # Click commands
│   ├── capture/        # Serial capture and session format
│   ├── dataset/        # Dataset builder and validators
│   ├── pack/           # Model packaging and manifest
│   ├── deploy/         # Deployment orchestration
│   ├── bench/          # Benchmark parser and reports
│   └── targets/        # ESP32 and STM32 adapters
├── firmware/           # Board firmware templates
│   ├── esp32-idf-template/
│   └── stm32-cube-template/
├── examples/           # Example projects
├── tests/              # Test suite
└── docs/               # Documentation
```

## Documentation

- [Architecture](docs/architecture.md)
- [Supported boards](docs/supported-boards.md)
- [Session format](docs/session-format.md)
- [Benchmark format](docs/benchmark-format.md)

## License

MIT
