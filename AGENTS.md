# MCUflow-Edge — AI Agent Guide

## Mission
Build MCUflow-Edge V1: a unified edge AI workflow for ESP32 and STM32.

## V1 Constraints
- Support only ESP32 and STM32.
- Support only the IMU gesture example.
- Do not introduce web dashboards or cloud dependencies.
- Prefer deterministic file outputs.
- Keep CLI stable and human-readable.

## Important Rules
- Do not break the session schema without versioning it.
- Do not hardcode board-specific assumptions outside target adapters.
- Keep target-specific logic inside `mcuflow_edge/targets/`.
- Add tests for every new manifest or parser change.

## Build Tool
- Use `uv` for all Python project management (sync, lock, add, run).
- Run `uv sync` to install the project and dev dependencies.
- Run `uv run pytest tests/` to execute tests.

## Coding Conventions
- Python 3.11+
- `pathlib` over raw path strings
- `dataclasses` for schema-like objects
- JSON outputs formatted consistently
- Small modules with explicit responsibilities
- Avoid hiding target-specific logic in generic helpers
- Prefer readable code over framework-heavy abstractions
