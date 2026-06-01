"""Tests for the target adapter registry."""

import pytest

from mcuflow_edge.targets import SUPPORTED_TARGETS, TARGET_REGISTRY, get_adapter
from mcuflow_edge.targets.base import TargetAdapter
from mcuflow_edge.targets.esp32.target import Esp32TargetAdapter
from mcuflow_edge.targets.stm32.target import Stm32TargetAdapter


def test_target_adapters_implement_base():
    assert issubclass(Esp32TargetAdapter, TargetAdapter)
    assert issubclass(Stm32TargetAdapter, TargetAdapter)


def test_registry_contains_both_targets():
    assert set(TARGET_REGISTRY.keys()) == {"esp32", "stm32"}


def test_supported_targets_list():
    assert "esp32" in SUPPORTED_TARGETS
    assert "stm32" in SUPPORTED_TARGETS


def test_get_adapter_esp32():
    adapter = get_adapter("esp32")
    assert isinstance(adapter, Esp32TargetAdapter)
    assert adapter.name == "esp32"


def test_get_adapter_stm32():
    adapter = get_adapter("stm32")
    assert isinstance(adapter, Stm32TargetAdapter)
    assert adapter.name == "stm32"


def test_get_adapter_unknown_raises():
    with pytest.raises(KeyError, match="Unknown target"):
        get_adapter("nrf52")


def test_get_adapter_unknown_lists_supported():
    with pytest.raises(KeyError, match="esp32"):
        get_adapter("unknown_target")
