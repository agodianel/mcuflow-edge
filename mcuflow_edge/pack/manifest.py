import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class PackManifest:
    target: str
    model_path: str
    model_sha256: str
    input_shape: list[int]
    output_labels: list[str]
    quantized: bool
    tool_version: str = "0.1.0"
    schema_version: int = 1
    created_at: str = field(
        default_factory=lambda: datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "target": self.target,
            "model_path": self.model_path,
            "model_sha256": self.model_sha256,
            "input_shape": self.input_shape,
            "output_labels": self.output_labels,
            "quantized": self.quantized,
            "created_at": self.created_at,
            "tool_version": self.tool_version,
        }


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
