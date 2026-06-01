/* MCUflow-Edge STM32 — benchmark runner */
#include <stdio.h>
#include "capture_protocol.h"

#define NUM_RUNS 100

void run_benchmark_mode(void) {
    printf("Benchmark mode started\n");
    float input[128 * 6];
    float output[5];
    float total_ms = 0;

    for (int i = 0; i < NUM_RUNS; i++) {
        uint32_t start = get_tick_ms();
        run_ai_inference(input, output);
        uint32_t end = get_tick_ms();
        total_ms += (float)(end - start);
    }

    float avg = total_ms / NUM_RUNS;
    printf("BNCH %.2f,%.2f,%d,%d\n",
           avg, avg, get_flash_size(), get_ram_usage());
}
