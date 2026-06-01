from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

import pandas as pd
from rich.console import Console
from rich.table import Table

from core.clock_math import compute_core_math
from core.models import (
    CrosstalkMode,
    PlaybookInputs,
    TimingStatus,
    default_ai_soc_5ghz_inputs,
)
from core.recommendation_engine import generate_recommendations
from core.timing_engine import compute_timing_result
from core.waveform_engine import generate_waveforms, waveform_summary


@dataclass(frozen=True)
class ValidationResult:
    case_name: str
    passed: bool
    message: str


def _close(
    actual: float,
    expected: float,
    abs_tol: float = 1e-3,
    rel_tol: float = 1e-6,
) -> bool:
    return math.isclose(actual, expected, abs_tol=abs_tol, rel_tol=rel_tol)


def _pass(name: str, message: str) -> ValidationResult:
    return ValidationResult(case_name=name, passed=True, message=message)


def _fail(name: str, message: str) -> ValidationResult:
    return ValidationResult(case_name=name, passed=False, message=message)


def _replace_clock(
    cfg: PlaybookInputs,
    **updates,
) -> PlaybookInputs:
    return cfg.model_copy(
        update={
            "clock": cfg.clock.model_copy(update=updates),
        }
    )


def _replace_interconnect(
    cfg: PlaybookInputs,
    **updates,
) -> PlaybookInputs:
    return cfg.model_copy(
        update={
            "interconnect": cfg.interconnect.model_copy(update=updates),
        }
    )


def _replace_noise(
    cfg: PlaybookInputs,
    **updates,
) -> PlaybookInputs:
    return cfg.model_copy(
        update={
            "noise": cfg.noise.model_copy(update=updates),
        }
    )


def _replace_timing(
    cfg: PlaybookInputs,
    **updates,
) -> PlaybookInputs:
    return cfg.model_copy(
        update={
            "timing": cfg.timing.model_copy(update=updates),
        }
    )


def validate_baseline_core_math() -> ValidationResult:
    """
    Validate canonical 5 GHz AI SoC baseline.

    Baseline:
        Frequency = 5 GHz
        PLL jitter = 120 fs
        Duty = 51.5%
        Wire length = 2400 um
        Sheet R = 28 mohm/sq
        C = 95 aF/um
        Repeaters = 4
        Droop = 45 mV
        Crosstalk = Quiet
        Shielding/decaps = ON

    Expected key values:
        Tclk = 200 ps
        Squares = 30000
        Rwire = 840 ohm
        Cwire = 228 fF
        tau_total = 191.52 ps
        tau_segment = 7.6608 ps
        insertion = 12.8 ps
        before_slew = 19.18592 ps
        after_slew = 6.715072 ps
        before_jitter = 1386.546629 fs
        after_jitter = 485.291320 fs
    """

    name = "baseline_core_math"

    cfg = default_ai_soc_5ghz_inputs()
    result = compute_core_math(cfg)

    checks = [
        ("clock_period_ps", result.clock_period_ps, 200.0),
        ("duty_cycle_error_percent", result.duty_cycle_error_percent, 1.5),
        ("wire_squares", result.wire_squares, 30000.0),
        ("wire_resistance_ohm", result.wire_resistance_ohm, 840.0),
        ("wire_capacitance_ff", result.wire_capacitance_ff, 228.0),
        ("total_rc_tau_ps", result.total_rc_tau_ps, 191.52),
        ("segment_rc_tau_ps", result.segment_rc_tau_ps, 7.6608),
        ("insertion_delay_ps", result.insertion_delay_ps, 12.8),
        ("before_slew_ps", result.before_slew_ps, 19.18592),
        ("after_slew_ps", result.after_slew_ps, 6.715072),
        ("psij_edge_shift_ps", result.psij_edge_shift_ps, 0.216),
        ("psij_jitter_fs", result.psij_jitter_fs, 81.0),
        ("crosstalk_edge_shift_ps", result.crosstalk_edge_shift_ps, 0.0),
        ("crosstalk_jitter_fs", result.crosstalk_jitter_fs, 8.0),
        ("rc_uncertainty_fs", result.rc_uncertainty_fs, 1378.944),
        ("before_total_jitter_fs", result.before_total_jitter_fs, 1386.546629),
        ("after_total_jitter_fs", result.after_total_jitter_fs, 485.291320),
        ("before_edge_shift_ps", result.before_edge_shift_ps, 13.016),
        ("after_edge_shift_ps", result.after_edge_shift_ps, 12.8756),
    ]

    for label, actual, expected in checks:
        if not _close(actual, expected, abs_tol=1e-3):
            return _fail(
                name,
                f"{label} mismatch: actual={actual:.6f}, expected={expected:.6f}",
            )

    return _pass(
        name,
        "Baseline core math values match expected 5 GHz AI SoC reference case.",
    )


