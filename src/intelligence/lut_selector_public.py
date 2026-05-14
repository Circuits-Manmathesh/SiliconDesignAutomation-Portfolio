"""Public gm/Id LUT selector interface.

Production version queries SPICE-generated gm/Id LUT.
Public portfolio version shows interface only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LutCandidate:
    device_role: str
    gm_id: float
    id_per_width: float
    gm_gds: float
    ft_hz: float
    cgg_per_width: float
    region: str


def select_lut_candidates(spec: dict[str, Any]) -> list[LutCandidate]:
    """Return representative public candidates without exposing private LUT data."""
    _ = spec
    return [
        LutCandidate(
            device_role="nmos_pull_down",
            gm_id=12.0,
            id_per_width=0.001,
            gm_gds=18.0,
            ft_hz=120.0e9,
            cgg_per_width=1.5e-15,
            region="saturation_margin_checked",
        ),
        LutCandidate(
            device_role="pmos_pull_up",
            gm_id=10.5,
            id_per_width=0.0007,
            gm_gds=16.0,
            ft_hz=95.0e9,
            cgg_per_width=1.8e-15,
            region="saturation_margin_checked",
        ),
    ]

