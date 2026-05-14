"""Public plot generator skeleton."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_public_plots(measurements: dict[str, Any], output_dir: Path) -> list[Path]:
    """Show the plot generation boundary used by the private framework."""
    _ = measurements
    output_dir.mkdir(parents=True, exist_ok=True)
    return [
        output_dir / "inverter_vtc.png",
        output_dir / "gain_phase_response_vm.png",
        output_dir / "best_waveform_stacked.png",
    ]

