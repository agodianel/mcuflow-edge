#include <stdio.h>
#include "capture_protocol.h"

#define SAMPLE_RATE_HZ 100
#define AXES 6

void run_capture_mode(void) {
    printf("Capture mode started\n");
    uint32_t t_ms = 0;
    float samples[AXES];
    while (1) {
        read_imu(samples);
        send_sample(t_ms, samples);
        t_ms += 1000 / SAMPLE_RATE_HZ;
        delay_ms(1000 / SAMPLE_RATE_HZ);
    }
}
