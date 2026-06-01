from pathlib import Path

import pytest

from mcuflow_edge.deploy.copier import copy_file
from mcuflow_edge.deploy.esp32 import deploy_esp32
from mcuflow_edge.deploy.stm32 import deploy_stm32
from mcuflow_edge.targets.esp32.deployer import Esp32Deployer
from mcuflow_edge.targets.esp32.packager import Esp32Packager
from mcuflow_edge.targets.stm32.packager import Stm32Packager


class TestPackagers:
    def test_esp32_packager_creates_artifacts(self, valid_tflite_model: Path, tmp_path: Path):
        output_dir = tmp_path / "pack"
        result = Esp32Packager.pack(valid_tflite_model, output_dir)
        assert result == output_dir / "esp32"
        assert (result / "model.tflite").exists()
        assert (result / "pack_manifest.json").exists()

    def test_stm32_packager_creates_artifacts(self, valid_tflite_model: Path, tmp_path: Path):
        output_dir = tmp_path / "pack"
        result = Stm32Packager.pack(valid_tflite_model, output_dir)
        assert result == output_dir / "stm32"


class TestDeployers:
    def test_esp32_deploy_copies_model(self, tmp_path: Path):
        package_dir = tmp_path / "package"
        package_dir.mkdir(parents=True)
        (package_dir / "model.tflite").write_bytes(b"model data")
        (package_dir / "pack_manifest.json").write_text('{"target": "esp32"}')

        firmware_dir = tmp_path / "firmware" / "main"
        firmware_dir.mkdir(parents=True)

        Esp32Deployer.deploy(package_dir, firmware_dir=tmp_path / "firmware")
        assert (firmware_dir / "model.tflite").exists()

    def test_stm32_deploy_copies_model(self, tmp_path: Path):
        package_dir = tmp_path / "package"
        package_dir.mkdir(parents=True)
        (package_dir / "model.tflite").write_bytes(b"model data")
        (package_dir / "pack_manifest.json").write_text('{"target": "stm32"}')

        firmware_dir = tmp_path / "firmware"
        deploy_stm32(package_dir, firmware_dir)

        assert (firmware_dir / "X-CUBE-AI" / "model.tflite").exists()

    def test_deploy_missing_manifest(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            deploy_esp32(tmp_path / "empty", tmp_path / "firmware")

    def test_deploy_missing_model(self, tmp_path: Path):
        package_dir = tmp_path / "package"
        package_dir.mkdir()
        (package_dir / "pack_manifest.json").write_text("{}")
        with pytest.raises(FileNotFoundError):
            deploy_esp32(package_dir, tmp_path / "firmware")


class TestCopier:
    def test_copy_file(self, tmp_path: Path):
        src = tmp_path / "src.txt"
        src.write_text("hello")
        dst = tmp_path / "dst" / "dst.txt"
        result = copy_file(src, dst)
        assert result.exists()
        assert result.read_text() == "hello"

    def test_copy_file_no_overwrite(self, tmp_path: Path):
        src = tmp_path / "src.txt"
        src.write_text("hello")
        dst = tmp_path / "dst.txt"
        dst.write_text("existing")
        result = copy_file(src, dst, overwrite=False)
        assert result.read_text() == "existing"
