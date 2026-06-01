#ifndef IMU_CAPTURE_H
#define IMU_CAPTURE_H

#include <stdint.h>

void read_imu(float *samples);
void delay_ms(uint32_t ms);

#endif
