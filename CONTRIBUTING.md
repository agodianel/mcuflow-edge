# Contributing to MCUflow-Edge

Thank you for considering contributing! This guide will help you get started.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/agodianel/mcuflow-edge.git
cd mcuflow-edge
```

### 2. Install dependencies

MCUflow-Edge uses [uv](https://docs.astral.sh/uv/) for Python project management:

```bash
uv sync
```

This installs the project in editable mode along with all dev dependencies (pytest, ruff).

### 3. Verify everything works

```bash
uv run pytest tests/ -v
uv run mcue --help
```

## Development Workflow

### Running tests

```bash
uv run pytest tests/ -v
```

### Linting

```bash
uv run ruff check mcuflow_edge/ tests/
uv run ruff format --check mcuflow_edge/ tests/
```

### Running the CLI

```bash
uv run mcue init imu-gesture
uv run mcue --help
```

## Coding Conventions

- **Python 3.11+** — use modern syntax (`X | Y` for unions, etc.)
- **`pathlib`** over raw path strings
- **`dataclasses`** for schema-like objects
- **JSON outputs** formatted consistently (2-space indent, trailing newline)
- **Small modules** with explicit responsibilities
- **Target-specific logic** stays inside `mcuflow_edge/targets/`
- **No board-specific assumptions** outside target adapters
- **Readable code** over framework-heavy abstractions

## Project Structure

```
mcuflow_edge/
├── cli/        # Click command definitions
├── capture/    # Serial capture and session I/O
├── dataset/    # Dataset builder and validators
├── pack/       # Model packaging and manifest
├── deploy/     # Artifact deployment
├── bench/      # Benchmark parsing and reports
├── targets/    # Target adapters (esp32/, stm32/)
└── utils/      # Shared utilities
```

## How to Add a New Target

1. Create a new directory: `mcuflow_edge/targets/<target_name>/`
2. Implement the target adapter:
   - `target.py` — class inheriting from `TargetAdapter`
   - `packager.py` — model packaging logic
   - `deployer.py` — firmware template deployment
   - `template_vars.py` — board configuration
3. Register the adapter in `mcuflow_edge/targets/__init__.py`
4. Add a firmware template in `firmware/<target>-template/`
5. Add tests in `tests/`
6. Update `docs/supported-boards.md`

## Pull Request Checklist

- [ ] Tests pass (`uv run pytest tests/`)
- [ ] Lint passes (`uv run ruff check mcuflow_edge/ tests/`)
- [ ] New features include tests
- [ ] CLI changes documented in `--help` output
- [ ] Deterministic output paths maintained
- [ ] No hardcoded board assumptions outside target adapters
- [ ] Session schema changes include a version bump
- [ ] Documentation updated where relevant

## V1 Constraints

Keep these in mind when contributing:

- Support only **ESP32** and **STM32** targets
- Support only the **IMU gesture** example
- No web dashboards or cloud dependencies
- Prefer deterministic file outputs
- Keep the CLI stable and human-readable