def validate_long_wire_stress() -> ValidationResult:
    """
    Validate wire-length stress case.

    Change:
        Wire length = 3500 um
        Repeaters = 4

    Expected:
        Squares = 43750
        Rwire = 1225 ohm
        Cwire = 332.5 fF
        tau_total = 407.3125 ps
        tau_segment = 16.2925 ps
        before_slew = 39.902 ps
    """

    name = "long_wire_stress"

    cfg = default_ai_soc_5ghz_inputs()
    cfg = _replace_interconnect(cfg, global_wire_length_um=3500.0)

    result = compute_core_math(cfg)

    checks = [
        ("wire_squares", result.wire_squares, 43750.0),
        ("wire_resistance_ohm", result.wire_resistance_ohm, 1225.0),
        ("wire_capacitance_ff", result.wire_capacitance_ff, 332.5),
        ("total_rc_tau_ps", result.total_rc_tau_ps, 407.3125),
        ("segment_rc_tau_ps", result.segment_rc_tau_ps, 16.2925),
        ("before_slew_ps", result.before_slew_ps, 39.902),
    ]

    for label, actual, expected in checks:
        if not _close(actual, expected, abs_tol=1e-3):
            return _fail(
                name,
                f"{label} mismatch: actual={actual:.6f}, expected={expected:.6f}",
            )

    return _pass(
        name,
        "Long-wire RC stress values match expected trend and calculations.",
    )


def validate_repeater_tradeoff() -> ValidationResult:
    """
    Validate that more repeaters reduce segment RC and slew,
    but increase insertion delay.

    Scenario:
        Wire length = 3500 um
        Compare repeater count = 2 vs 8
    """

    name = "repeater_tradeoff"

    base = default_ai_soc_5ghz_inputs()
    base = _replace_interconnect(base, global_wire_length_um=3500.0)

    low_rep_cfg = _replace_interconnect(base, repeater_count=2)
    high_rep_cfg = _replace_interconnect(base, repeater_count=8)

    low = compute_core_math(low_rep_cfg)
    high = compute_core_math(high_rep_cfg)

    if not high.segment_rc_tau_ps < low.segment_rc_tau_ps:
        return _fail(
            name,
            "Expected higher repeater count to reduce segment RC tau.",
        )

    if not high.before_slew_ps < low.before_slew_ps:
        return _fail(
            name,
            "Expected higher repeater count to improve before-mitigation slew.",
        )

    if not high.insertion_delay_ps > low.insertion_delay_ps:
        return _fail(
            name,
            "Expected higher repeater count to increase insertion delay.",
        )

    if not _close(low.segment_rc_tau_ps, 45.256944, abs_tol=1e-3):
        return _fail(
            name,
            f"Low-repeater segment tau mismatch: {low.segment_rc_tau_ps:.6f}",
        )

    if not _close(high.segment_rc_tau_ps, 5.028549, abs_tol=1e-3):
        return _fail(
            name,
            f"High-repeater segment tau mismatch: {high.segment_rc_tau_ps:.6f}",
        )

    return _pass(
        name,
        (
            "Repeater tradeoff is correct: more repeaters improve segment RC/slew "
            "but increase insertion delay."
        ),
    )


def validate_ir_drop_and_crosstalk_stress() -> ValidationResult:
    """
    Validate PSIJ and crosstalk terms.

    Scenario:
        Wire length = 3500 um
        Repeaters = 8
        Droop = 70 mV
        Crosstalk = In-Phase

    Expected:
        PSIJ shift = 0.336 ps
        PSIJ jitter = 126 fs
        Crosstalk shift = +0.75 ps
        Crosstalk jitter = 32 fs
    """

    name = "ir_drop_and_crosstalk_stress"

    cfg = default_ai_soc_5ghz_inputs()
    cfg = _replace_interconnect(
        cfg,
        global_wire_length_um=3500.0,
        repeater_count=8,
    )
    cfg = _replace_noise(
        cfg,
        dynamic_vdd_droop_mv=70.0,
        crosstalk_mode=CrosstalkMode.IN_PHASE,
        shielding_decaps_enabled=True,
    )

    result = compute_core_math(cfg)

    checks = [
        ("psij_edge_shift_ps", result.psij_edge_shift_ps, 0.336),
        ("psij_jitter_fs", result.psij_jitter_fs, 126.0),
        ("crosstalk_edge_shift_ps", result.crosstalk_edge_shift_ps, 0.75),
        ("crosstalk_jitter_fs", result.crosstalk_jitter_fs, 32.0),
    ]

    for label, actual, expected in checks:
        if not _close(actual, expected, abs_tol=1e-3):
            return _fail(
                name,
                f"{label} mismatch: actual={actual:.6f}, expected={expected:.6f}",
            )

    return _pass(
        name,
        "IR-drop and crosstalk stress terms match expected architecture model.",
    )


