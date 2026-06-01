from pathlib import Path

from mcuflow_edge.pack.manifest import PackManifest, sha256_of
from mcuflow_edge.pack.model_inspect import inspect_model
from mcuflow_edge.utils.jsonio import write_json


def create_package(
    target: str,
    model_path: Path,
    output_dir: Path,
    output_labels: list[str],
    tool_version: str = "0.1.0",
) -> Path:
    target_dir = output_dir / target
    target_dir.mkdir(parents=True, exist_ok=True)

    model_dest = target_dir / "model.tflite"
    model_dest.write_bytes(model_path.read_bytes())

    model_info = inspect_model(model_path)

    manifest = PackManifest(
        target=target,
        model_path="model.tflite",
        model_sha256=sha256_of(model_path),
        input_shape=model_info.get("input_shape", [1, 128, 6]),
        output_labels=output_labels,
        quantized=model_info.get("quantized", False),
        tool_version=tool_version,
    )

    write_json(target_dir / "pack_manifest.json", manifest.to_dict())
    write_json(target_dir / "model_info.json", model_info)

    generated_dir = target_dir / "generated"
    generated_dir.mkdir(exist_ok=True)

    return target_dir
