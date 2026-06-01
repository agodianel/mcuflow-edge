from pathlib import Path

import flatbuffers
import pytest
import tflite


def _make_vector(builder, items):
    builder.StartVector(4, len(items), 4)
    for v in reversed(items):
        builder.PrependInt32(v)
    return builder.EndVector()


def _uoffset_vec(builder, items):
    builder.StartVector(4, len(items), 4)
    for v in reversed(items):
        builder.PrependUOffsetTRelative(v)
    return builder.EndVector()


@pytest.fixture
def valid_tflite_model(tmp_path: Path) -> Path:
    builder = flatbuffers.Builder(2048)
    input_name = builder.CreateString("input_0")
    output_name = builder.CreateString("output_0")

    input_shape = _make_vector(builder, [1, 128, 6])
    output_shape = _make_vector(builder, [1, 5])

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

    tensors_vec = _uoffset_vec(builder, [input_tensor, output_tensor])
    inputs_vec = _make_vector(builder, [0])
    outputs_vec = _make_vector(builder, [1])

    tflite.SubGraphStart(builder)
    tflite.SubGraphAddInputs(builder, inputs_vec)
    tflite.SubGraphAddOutputs(builder, outputs_vec)
    tflite.SubGraphAddTensors(builder, tensors_vec)
    subgraph = tflite.SubGraphEnd(builder)

    subgraphs_vec = _uoffset_vec(builder, [subgraph])
    desc_str = builder.CreateString("test model")

    tflite.ModelStart(builder)
    tflite.ModelAddSubgraphs(builder, subgraphs_vec)
    tflite.ModelAddDescription(builder, desc_str)
    model = tflite.ModelEnd(builder)

    builder.Finish(model)
    path = tmp_path / "model.tflite"
    path.write_bytes(builder.Output())
    return path
