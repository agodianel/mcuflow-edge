#include <stdio.h>
#include "capture_protocol.h"
#include "inference_runner.h"

#define NUM_RUNS 100

void run_benchmark_mode(void) {
    printf("Benchmark mode started\n");
    float input[128 * 6];
    float output[5];
    float total_ms = 0;
    float total_p95 = 0;
    float latencies[NUM_RUNS];

    for (int i = 0; i < NUM_RUNS; i++) {
        uint32_t start = get_tick_ms();
        run_tflm_inference(input, output);
        uint32_t end = get_tick_ms();
        latencies[i] = (float)(end - start);
        total_ms += latencies[i];
    }

    float avg = total_ms / NUM_RUNS;
    for (int i = 0; i < NUM_RUNS; i++) {
        total_p95 += latencies[i];
    }

    printf("BNCH %.2f,%.2f,%d,%d\n",
           avg, avg, get_flash_size(), get_ram_usage());
}
