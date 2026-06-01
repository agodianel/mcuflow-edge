from pathlib import Path

from mcuflow_edge.pack.artifacts import create_package
from mcuflow_edge.targets.stm32.template_vars import STM32_TEMPLATE_VARS


class Stm32Packager:
    @staticmethod
    def pack(model_path: Path, output_dir: Path) -> Path:
        return create_package(
            target="stm32",
            model_path=model_path,
            output_dir=output_dir,
            output_labels=STM32_TEMPLATE_VARS["output_labels"],
        )
