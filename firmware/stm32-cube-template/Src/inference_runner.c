/* MCUflow-Edge STM32 — inference runner */
#include <stdio.h>
#include "capture_protocol.h"
#include "imu_capture.h"

void run_inference_mode(void) {
    printf("Inference mode started\n");
    float input[128 * 6];
    float output[5];
    while (1) {
        read_imu_window(input, 128);
        run_ai_inference(input, output);
        int top = 0;
        for (int i = 1; i < 5; i++) {
            if (output[i] > output[top]) top = i;
        }
        printf("INF %d\n", top);
        delay_ms(100);
    }
}
