"""Public operating-region checker skeleton."""

from __future__ import annotations

from typing import Iterable, Protocol


class RegionCandidate(Protocol):
    device_role: str
    region: str
    ft_hz: float
    gm_gds: float


def check_candidate_regions(candidates: Iterable[RegionCandidate]) -> dict[str, str]:
    """Check public candidate metadata for review-safe region status."""
    report: dict[str, str] = {}
    for candidate in candidates:
        if "checked" not in candidate.region:
            report[candidate.device_role] = "needs_review"
        elif candidate.ft_hz <= 0.0 or candidate.gm_gds <= 0.0:
            report[candidate.device_role] = "invalid_public_metadata"
        else:
            report[candidate.device_role] = "region_screen_pass"
    return report

