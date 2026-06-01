#ifndef INFERENCE_RUNNER_H
#define INFERENCE_RUNNER_H

void run_inference_mode(void);
void read_imu_window(float *buf, int len);
void run_tflm_inference(float *input, float *output);

#endif
