import json
from pathlib import Path

from mcuflow_edge.pack.artifacts import create_package
from mcuflow_edge.pack.manifest import PackManifest, sha256_of


def test_pack_manifest_defaults():
    manifest = PackManifest(
        target="esp32",
        model_path="model.tflite",
        model_sha256="abc123",
        input_shape=[1, 128, 6],
        output_labels=["idle", "shake"],
        quantized=True,
    )
    data = manifest.to_dict()
    assert data["target"] == "esp32"
    assert data["schema_version"] == 1
    assert data["tool_version"] == "0.1.0"
    assert "created_at" in data


def test_sha256_of(tmp_path: Path):
    f = tmp_path / "test.bin"
    f.write_bytes(b"hello world")
    digest = sha256_of(f)
    assert len(digest) == 64


def test_create_package(valid_tflite_model: Path, tmp_path: Path):
    output_dir = tmp_path / "artifacts"
    result = create_package(
        target="esp32",
        model_path=valid_tflite_model,
        output_dir=output_dir,
        output_labels=["idle", "shake"],
    )

    assert result == output_dir / "esp32"
    assert (result / "model.tflite").exists()
    assert (result / "pack_manifest.json").exists()
    assert (result / "model_info.json").exists()
    assert (result / "generated").is_dir()

    manifest = json.loads((result / "pack_manifest.json").read_text())
    assert manifest["target"] == "esp32"
    assert manifest["output_labels"] == ["idle", "shake"]

    info = json.loads((result / "model_info.json").read_text())
    assert info["input_shape"] == [1, 128, 6]


def test_create_package_fallback_model_info(tmp_path: Path):
    model_path = tmp_path / "bad.tflite"
    model_path.write_bytes(b"\x00" * 50)

    output_dir = tmp_path / "artifacts"
    create_package(
        target="stm32",
        model_path=model_path,
        output_dir=output_dir,
        output_labels=["idle"],
    )

    info = json.loads((output_dir / "stm32" / "model_info.json").read_text())
    assert "size_bytes" in info
    assert info["size_bytes"] == 50
