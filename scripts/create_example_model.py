"""Generate a minimal valid .tflite model for the IMU gesture example."""

import flatbuffers
import tflite


def int32_vec(builder, items):
    builder.StartVector(4, len(items), 4)
    for v in reversed(items):
        builder.PrependInt32(v)
    return builder.EndVector()


def uoffset_vec(builder, items):
    builder.StartVector(4, len(items), 4)
    for v in reversed(items):
        builder.PrependUOffsetTRelative(v)
    return builder.EndVector()


builder = flatbuffers.Builder(2048)

input_name = builder.CreateString("input_0")
output_name = builder.CreateString("output_0")

input_shape = int32_vec(builder, [1, 128, 6])
output_shape = int32_vec(builder, [1, 5])

tflite.TensorStart(builder)
tflite.TensorAddShape(builder, input_shape)
tflite.TensorAddType(builder, tflite.TensorType.FLOAT32)
tflite.TensorAddName(builder, input_name)
input_tensor = tflite.TensorEnd(builder)

tflite.TensorStart(builder)
tflite.TensorAddShape(builder, output_shape)
tflite.TensorAddType(builder, tflite.TensorType.FLOAT32)
tflite.TensorAddName(builder, output_name)
output_tensor = tflite.TensorEnd(builder)

tensors_vec = uoffset_vec(builder, [input_tensor, output_tensor])
inputs_vec = int32_vec(builder, [0])
outputs_vec = int32_vec(builder, [1])

tflite.SubGraphStart(builder)
tflite.SubGraphAddInputs(builder, inputs_vec)
tflite.SubGraphAddOutputs(builder, outputs_vec)
tflite.SubGraphAddTensors(builder, tensors_vec)
subgraph = tflite.SubGraphEnd(builder)

subgraphs_vec = uoffset_vec(builder, [subgraph])
desc_str = builder.CreateString("MCUflow-Edge IMU gesture model")

tflite.ModelStart(builder)
tflite.ModelAddSubgraphs(builder, subgraphs_vec)
tflite.ModelAddDescription(builder, desc_str)
model = tflite.ModelEnd(builder)

builder.Finish(model)
tflite_model = builder.Output()

import sys
path = sys.argv[1]
with open(path, "wb") as f:
    f.write(tflite_model)

print(f"Created model: {path} ({len(tflite_model)} bytes)")
