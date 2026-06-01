#include <stdio.h>
#include <string.h>
#include "sdkconfig.h"

void app_main(void) {
    printf("MCUflow-Edge ESP32 firmware v0.1.0\n");
    printf("Modes: capture, inference, benchmark\n");
    printf("Enter mode: ");
    char buf[64];
    if (fgets(buf, sizeof(buf), stdin)) {
        buf[strcspn(buf, "\n")] = 0;
        if (strcmp(buf, "capture") == 0) {
            run_capture_mode();
        } else if (strcmp(buf, "inference") == 0) {
            run_inference_mode();
        } else if (strcmp(buf, "benchmark") == 0) {
            run_benchmark_mode();
        } else {
            printf("Unknown mode: %s\n", buf);
        }
    }
}

void run_capture_mode(void);
void run_inference_mode(void);
void run_benchmark_mode(void);
