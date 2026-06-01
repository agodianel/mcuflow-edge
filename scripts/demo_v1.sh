#!/usr/bin/env bash
# MCUflow-Edge V1 demo
set -euo pipefail

echo "=== MCUflow-Edge Demo ==="
echo ""

echo "1. Create example model"
MODEL="examples/imu-gesture/model/gesture.tflite"
if [ ! -f "$MODEL" ]; then
    uv run python3 scripts/create_example_model.py "$MODEL"
fi
echo ""

echo "2. Init workspace"
uv run mcue init imu-gesture

echo ""
echo "4. Create sample capture session"
mkdir -p sessions
python3 -c "
import json
for label in ['idle', 'shake', 'tilt_left', 'tilt_right', 'tap']:
    lines = []
    for i in range(130):
        rec = {'t_ms': i * 10, 'ax': 0.0, 'ay': 0.0, 'az': 1.0, 'gx': 0.0, 'gy': 0.0, 'gz': 0.0, 'label': label}
        lines.append(rec)
    with open(f'sessions/demo_{label}.jsonl', 'w') as f:
        for l in lines:
            f.write(json.dumps(l) + '\n')
    meta = {
        'session_id': f'demo_{label}',
        'target': 'esp32',
        'board': 'esp32-s3-devkit',
        'sensor': 'imu',
        'sample_rate_hz': 100,
        'label': label,
        'schema_version': 1,
    }
    with open(f'sessions/demo_{label}.meta.json', 'w') as f:
        json.dump(meta, f, indent=2)
"

echo ""
echo "3. Build dataset"
uv run mcue dataset build ./sessions --out ./artifacts/dataset.npz

echo ""
echo "4. Package for ESP32"
uv run mcue pack --target esp32 --model "$MODEL"

echo ""
echo "5. Package for STM32"
uv run mcue pack --target stm32 --model "$MODEL"

echo ""
echo "6. Deploy to ESP32 template"
uv run mcue deploy --target esp32

echo ""
echo "=== Demo complete ==="
