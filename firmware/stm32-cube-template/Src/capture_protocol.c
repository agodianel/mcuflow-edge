/* MCUflow-Edge STM32 — serial capture protocol */
#include <stdio.h>
#include <stdint.h>

void send_sample(uint32_t t_ms, float *values) {
    printf("SMP %u,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n",
           t_ms, values[0], values[1], values[2],
           values[3], values[4], values[5]);
}

uint32_t get_tick_ms(void) { return 0; }
int get_flash_size(void) { return 262144; }
int get_ram_usage(void) { return 65536; }
void read_imu_window(float *buf, int len) {
    for (int i = 0; i < len; i++) buf[i] = 0.0f;
}
void run_ai_inference(float *input, float *output) {
    (void)input;
    for (int i = 0; i < 5; i++) output[i] = 0.0f;
}
