#ifndef CAPTURE_PROTOCOL_H
#define CAPTURE_PROTOCOL_H

#include <stdint.h>

void send_sample(uint32_t t_ms, float *values);

#endif
