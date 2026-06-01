from __future__ import annotations

import math
from typing import Iterable

import numpy as np
import pandas as pd

from core.clock_math import compute_core_math
from core.models import CoreMathResult, PlaybookInputs, WaveformResult


def _safe_positive(value: float, floor: float = 1e-15) -> float:
    return max(float(value), floor)


def _logistic_edge(time_ps: np.ndarray, center_ps: float, slew_ps: float) -> np.ndarray:
    """
    Smooth digital edge model.

    A perfect digital edge is vertical, but real clock edges have finite slew.
    We model each transition using a logistic function:

        y = 1 / (1 + exp(-(t - t_edge) / slew))

    Smaller slew_ps:
        sharper edge

    Larger slew_ps:
        slower and more rounded edge

    This is not a transistor-level SPICE model.
    It is an explainable architecture-level waveform model.
    """

    slew_ps = _safe_positive(slew_ps)
    x = np.clip((time_ps - center_ps) / slew_ps, -80.0, 80.0)
    return 1.0 / (1.0 + np.exp(-x))


def _generate_clock_waveform(
    time_ps: np.ndarray,
    frequency_ghz: float,
    duty_cycle_percent: float,
    jitter_rms_fs: float,
    slew_ps: float,
    edge_shift_ps: float,
    amplitude_v: float,
    seed: int,
) -> np.ndarray:
    """
    Generate a synthetic clock waveform using equation-driven edges.

    Parameters:
        time_ps:
            Time axis in ps.

        frequency_ghz:
            Clock frequency.

        duty_cycle_percent:
            High-time percentage.

        jitter_rms_fs:
            RMS random jitter. Internally converted from fs to ps.

        slew_ps:
            Edge slew control. Larger value means slower transition.

        edge_shift_ps:
            Static edge shift caused by insertion delay, PSIJ, and crosstalk.

        amplitude_v:
            Clock voltage amplitude used for visualization.

        seed:
            Deterministic random seed for repeatable demo results.

    Physical interpretation:
        - jitter_rms_fs moves each clock edge randomly
        - duty_cycle_percent changes high/low pulse width
        - slew_ps controls edge sharpness
        - edge_shift_ps moves the waveform in time
    """

    period_ps = 1000.0 / _safe_positive(frequency_ghz)
    duty_fraction = float(np.clip(duty_cycle_percent / 100.0, 0.05, 0.95))
    jitter_rms_ps = jitter_rms_fs / 1000.0

    rng = np.random.default_rng(seed)

    start_cycle = -2
    end_cycle = int(math.ceil((time_ps[-1] - time_ps[0]) / period_ps)) + 4

    waveform = np.zeros_like(time_ps, dtype=float)

    for cycle_index in range(start_cycle, end_cycle):
        # One phase-jitter value per cycle.
        # Rise and fall share the same cycle-level phase movement.
        cycle_jitter_ps = rng.normal(0.0, jitter_rms_ps)

        rise_center_ps = (
            cycle_index * period_ps
            + edge_shift_ps
            + cycle_jitter_ps
        )

        fall_center_ps = (
            cycle_index * period_ps
            + duty_fraction * period_ps
            + edge_shift_ps
            + cycle_jitter_ps
        )

        waveform += _logistic_edge(time_ps, rise_center_ps, slew_ps)
        waveform -= _logistic_edge(time_ps, fall_center_ps, slew_ps)

    waveform = np.clip(waveform, 0.0, 1.0)
    return amplitude_v * waveform


def _mitigated_duty_cycle_percent(inputs: PlaybookInputs) -> float:
    """
    Return duty cycle used for the mitigated waveform.

    Important engineering note:
    Shielding and decaps do not directly fix PLL duty-cycle distortion.
    However, the playbook's 'mitigated clock' represents the combined
    architecture-cleanup view after mitigation and clock conditioning.

    To avoid an unrealistic perfect jump to 50%, we reduce DCD partially:
        residual duty error = mitigation_factor * original duty error

    Example:
        original duty = 51.5%
        mitigation factor = 0.35
        mitigated duty = 50 + 0.35 * 1.5 = 50.525%

    This is more defensible than forcing ideal 50%.
    """

    clock = inputs.clock
    constants = inputs.constants
    noise = inputs.noise

    mitigation_factor = (
        constants.shielded_mitigation_factor
        if noise.shielding_decaps_enabled
        else constants.unshielded_mitigation_factor
    )

    duty_error = clock.pll_duty_cycle_percent - 50.0
    return 50.0 + mitigation_factor * duty_error


