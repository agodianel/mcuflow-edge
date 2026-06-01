# IMU Gesture Classification Example

This example demonstrates the full MCUflow-Edge workflow: capture labeled IMU data from ESP32 or STM32 boards, build a dataset, package a trained model, deploy firmware artifacts, and benchmark.

## Gesture classes

| Label | Description |
|---|---|
| `idle` | No motion, device stationary |
| `shake` | Rapid back-and-forth motion |
| `tilt_left` | Device tilted to the left |
| `tilt_right` | Device tilted to the right |
| `tap` | Single tap on the device |

## Workflow

### 1. Initialize

```bash
mcue init imu-gesture
```

### 2. Capture data

For each gesture class, connect the board and run capture:

```bash
mcue capture --target esp32 --port /dev/ttyUSB0 --label idle --duration 30
mcue capture --target esp32 --port /dev/ttyUSB0 --label shake --duration 30
mcue capture --target esp32 --port /dev/ttyUSB0 --label tilt_left --duration 30
mcue capture --target esp32 --port /dev/ttyUSB0 --label tilt_right --duration 30
mcue capture --target esp32 --port /dev/ttyUSB0 --label tap --duration 30
```

Sessions are saved as JSONL files in `./sessions/`.

### 3. Build dataset

```bash
mcue dataset build ./sessions --out ./artifacts/dataset.npz
```

### 4. Train a model

Train a TinyML model (e.g., using TensorFlow) and export as `.tflite`. Place the model in `./models/gesture.tflite`.

### 5. Package for target

```bash
mcue pack --target esp32 --model ./models/gesture.tflite
mcue pack --target stm32 --model ./models/gesture.tflite
```

### 6. Deploy

```bash
mcue deploy --target esp32 --port /dev/ttyUSB0
mcue deploy --target stm32 --project ./firmware/stm32-cube-template
```

### 7. Benchmark

```bash
mcue bench --target esp32 --port /dev/ttyUSB0
```

## Labels

See [labels.yaml](labels.yaml) for the class definitions.
