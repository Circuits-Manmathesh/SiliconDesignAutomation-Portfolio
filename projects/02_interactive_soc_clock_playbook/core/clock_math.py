from __future__ import annotations

import math

from core.models import CoreMathResult, CrosstalkMode, PlaybookInputs


def _crosstalk_terms(mode: CrosstalkMode) -> tuple[float, float]:
    """
    Return architecture-level crosstalk timing shift and jitter term.

    These values are intentionally simple and explainable:
    - In-phase aggressor can push the victim clock edge in one direction.
    - Out-of-phase aggressor can shift it in the opposite direction.
    - Quiet/orthogonal routing keeps the coupling contribution small.

    Returns:
        (edge_shift_ps, jitter_fs)
    """

    if mode == CrosstalkMode.IN_PHASE:
        return 0.75, 32.0

    if mode == CrosstalkMode.OUT_OF_PHASE:
        return -0.75, 38.0

    return 0.0, 8.0


def compute_core_math(inputs: PlaybookInputs) -> CoreMathResult:
    """
    Compute the core architecture-level clock distribution quantities.

    This is the single source of truth for:
    - waveform engine
    - SoC path engine
    - live math analysis
    - jitter/skew budget
    - recommendation engine

    Technical positioning:
    These calculations are architecture-level sensitivity models.
    They are intentionally transparent and explainable.
    They are not a replacement for signoff extraction using SPEF, Liberty,
    STA, SI, EMIR, OCV, and PVT analysis.
    """

    clock = inputs.clock
    interconnect = inputs.interconnect
    noise = inputs.noise
    constants = inputs.constants

    # ------------------------------------------------------------------
    # 1. Clock period
    # GHz to ps conversion:
    # 1 GHz period = 1000 ps
    # ------------------------------------------------------------------
    clock_period_ps = 1000.0 / clock.frequency_ghz

    # ------------------------------------------------------------------
    # 2. Duty-cycle distortion
    # Ideal duty is 50%.
    # Any deviation from 50% is treated as duty-cycle error.
    # ------------------------------------------------------------------
    duty_cycle_error_percent = abs(clock.pll_duty_cycle_percent - 50.0)

    # ------------------------------------------------------------------
    # 3. Interconnect resistance/capacitance model
    # Squares = length / effective width
    # Rwire = Rsheet * squares
    # Cwire = Cper_um * length
    # ------------------------------------------------------------------
    wire_width_um = constants.wire_width_um
    wire_squares = interconnect.global_wire_length_um / wire_width_um

    sheet_resistance_ohm_sq = (
        interconnect.top_metal_sheet_resistance_mohm_sq * 1e-3
    )

    wire_resistance_ohm = sheet_resistance_ohm_sq * wire_squares

    wire_capacitance_f = (
        interconnect.wire_capacitance_af_um
        * 1e-18
        * interconnect.global_wire_length_um
    )

    wire_capacitance_ff = wire_capacitance_f * 1e15

    # τ = R * C
    # seconds to ps conversion = 1e12
    total_rc_tau_ps = wire_resistance_ohm * wire_capacitance_f * 1e12

    # ------------------------------------------------------------------
    # 4. Repeater segmentation
    # For a simple first-order architecture model:
    # segment tau scales approximately as tau_total / segments^2
    # where segments = repeaters + 1.
    # ------------------------------------------------------------------
    segment_count = interconnect.repeater_count + 1
    segment_rc_tau_ps = total_rc_tau_ps / (segment_count**2)

    # ------------------------------------------------------------------
    # 5. Repeater insertion delay
    # Each inserted buffer/repeater restores edge quality but adds latency.
    # ------------------------------------------------------------------
    insertion_delay_ps = (
        interconnect.repeater_count * constants.buffer_delay_ps
    )

    # ------------------------------------------------------------------
    # 6. Slew approximation
    # A simple explainable model:
    # before_slew = base_slew + k * segment_tau
    #
    # After mitigation, shielding/decap/clock conditioning reduces
    # the effective degradation seen in the waveform.
    # ------------------------------------------------------------------
    before_slew_ps = (
        constants.base_slew_ps
        + constants.rc_slew_gain * segment_rc_tau_ps
    )

    mitigation_factor = (
        constants.shielded_mitigation_factor
        if noise.shielding_decaps_enabled
        else constants.unshielded_mitigation_factor
    )

    after_slew_ps = max(
        constants.base_slew_ps,
        before_slew_ps * mitigation_factor,
    )

    # ------------------------------------------------------------------
    # 7. Power Supply Induced Jitter / delay shift
    # VDD droop slows clock buffers and shifts edge timing.
    # ------------------------------------------------------------------
    psij_edge_shift_ps = (
        constants.psij_delay_coeff_ps_per_mv
        * noise.dynamic_vdd_droop_mv
    )

    psij_jitter_fs = (
        constants.psij_jitter_coeff_fs_per_mv
        * noise.dynamic_vdd_droop_mv
    )

    # ------------------------------------------------------------------
    # 8. Crosstalk timing shift
    # ------------------------------------------------------------------
    crosstalk_edge_shift_ps, crosstalk_jitter_fs = _crosstalk_terms(
        noise.crosstalk_mode
    )

    # ------------------------------------------------------------------
    # 9. RC uncertainty
    # Important:
    # Use effective segment RC, not total unbuffered RC.
    #
    # This is more defensible because a real clock trunk is segmented
    # using repeaters/buffers.
    # ------------------------------------------------------------------
    rc_uncertainty_fs = (
        constants.rc_uncertainty_coeff
        * segment_rc_tau_ps
        * 1000.0
    )

    # ------------------------------------------------------------------
    # 10. Total jitter before/after mitigation
    # RSS model:
    # independent uncertainty sources are combined in root-sum-square form.
    # ------------------------------------------------------------------
    before_total_jitter_fs = math.sqrt(
        clock.pll_random_jitter_fs**2
        + rc_uncertainty_fs**2
        + psij_jitter_fs**2
        + crosstalk_jitter_fs**2
    )

    after_total_jitter_fs = before_total_jitter_fs * mitigation_factor

    # ------------------------------------------------------------------
    # 11. Edge shift before/after mitigation
    # Insertion delay remains because buffers physically exist.
    # Noise-induced shifts are reduced by mitigation.
    # ------------------------------------------------------------------
    before_edge_shift_ps = (
        insertion_delay_ps
        + psij_edge_shift_ps
        + crosstalk_edge_shift_ps
    )

    after_edge_shift_ps = (
        insertion_delay_ps
        + mitigation_factor
        * (psij_edge_shift_ps + crosstalk_edge_shift_ps)
    )

    return CoreMathResult(
        clock_period_ps=clock_period_ps,
        duty_cycle_error_percent=duty_cycle_error_percent,
        wire_width_um=wire_width_um,
        wire_squares=wire_squares,
        wire_resistance_ohm=wire_resistance_ohm,
        wire_capacitance_ff=wire_capacitance_ff,
        total_rc_tau_ps=total_rc_tau_ps,
        segment_count=segment_count,
        segment_rc_tau_ps=segment_rc_tau_ps,
        insertion_delay_ps=insertion_delay_ps,
        before_slew_ps=before_slew_ps,
        after_slew_ps=after_slew_ps,
        psij_edge_shift_ps=psij_edge_shift_ps,
        psij_jitter_fs=psij_jitter_fs,
        crosstalk_edge_shift_ps=crosstalk_edge_shift_ps,
        crosstalk_jitter_fs=crosstalk_jitter_fs,
        rc_uncertainty_fs=rc_uncertainty_fs,
        before_total_jitter_fs=before_total_jitter_fs,
        after_total_jitter_fs=after_total_jitter_fs,
        mitigation_factor=mitigation_factor,
        before_edge_shift_ps=before_edge_shift_ps,
        after_edge_shift_ps=after_edge_shift_ps,
    )