def generate_waveforms(
    inputs: PlaybookInputs,
    core_math: CoreMathResult | None = None,
    total_cycles: int = 6,
    samples: int = 6000,
) -> WaveformResult:
    """
    Generate ideal, degraded and mitigated clock waveforms.

    This function is the single waveform generator used by the UI.

    Waveform definitions:

    1. Ideal Clock:
        - 50% duty
        - no jitter
        - base slew
        - no edge shift

    2. Degraded Clock:
        - PLL duty-cycle distortion
        - before_total_jitter_fs
        - before_slew_ps
        - before_edge_shift_ps

    3. Mitigated Clock:
        - partially corrected duty cycle
        - after_total_jitter_fs
        - after_slew_ps
        - after_edge_shift_ps

    The waveform is synthetic but tied directly to architecture formulas.
    """

    if core_math is None:
        core_math = compute_core_math(inputs)

    clock = inputs.clock
    constants = inputs.constants

    period_ps = core_math.clock_period_ps
    t_stop_ps = total_cycles * period_ps
    time_ps = np.linspace(0.0, t_stop_ps, samples)

    ideal_clock_v = _generate_clock_waveform(
        time_ps=time_ps,
        frequency_ghz=clock.frequency_ghz,
        duty_cycle_percent=50.0,
        jitter_rms_fs=0.0,
        slew_ps=constants.base_slew_ps,
        edge_shift_ps=0.0,
        amplitude_v=constants.nominal_vdd_v,
        seed=1,
    )

    degraded_clock_v = _generate_clock_waveform(
        time_ps=time_ps,
        frequency_ghz=clock.frequency_ghz,
        duty_cycle_percent=clock.pll_duty_cycle_percent,
        jitter_rms_fs=core_math.before_total_jitter_fs,
        slew_ps=core_math.before_slew_ps,
        edge_shift_ps=core_math.before_edge_shift_ps,
        amplitude_v=constants.nominal_vdd_v,
        seed=11,
    )

    mitigated_clock_v = _generate_clock_waveform(
        time_ps=time_ps,
        frequency_ghz=clock.frequency_ghz,
        duty_cycle_percent=_mitigated_duty_cycle_percent(inputs),
        jitter_rms_fs=core_math.after_total_jitter_fs,
        slew_ps=core_math.after_slew_ps,
        edge_shift_ps=core_math.after_edge_shift_ps,
        amplitude_v=constants.nominal_vdd_v,
        seed=17,
    )

    return WaveformResult(
        time_ps=time_ps.tolist(),
        ideal_clock_v=ideal_clock_v.tolist(),
        degraded_clock_v=degraded_clock_v.tolist(),
        mitigated_clock_v=mitigated_clock_v.tolist(),
    )


def waveform_to_dataframe(waveform: WaveformResult) -> pd.DataFrame:
    """
    Convert waveform result into a Pandas DataFrame.

    This is useful for:
    - UI tables
    - export
    - debug
    - future CSV report generation
    """

    return pd.DataFrame(
        {
            "time_ps": waveform.time_ps,
            "ideal_clock_v": waveform.ideal_clock_v,
            "degraded_clock_v": waveform.degraded_clock_v,
            "mitigated_clock_v": waveform.mitigated_clock_v,
        }
    )


def waveform_summary(waveform: WaveformResult) -> dict[str, float]:
    """
    Return a compact numeric summary for quick validation.

    This does not replace waveform plotting.
    It is only for terminal checks and automated validation cases.
    """

    time_arr = np.asarray(waveform.time_ps, dtype=float)
    ideal_arr = np.asarray(waveform.ideal_clock_v, dtype=float)
    degraded_arr = np.asarray(waveform.degraded_clock_v, dtype=float)
    mitigated_arr = np.asarray(waveform.mitigated_clock_v, dtype=float)

    return {
        "samples": float(len(time_arr)),
        "time_start_ps": float(time_arr[0]),
        "time_stop_ps": float(time_arr[-1]),
        "ideal_min_v": float(np.min(ideal_arr)),
        "ideal_max_v": float(np.max(ideal_arr)),
        "degraded_min_v": float(np.min(degraded_arr)),
        "degraded_max_v": float(np.max(degraded_arr)),
        "mitigated_min_v": float(np.min(mitigated_arr)),
        "mitigated_max_v": float(np.max(mitigated_arr)),
    }


__all__ = [
    "generate_waveforms",
    "waveform_summary",
    "waveform_to_dataframe",
]