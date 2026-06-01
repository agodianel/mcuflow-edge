#ifndef BENCHMARK_H
#define BENCHMARK_H

void run_benchmark_mode(void);
uint32_t get_tick_ms(void);
int get_flash_size(void);
int get_ram_usage(void);
void run_ai_inference(float *input, float *output);

#endif
