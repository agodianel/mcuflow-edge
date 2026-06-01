#include <stdio.h>

void send_sample(uint32_t t_ms, float *values) {
    printf("SMP %u,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n",
           t_ms, values[0], values[1], values[2],
           values[3], values[4], values[5]);
}

void read_imu(float *samples) {
    for (int i = 0; i < 6; i++) samples[i] = 0.0f;
}

uint32_t get_tick_ms(void) { return 0; }
int get_flash_size(void) { return 182304; }
int get_ram_usage(void) { return 48128; }
void delay_ms(uint32_t ms) { (void)ms; }
void read_imu_window(float *buf, int len) {
    for (int i = 0; i < len; i++) buf[i] = 0.0f;
}
void run_tflm_inference(float *input, float *output) {
    (void)input;
    for (int i = 0; i < 5; i++) output[i] = 0.0f;
}
