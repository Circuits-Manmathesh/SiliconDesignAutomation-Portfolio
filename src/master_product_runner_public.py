"""Public skeleton for the SiliconDesignAutomation master product runner."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - public skeleton fallback
    yaml = None

from intelligence.sizing_optimizer_public import optimize_sizing
from measurement.inverter_measurement_public import measure_inverter_results
from reporting.report_generator_public import generate_public_report
from testbenches.inverter_testbench_builder_public import build_inverter_testbenches


@dataclass(frozen=True)
class ProjectContext:
    spec_path: Path
    spec: dict[str, Any]
    output_dir: Path


def parse_spec(spec_path: Path) -> dict[str, Any]:
    """Parse a public YAML spec into a dictionary."""
    if yaml is None:
        raise RuntimeError("Install PyYAML to run the public skeleton parser.")
    with spec_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("Project spec must parse to a mapping.")
    return data


def run_preflight(spec: dict[str, Any]) -> None:
    """Validate the minimum fields needed by the public skeleton."""
    required = ["project_name", "design_type", "vdd", "targets"]
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError(f"Missing required spec fields: {', '.join(missing)}")


def route_to_strategy(context: ProjectContext) -> dict[str, Any]:
    """Route a spec to the correct public strategy interface."""
    design_type = context.spec.get("design_type")
    if design_type != "inverter":
        raise NotImplementedError(f"Public skeleton supports inverter only, got {design_type!r}.")

    run_preflight(context.spec)

    sizing = optimize_sizing(context.spec)
    testbenches = build_inverter_testbenches(context.spec, sizing)
    measurements = measure_inverter_results(context.spec, testbenches)
    report = generate_public_report(context.spec, sizing, measurements, context.output_dir)

    return {
        "sizing": sizing,
        "testbenches": testbenches,
        "measurements": measurements,
        "report": report,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Public SDA master product runner skeleton.")
    parser.add_argument("--spec", required=True, type=Path, help="Path to sanitized public project spec.")
    parser.add_argument("--output-dir", type=Path, default=Path("public_run_output"))
    args = parser.parse_args()

    spec = parse_spec(args.spec)
    context = ProjectContext(spec_path=args.spec, spec=spec, output_dir=args.output_dir)
    result = route_to_strategy(context)
    print(f"Public skeleton completed: {result['report']}")


if __name__ == "__main__":
    main()

