/* MCUflow-Edge STM32 — IMU capture adapter */
#include <stdio.h>

void read_imu(float *samples) {
    for (int i = 0; i < 6; i++) samples[i] = 0.0f;
}

void delay_ms(uint32_t ms) {
    (void)ms;
}
