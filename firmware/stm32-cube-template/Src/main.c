/**
 * MCUflow-Edge STM32 Template — Main Application
 *
 * This is a skeleton main.c for the STM32 firmware template.
 * It provides mode selection between capture, inference, and benchmark modes.
 *
 * Replace the TODO stubs with actual HAL/BSP initialization for your board.
 */

#include "main.h"

/* Mode selection: set via compile-time define or runtime switch */
typedef enum {
    MODE_CAPTURE,
    MODE_INFERENCE,
    MODE_BENCHMARK,
} app_mode_t;

static app_mode_t current_mode = MODE_INFERENCE;

int main(void)
{
    /* TODO: HAL_Init() and SystemClock_Config() */
    /* TODO: Initialize UART for serial communication */
    /* TODO: Initialize IMU sensor (I2C/SPI) */

    switch (current_mode) {
        case MODE_CAPTURE:
            /* TODO: Run IMU capture loop, emit SMP lines over serial */
            break;
        case MODE_INFERENCE:
            /* TODO: Run inference loop using STM32Cube.AI generated code */
            break;
        case MODE_BENCHMARK:
            /* TODO: Run benchmark, emit BNCH line over serial */
            break;
    }

    while (1) {
        /* Main loop */
    }
}