def format_core_math_summary(result: CoreMathResult) -> dict[str, str]:
    """
    Small helper for terminal checks, debug logs, and documentation examples.
    """

    return {
        "Clock Period": f"{result.clock_period_ps:.3f} ps",
        "DCD": f"{result.duty_cycle_error_percent:.3f} %",
        "Wire Squares": f"{result.wire_squares:.3f}",
        "Rwire": f"{result.wire_resistance_ohm:.3f} ohm",
        "Cwire": f"{result.wire_capacitance_ff:.3f} fF",
        "Total RC Tau": f"{result.total_rc_tau_ps:.3f} ps",
        "Segment RC Tau": f"{result.segment_rc_tau_ps:.3f} ps",
        "Insertion Delay": f"{result.insertion_delay_ps:.3f} ps",
        "Before Slew": f"{result.before_slew_ps:.3f} ps",
        "After Slew": f"{result.after_slew_ps:.3f} ps",
        "PSIJ Shift": f"{result.psij_edge_shift_ps:.3f} ps",
        "RC Uncertainty": f"{result.rc_uncertainty_fs:.3f} fs",
        "Before Jitter": f"{result.before_total_jitter_fs:.3f} fs",
        "After Jitter": f"{result.after_total_jitter_fs:.3f} fs",
        "Before Edge Shift": f"{result.before_edge_shift_ps:.3f} ps",
        "After Edge Shift": f"{result.after_edge_shift_ps:.3f} ps",
    }


__all__ = [
    "compute_core_math",
    "format_core_math_summary",
]