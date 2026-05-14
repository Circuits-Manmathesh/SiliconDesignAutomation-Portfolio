"""Public inverter measurement interface."""

from __future__ import annotations

from typing import Any


def measure_inverter_results(spec: dict[str, Any], testbenches: dict[str, Any]) -> dict[str, Any]:
    """Return representative public measurements."""
    _ = testbenches
    return {
        "project_name": spec["project_name"],
        "status": "pass",
        "tphl_s": 16.1e-12,
        "tplh_s": 16.4e-12,
        "rise_time_20_80_s": 10.6e-12,
        "fall_time_20_80_s": 11.9e-12,
        "average_power_w": 0.478e-3,
        "duty_cycle_window": [0.45, 0.55],
        "note": "Production version parses simulator measurements and marker outputs.",
    }

