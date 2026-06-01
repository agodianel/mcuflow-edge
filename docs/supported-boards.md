# Supported Boards (V1)

MCUflow-Edge V1 supports a **small, explicit hardware matrix**. The project does not claim broad support for all boards in either family.

## Hardware Matrix

| Family | Board | MCU | IMU Access | Runtime Path | Status |
|--------|-------|-----|-----------|-------------|--------|
| ESP32 | ESP32-S3 DevKit | ESP32-S3 | External I2C/SPI IMU (e.g. MPU6050, ICM-42670) | ESP-IDF + esp-tflite-micro | ✅ First-class |
| STM32 | STWIN / STWIN.box | STM32L4R9 | Onboard ISM330DHCX | STM32Cube.AI | ✅ First-class |
| STM32 | Nucleo + IMU shield | STM32L4/F4 series | External IMU via I2C/SPI | STM32Cube.AI | 🔧 Supported |

## ESP32 Details

- **Environment**: ESP-IDF v5.x
- **Inference runtime**: TensorFlow Lite Micro via [esp-tflite-micro](https://github.com/espressif/esp-tflite-micro)
- **Firmware template**: `firmware/esp32-idf-template/`
- **Build/flash**: `idf.py set-target esp32s3 && idf.py build && idf.py -p PORT flash monitor`

## STM32 Details

- **Environment**: STM32CubeIDE
- **Inference runtime**: [STM32Cube.AI](https://www.st.com/en/embedded-software/x-cube-ai.html) (X-CUBE-AI)
- **Firmware template**: `firmware/stm32-cube-template/`
- **Build/flash**: Use STM32CubeIDE to build and flash via ST-Link

## Adding a New Board

To add a new board within a supported family:

1. Create a new `template_vars.py` in the target's directory with board-specific configuration
2. Add the board to the target adapter's `validate_environment()` if it needs specific checks
3. Create a firmware template directory if the board requires different project structure
4. Update this document with the new board's details
5. Add tests for the new configuration

> **Note**: V1 does not support adding entirely new MCU families. The architecture supports it, but new families require a new target adapter implementation.
