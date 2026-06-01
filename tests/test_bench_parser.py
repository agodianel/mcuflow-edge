import json
from pathlib import Path

import pytest

from mcuflow_edge.bench.parser import parse_bench_line, parse_bench_output
from mcuflow_edge.bench.report import write_bench_report


class TestBenchParser:
    def test_parse_valid_line(self):
        line = "BNCH 12.4,14.2,182304,48128"
        result = parse_bench_line(line)
        assert result is not None
        assert result["latency_ms_avg"] == 12.4
        assert result["latency_ms_p95"] == 14.2
        assert result["flash_bytes"] == 182304
        assert result["ram_bytes"] == 48128

    def test_parse_invalid_prefix(self):
        assert parse_bench_line("OTHER 1,2,3,4") is None

    def test_parse_malformed(self):
        assert parse_bench_line("BNCH not,a,number") is None

    def test_parse_too_few_fields(self):
        assert parse_bench_line("BNCH 1,2,3") is None

    def test_parse_output(self):
        lines = [
            "some log line",
            "BNCH 5.0,6.0,90000,32000",
            "another line",
        ]
        result = parse_bench_output(lines)
        assert result["latency_ms_avg"] == 5.0
        assert result["ram_bytes"] == 32000

    def test_parse_output_no_data(self):
        with pytest.raises(ValueError, match="No benchmark data"):
            parse_bench_output(["log line 1", "log line 2"])


class TestBenchReport:
    def test_write_report(self, tmp_path: Path):
        report_dir = tmp_path / "reports"
        bench_data = {
            "latency_ms_avg": 12.4,
            "latency_ms_p95": 14.2,
            "input_shape": [1, 128, 6],
            "flash_bytes": 182304,
            "ram_bytes": 48128,
        }
        path = write_bench_report(
            target="esp32",
            board="esp32-s3-devkit",
            model_name="gesture.tflite",
            bench_data=bench_data,
            report_dir=report_dir,
        )
        assert path.exists()
        report = json.loads(path.read_text())
        assert report["target"] == "esp32"
        assert report["latency_ms_avg"] == 12.4
        assert report["flash_bytes"] == 182304
        assert "timestamp" in report
        assert "tool_version" in report
