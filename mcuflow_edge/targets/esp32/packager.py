from pathlib import Path

from mcuflow_edge.pack.artifacts import create_package
from mcuflow_edge.targets.esp32.template_vars import ESP32_TEMPLATE_VARS


class Esp32Packager:
    @staticmethod
    def pack(model_path: Path, output_dir: Path) -> Path:
        return create_package(
            target="esp32",
            model_path=model_path,
            output_dir=output_dir,
            output_labels=ESP32_TEMPLATE_VARS["output_labels"],
        )
