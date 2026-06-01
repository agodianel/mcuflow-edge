# MCUflow-Edge Integration Point

This directory is where `mcue deploy --target stm32` places packaged model artifacts.

After running `mcue pack` and `mcue deploy`, you'll find:

- `../X-CUBE-AI/model.tflite` — The packaged model

## Next Steps

1. Open the STM32CubeIDE project
2. Run STM32Cube.AI (X-CUBE-AI) to regenerate integration files from the model
3. Build and flash the project via ST-Link
