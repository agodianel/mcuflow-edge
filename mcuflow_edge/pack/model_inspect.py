from pathlib import Path


def inspect_model(model_path: Path) -> dict:
    raw = model_path.read_bytes()
    info: dict = {
        "size_bytes": len(raw),
        "quantized": False,
        "input_shape": [1, 128, 6],
        "input_dtype": "unknown",
    }

    try:
        import tflite
        model = tflite.Model.GetRootAsModel(raw, 0)
        subgraphs = model.Subgraphs
        if subgraphs:
            sg = subgraphs(0)
            tensors = sg.Tensors
            if tensors:
                t = tensors(0)
                info["input_shape"] = t.ShapeAsNumpy().astype(int).tolist()
                ttype = t.Type()
                info["input_dtype"] = {
                    0: "float32",
                    1: "float16",
                    2: "int32",
                    3: "uint8",
                    9: "int8",
                }.get(ttype, "unknown")
                q = t.Quantization()
                if q:
                    info["quantized"] = q.ScaleIsPresent() or q.ZeroPointIsPresent()
    except Exception:
        pass

    return info
