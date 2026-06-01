SERIAL_BAUD = 115200
SAMPLE_LINE_PREFIX = "SMP"  # lines starting with SMP contain sensor data

# Expected CSV format from firmware: SMP <t_ms>,<ax>,<ay>,<az>,<gx>,<gy>,<gz>
# Example: SMP 0,0.02,-0.01,0.98,0.1,0.0,-0.2
