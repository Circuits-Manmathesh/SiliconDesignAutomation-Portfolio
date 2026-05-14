"""Public inverter testbench builder interface."""

from __future__ import annotations

from typing import Any


def build_inverter_testbenches(spec: dict[str, Any], sizing: dict[str, Any]) -> dict[str, Any]:
    """Return sanitized testbench descriptors instead of simulator decks."""
    _ = sizing
    return {
        "dc": {
            "analysis": "voltage_transfer_sweep",
            "vdd": spec["vdd"],
        },
        "ac": {
            "analysis": "small_signal_gain_phase",
            "load_capacitance": spec["load"]["capacitance"],
        },
        "tran": {
            "analysis": "clock_timing_duty_cycle_sweep",
            "frequency": spec["clock"]["frequency"],
            "duty_cycle_sweep": spec["clock"]["duty_cycle_sweep"],
        },
        "note": "Production version emits simulator-ready netlists with private model configuration.",
    }

