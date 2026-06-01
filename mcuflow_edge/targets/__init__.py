"""Central target adapter registry.

Provides a single lookup point for all supported target adapters,
so CLI commands don't need to hard-import specific classes.
"""

from mcuflow_edge.targets.base import TargetAdapter
from mcuflow_edge.targets.esp32.target import Esp32TargetAdapter
from mcuflow_edge.targets.stm32.target import Stm32TargetAdapter

TARGET_REGISTRY: dict[str, type[TargetAdapter]] = {
    "esp32": Esp32TargetAdapter,
    "stm32": Stm32TargetAdapter,
}

SUPPORTED_TARGETS = list(TARGET_REGISTRY.keys())


def get_adapter(target_name: str) -> TargetAdapter:
    """Look up and instantiate a target adapter by name.

    Raises:
        KeyError: If the target name is not registered.
    """
    adapter_cls = TARGET_REGISTRY.get(target_name)
    if adapter_cls is None:
        supported = ", ".join(sorted(TARGET_REGISTRY.keys()))
        raise KeyError(f"Unknown target '{target_name}'. Supported targets: {supported}")
    return adapter_cls()