def validate_baseline_timing() -> ValidationResult:
    """
    Validate baseline timing.

    Baseline:
        Period = 200 ps
        Logic delay = 175 ps
        Spatial skew = 8 ps
        Useful skew = 0 ps
        Setup = 8 ps
        Hold = 5 ps

    Expected:
        Capture = 208 ps
        Setup slack = 25 ps
        Hold slack = 162 ps
        Status = PASS
    """

    name = "baseline_timing"

    cfg = default_ai_soc_5ghz_inputs()
    core = compute_core_math(cfg)
    timing = compute_timing_result(cfg, core)

    checks = [
        ("capture_clock_ps", timing.capture_clock_ps, 208.0),
        ("setup_slack_ps", timing.setup_slack_ps, 25.0),
        ("hold_slack_ps", timing.hold_slack_ps, 162.0),
    ]

    for label, actual, expected in checks:
        if not _close(actual, expected, abs_tol=1e-6):
            return _fail(
                name,
                f"{label} mismatch: actual={actual:.6f}, expected={expected:.6f}",
            )

    if timing.status != TimingStatus.PASS:
        return _fail(
            name,
            f"Expected PASS status, got {timing.status.value}",
        )

    return _pass(
        name,
        "Baseline setup/hold timing matches expected PASS case.",
    )


def validate_setup_violation_and_recovery() -> ValidationResult:
    """
    Validate setup violation and useful-skew recovery.

    Case 1:
        Logic delay = 203 ps
        Spatial skew = 10 ps
        Useful skew = 0 ps
        Expected setup slack = -1 ps

    Case 2:
        Useful skew = +8 ps
        Expected setup slack = +7 ps
    """

    name = "setup_violation_and_recovery"

    cfg = default_ai_soc_5ghz_inputs()
    cfg_bad = _replace_timing(
        cfg,
        logic_path_delay_ps=203.0,
        spatial_clock_skew_ps=10.0,
        useful_skew_ps=0.0,
    )

    core_bad = compute_core_math(cfg_bad)
    timing_bad = compute_timing_result(cfg_bad, core_bad)

    if not _close(timing_bad.setup_slack_ps, -1.0, abs_tol=1e-6):
        return _fail(
            name,
            f"Expected setup slack -1 ps, got {timing_bad.setup_slack_ps:.6f}",
        )

    if timing_bad.status != TimingStatus.SETUP_VIOLATION:
        return _fail(
            name,
            f"Expected SETUP VIOLATION, got {timing_bad.status.value}",
        )

    cfg_fixed = _replace_timing(
        cfg_bad,
        useful_skew_ps=8.0,
    )

    core_fixed = compute_core_math(cfg_fixed)
    timing_fixed = compute_timing_result(cfg_fixed, core_fixed)

    if not _close(timing_fixed.setup_slack_ps, 7.0, abs_tol=1e-6):
        return _fail(
            name,
            f"Expected recovered setup slack +7 ps, got {timing_fixed.setup_slack_ps:.6f}",
        )

    if timing_fixed.status != TimingStatus.PASS:
        return _fail(
            name,
            f"Expected recovered PASS status, got {timing_fixed.status.value}",
        )

    return _pass(
        name,
        "Setup violation and useful-skew recovery behave as expected.",
    )


def validate_hold_violation_case() -> ValidationResult:
    """
    Validate short-path hold violation.

    Case:
        Logic delay = 28 ps
        Spatial skew = 10 ps
        Useful skew = 18 ps
        Hold = 5 ps

    Expected:
        Hold slack = 28 - (10 + 18 + 5) = -5 ps
        Status = HOLD VIOLATION
    """

    name = "hold_violation_case"

    cfg = default_ai_soc_5ghz_inputs()
    cfg = _replace_timing(
        cfg,
        logic_path_delay_ps=28.0,
        spatial_clock_skew_ps=10.0,
        useful_skew_ps=18.0,
        hold_requirement_ps=5.0,
    )

    core = compute_core_math(cfg)
    timing = compute_timing_result(cfg, core)

    if not _close(timing.hold_slack_ps, -5.0, abs_tol=1e-6):
        return _fail(
            name,
            f"Expected hold slack -5 ps, got {timing.hold_slack_ps:.6f}",
        )

    if timing.status != TimingStatus.HOLD_VIOLATION:
        return _fail(
            name,
            f"Expected HOLD VIOLATION, got {timing.status.value}",
        )

    return _pass(
        name,
        "Short-path hold violation case behaves as expected.",
    )


def validate_waveform_smoke() -> ValidationResult:
    """
    Validate waveform generation smoke case.

    This checks:
        - vector lengths are consistent
        - 6000 samples are generated
        - 6 cycles at 5 GHz gives 1200 ps window
        - clock voltage remains within 0 to nominal VDD
    """

    name = "waveform_smoke"

    cfg = default_ai_soc_5ghz_inputs()
    core = compute_core_math(cfg)
    waveform = generate_waveforms(cfg, core)
    summary = waveform_summary(waveform)

    if int(summary["samples"]) != 6000:
        return _fail(
            name,
            f"Expected 6000 waveform samples, got {summary['samples']}",
        )

    if not _close(summary["time_stop_ps"], 1200.0, abs_tol=1e-6):
        return _fail(
            name,
            f"Expected time stop 1200 ps, got {summary['time_stop_ps']:.6f}",
        )

    for key in [
        "ideal_min_v",
        "degraded_min_v",
        "mitigated_min_v",
    ]:
        if summary[key] < -1e-9:
            return _fail(
                name,
                f"{key} is below 0 V: {summary[key]}",
            )

    for key in [
        "ideal_max_v",
        "degraded_max_v",
        "mitigated_max_v",
    ]:
        if summary[key] > cfg.constants.nominal_vdd_v + 1e-9:
            return _fail(
                name,
                f"{key} exceeds nominal VDD: {summary[key]}",
            )

    return _pass(
        name,
        "Waveform vectors are consistent and within expected voltage/time limits.",
    )


def validate_recommendation_smoke() -> ValidationResult:
    """
    Validate that recommendation engine returns meaningful baseline output.
    """

    name = "recommendation_smoke"

    cfg = default_ai_soc_5ghz_inputs()
    core = compute_core_math(cfg)
    timing = compute_timing_result(cfg, core)
    recs = generate_recommendations(cfg, core, timing)

    if not recs:
        return _fail(
            name,
            "Expected at least one architecture recommendation.",
        )

    titles = {rec.title for rec in recs}

    expected_titles = {
        "High-speed clock budget requires careful tracking",
        "Nominal setup/hold pass",
    }

    missing = expected_titles - titles
    if missing:
        return _fail(
            name,
            f"Missing expected recommendation titles: {sorted(missing)}",
        )

    return _pass(
        name,
        f"Recommendation engine returned {len(recs)} baseline recommendations.",
    )


VALIDATION_CASES: list[Callable[[], ValidationResult]] = [
    validate_baseline_core_math,
    validate_long_wire_stress,
    validate_repeater_tradeoff,
    validate_ir_drop_and_crosstalk_stress,
    validate_baseline_timing,
    validate_setup_violation_and_recovery,
    validate_hold_violation_case,
    validate_waveform_smoke,
    validate_recommendation_smoke,
]


def run_all_validation_cases() -> list[ValidationResult]:
    """
    Run all validation cases.
    """

    return [case() for case in VALIDATION_CASES]


def validation_results_to_dataframe(
    results: list[ValidationResult],
) -> pd.DataFrame:
    """
    Convert validation results to a DataFrame for UI/report use.
    """

    return pd.DataFrame(
        [
            {
                "Case": result.case_name,
                "Passed": result.passed,
                "Message": result.message,
            }
            for result in results
        ]
    )


def print_validation_report(
    results: list[ValidationResult],
) -> None:
    """
    Pretty terminal report using Rich.
    """

    console = Console()

    table = Table(title="Interactive SoC Clock Playbook Validation Report")
    table.add_column("Case", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Message", style="white")

    for result in results:
        status = "[green]PASS[/green]" if result.passed else "[red]FAIL[/red]"
        table.add_row(result.case_name, status, result.message)

    console.print(table)

    passed = sum(1 for result in results if result.passed)
    total = len(results)

    if passed == total:
        console.print(f"[bold green]All validation cases passed: {passed}/{total}[/bold green]")
    else:
        console.print(f"[bold red]Validation failures: {total - passed}/{total}[/bold red]")


def main() -> None:
    results = run_all_validation_cases()
    print_validation_report(results)

    if not all(result.passed for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()


__all__ = [
    "VALIDATION_CASES",
    "ValidationResult",
    "print_validation_report",
    "run_all_validation_cases",
    "validation_results_to_dataframe",
]