from __future__ import annotations

import pandas as pd

from core.models import (
    CoreMathResult,
    CrosstalkMode,
    PlaybookInputs,
    Recommendation,
    RiskLevel,
    TimingResult,
    TimingStatus,
)


def _make_recommendation(
    priority: int,
    risk_level: RiskLevel,
    title: str,
    observation: str,
    recommended_action: str,
    engineering_reason: str,
) -> Recommendation:
    """
    Helper to keep recommendation construction consistent.
    """

    return Recommendation(
        priority=priority,
        risk_level=risk_level,
        title=title,
        observation=observation,
        recommended_action=recommended_action,
        engineering_reason=engineering_reason,
    )


def generate_recommendations(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
    timing: TimingResult,
) -> list[Recommendation]:
    """
    Generate architecture recommendations from live clock analysis values.

    Important positioning:
    These recommendations are architecture-review suggestions.
    They do not replace detailed STA/CTS/SI/EMIR signoff.
    They help identify which design knob should be investigated first.
    """

    recs: list[Recommendation] = []

    clock = inputs.clock
    interconnect = inputs.interconnect
    noise = inputs.noise

    # ------------------------------------------------------------------
    # 1. Clock period / frequency pressure
    # ------------------------------------------------------------------
    if core_math.clock_period_ps <= 160.0:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Very tight clock period",
                observation=(
                    f"Clock period is {core_math.clock_period_ps:.2f} ps "
                    f"at {clock.frequency_ghz:.2f} GHz."
                ),
                recommended_action=(
                    "Keep explicit jitter, skew, slew, setup, hold, and IR-drop budgets. "
                    "Avoid treating the clock as an ideal square wave."
                ),
                engineering_reason=(
                    "At very high frequency, even small edge movement consumes a visible "
                    "fraction of the timing cycle."
                ),
            )
        )
    elif core_math.clock_period_ps <= 250.0:
        recs.append(
            _make_recommendation(
                priority=2,
                risk_level=RiskLevel.MEDIUM,
                title="High-speed clock budget requires careful tracking",
                observation=(
                    f"Clock period is {core_math.clock_period_ps:.2f} ps. "
                    "Timing margin is limited."
                ),
                recommended_action=(
                    "Track clock uncertainty, local skew, RC slew, and setup/hold "
                    "margin together during architecture review."
                ),
                engineering_reason=(
                    "At multi-GHz operation, clock distribution effects can become "
                    "comparable to useful timing margin."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 2. Duty-cycle distortion
    # ------------------------------------------------------------------
    if core_math.duty_cycle_error_percent >= 4.0:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Large duty-cycle distortion",
                observation=(
                    f"Duty-cycle error is {core_math.duty_cycle_error_percent:.2f}%."
                ),
                recommended_action=(
                    "Review PLL output driver symmetry, divider duty-cycle correction, "
                    "and clock-conditioning strategy."
                ),
                engineering_reason=(
                    "Large duty-cycle distortion can reduce latch/DDR/HBM sampling "
                    "aperture and create asymmetric timing windows."
                ),
            )
        )
    elif core_math.duty_cycle_error_percent >= 1.0:
        recs.append(
            _make_recommendation(
                priority=5,
                risk_level=RiskLevel.LOW,
                title="Duty-cycle distortion is present",
                observation=(
                    f"Duty-cycle error is {core_math.duty_cycle_error_percent:.2f}%."
                ),
                recommended_action=(
                    "Keep duty-cycle correction visible in the clock-conditioning budget."
                ),
                engineering_reason=(
                    "Small DCD is usually manageable, but it should not be ignored "
                    "in high-speed interfaces."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 3. Long global wire / RC severity
    # ------------------------------------------------------------------
    if interconnect.global_wire_length_um >= 4000.0:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Very long global clock trunk",
                observation=(
                    f"Global wire length is {interconnect.global_wire_length_um:.0f} µm "
                    f"with total RC indicator {core_math.total_rc_tau_ps:.2f} ps."
                ),
                recommended_action=(
                    "Split the trunk, use wider top metal, add shielding, and optimize "
                    "repeater spacing."
                ),
                engineering_reason=(
                    "Long unsegmented RC routes strongly degrade edge slew and increase "
                    "timing uncertainty."
                ),
            )
        )
    elif interconnect.global_wire_length_um >= 2500.0:
        recs.append(
            _make_recommendation(
                priority=2,
                risk_level=RiskLevel.MEDIUM,
                title="Global trunk length needs segmentation review",
                observation=(
                    f"Global wire length is {interconnect.global_wire_length_um:.0f} µm "
                    f"and total RC indicator is {core_math.total_rc_tau_ps:.2f} ps."
                ),
                recommended_action=(
                    "Check whether repeater count and top-metal width are sufficient "
                    "for the selected trunk length."
                ),
                engineering_reason=(
                    "As length increases, both resistance and capacitance increase, "
                    "so RC severity grows quickly."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 4. Repeater count and effective segment RC
    # ------------------------------------------------------------------
    if core_math.segment_rc_tau_ps >= 25.0:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Segment RC is too high",
                observation=(
                    f"Effective segment RC tau is {core_math.segment_rc_tau_ps:.2f} ps "
                    f"with {interconnect.repeater_count} repeaters."
                ),
                recommended_action=(
                    "Increase repeater count, shorten route segments, or improve metal width."
                ),
                engineering_reason=(
                    "Large segment RC makes the local clock edge slow before the next "
                    "buffer can restore it."
                ),
            )
        )
    elif core_math.segment_rc_tau_ps >= 10.0:
        recs.append(
            _make_recommendation(
                priority=3,
                risk_level=RiskLevel.MEDIUM,
                title="Segment RC should be reviewed",
                observation=(
                    f"Effective segment RC tau is {core_math.segment_rc_tau_ps:.2f} ps."
                ),
                recommended_action=(
                    "Sweep repeater count and review insertion-delay versus slew tradeoff."
                ),
                engineering_reason=(
                    "Moderate segment RC may still be acceptable, but it should be "
                    "balanced against buffer delay and power."
                ),
            )
        )

    if interconnect.repeater_count >= 20:
        recs.append(
            _make_recommendation(
                priority=4,
                risk_level=RiskLevel.MEDIUM,
                title="High repeater count",
                observation=(
                    f"Repeater count is {interconnect.repeater_count}, creating "
                    f"{core_math.insertion_delay_ps:.2f} ps insertion delay."
                ),
                recommended_action=(
                    "Check clock power, EMIR, insertion delay, and skew impact before "
                    "adding more repeaters."
                ),
                engineering_reason=(
                    "Repeaters improve slew, but excessive buffer count increases power, "
                    "latency, and mismatch exposure."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 5. Slew risk
    # ------------------------------------------------------------------
    if core_math.before_slew_ps >= 80.0:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Severe clock slew degradation",
                observation=(
                    f"Before-mitigation slew is {core_math.before_slew_ps:.2f} ps."
                ),
                recommended_action=(
                    "Improve segmentation, strengthen clock drivers, shorten RC path, "
                    "or use wider/protected metal routing."
                ),
                engineering_reason=(
                    "Slow clock edges increase delay uncertainty, short-circuit power, "
                    "and noise sensitivity."
                ),
            )
        )
    elif core_math.before_slew_ps >= 30.0:
        recs.append(
            _make_recommendation(
                priority=3,
                risk_level=RiskLevel.MEDIUM,
                title="Clock slew is becoming slow",
                observation=(
                    f"Before-mitigation slew is {core_math.before_slew_ps:.2f} ps."
                ),
                recommended_action=(
                    "Review repeater spacing and local clock-buffer strength."
                ),
                engineering_reason=(
                    "Moderate slew degradation can reduce effective timing margin "
                    "in high-speed paths."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 6. Dynamic IR-drop / PSIJ
    # ------------------------------------------------------------------
    if noise.dynamic_vdd_droop_mv >= 90.0:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="High dynamic VDD droop",
                observation=(
                    f"Dynamic VDD droop is {noise.dynamic_vdd_droop_mv:.1f} mV, "
                    f"creating PSIJ shift of {core_math.psij_edge_shift_ps:.3f} ps."
                ),
                recommended_action=(
                    "Strengthen power grid, add local decaps, and avoid placing critical "
                    "clock buffers inside heavy switching hotspots."
                ),
                engineering_reason=(
                    "Clock-buffer delay is supply-sensitive. IR-drop can convert "
                    "power-integrity noise into timing uncertainty."
                ),
            )
        )
    elif noise.dynamic_vdd_droop_mv >= 40.0:
        recs.append(
            _make_recommendation(
                priority=2,
                risk_level=RiskLevel.MEDIUM,
                title="Dynamic IR-drop should be tracked",
                observation=(
                    f"Dynamic VDD droop is {noise.dynamic_vdd_droop_mv:.1f} mV "
                    f"and PSIJ shift is {core_math.psij_edge_shift_ps:.3f} ps."
                ),
                recommended_action=(
                    "Review local decap coverage, clock-buffer placement, and "
                    "activity-aware power grid planning."
                ),
                engineering_reason=(
                    "Even sub-ps edge movement can matter when timing margins are small."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 7. Crosstalk
    # ------------------------------------------------------------------
    if noise.crosstalk_mode != CrosstalkMode.QUIET:
        recs.append(
            _make_recommendation(
                priority=2,
                risk_level=RiskLevel.MEDIUM,
                title="Crosstalk alignment is active",
                observation=(
                    f"Crosstalk mode is {noise.crosstalk_mode.value}, causing "
                    f"{core_math.crosstalk_edge_shift_ps:.3f} ps edge shift."
                ),
                recommended_action=(
                    "Apply clock shielding, spacing, layer planning, and SI-aware routing "
                    "near high-toggle aggressors."
                ),
                engineering_reason=(
                    "Coupling can move the clock edge and create deterministic timing shift."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 8. Shielding / decaps
    # ------------------------------------------------------------------
    if not noise.shielding_decaps_enabled:
        if noise.dynamic_vdd_droop_mv >= 40.0 or noise.crosstalk_mode != CrosstalkMode.QUIET:
            recs.append(
                _make_recommendation(
                    priority=1,
                    risk_level=RiskLevel.HIGH,
                    title="Mitigation is disabled while noise is active",
                    observation=(
                        "Shielding/decaps are disabled while droop or crosstalk risk exists."
                    ),
                    recommended_action=(
                        "Enable shielding/decap strategy in the architecture study and "
                        "compare before/after waveform and timing margins."
                    ),
                    engineering_reason=(
                        "The playbook shows mitigation because real clock signoff requires "
                        "both problem identification and a credible repair path."
                    ),
                )
            )
    else:
        recs.append(
            _make_recommendation(
                priority=7,
                risk_level=RiskLevel.LOW,
                title="Mitigation path is enabled",
                observation=(
                    f"Mitigation factor is {core_math.mitigation_factor:.2f}; "
                    "waveform and endpoint jitter are reduced after mitigation."
                ),
                recommended_action=(
                    "Keep before/after comparison visible during design review."
                ),
                engineering_reason=(
                    "A mitigation-aware view helps connect physical fixes to waveform "
                    "and timing behavior."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 9. Endpoint jitter
    # ------------------------------------------------------------------
    if core_math.after_total_jitter_fs >= 800.0:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Endpoint uncertainty is high",
                observation=(
                    f"After-mitigation endpoint jitter metric is "
                    f"{core_math.after_total_jitter_fs:.1f} fs."
                ),
                recommended_action=(
                    "Separate PLL, RC, PSIJ, and crosstalk contributions. "
                    "Optimize the dominant contributor first."
                ),
                engineering_reason=(
                    "A single endpoint jitter number is not enough; root-cause budgeting "
                    "is required for architecture decisions."
                ),
            )
        )
    elif core_math.after_total_jitter_fs >= 400.0:
        recs.append(
            _make_recommendation(
                priority=3,
                risk_level=RiskLevel.MEDIUM,
                title="Endpoint uncertainty should be watched",
                observation=(
                    f"After-mitigation endpoint jitter metric is "
                    f"{core_math.after_total_jitter_fs:.1f} fs."
                ),
                recommended_action=(
                    "Keep jitter budget visible and calibrate with extracted signoff data later."
                ),
                engineering_reason=(
                    "Moderate endpoint uncertainty may be acceptable for architecture study, "
                    "but needs calibration before silicon signoff."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 10. Setup / Hold timing
    # ------------------------------------------------------------------
    if timing.status == TimingStatus.SETUP_VIOLATION:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Setup violation",
                observation=(
                    f"Setup slack is {timing.setup_slack_ps:.3f} ps."
                ),
                recommended_action=(
                    "Reduce logic delay, improve clock/data slew, pipeline the path, "
                    "or apply useful skew carefully."
                ),
                engineering_reason=(
                    "Data is arriving too late relative to the capture edge."
                ),
            )
        )

    elif timing.status == TimingStatus.HOLD_VIOLATION:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Hold violation",
                observation=(
                    f"Hold slack is {timing.hold_slack_ps:.3f} ps."
                ),
                recommended_action=(
                    "Add hold buffers, reduce positive useful skew, or rebalance local CTS."
                ),
                engineering_reason=(
                    "Data is changing too early relative to the hold requirement."
                ),
            )
        )

    elif timing.status == TimingStatus.SETUP_AND_HOLD_RISK:
        recs.append(
            _make_recommendation(
                priority=1,
                risk_level=RiskLevel.HIGH,
                title="Combined setup and hold risk",
                observation=(
                    f"Setup slack is {timing.setup_slack_ps:.3f} ps and "
                    f"hold slack is {timing.hold_slack_ps:.3f} ps."
                ),
                recommended_action=(
                    "Revisit clock skew strategy, logic partitioning, and local CTS balance."
                ),
                engineering_reason=(
                    "Both long-path and short-path timing risks are active."
                ),
            )
        )

    else:
        recs.append(
            _make_recommendation(
                priority=8,
                risk_level=RiskLevel.LOW,
                title="Nominal setup/hold pass",
                observation=(
                    f"Setup slack is {timing.setup_slack_ps:.3f} ps and "
                    f"hold slack is {timing.hold_slack_ps:.3f} ps."
                ),
                recommended_action=(
                    "Preserve timing margin while sweeping stress cases for wire length, "
                    "droop, crosstalk, and skew."
                ),
                engineering_reason=(
                    "A passing nominal path still needs stress testing before architecture signoff."
                ),
            )
        )

    # ------------------------------------------------------------------
    # 11. Useful skew tradeoff
    # ------------------------------------------------------------------
    if abs(timing.useful_skew_ps) >= 20.0:
        recs.append(
            _make_recommendation(
                priority=4,
                risk_level=RiskLevel.MEDIUM,
                title="Large useful skew value",
                observation=(
                    f"Useful skew is {timing.useful_skew_ps:.2f} ps."
                ),
                recommended_action=(
                    "Check both setup and hold across long and short paths before accepting "
                    "this skew strategy."
                ),
                engineering_reason=(
                    "Useful skew can recover setup but may create hold risk."
                ),
            )
        )

    # ------------------------------------------------------------------
    # Final fallback
    # ------------------------------------------------------------------
    if not recs:
        recs.append(
            _make_recommendation(
                priority=10,
                risk_level=RiskLevel.LOW,
                title="Architecture appears balanced in this scenario",
                observation="No dominant risk detected under current slider settings.",
                recommended_action=(
                    "Continue sweeping stress cases and compare against timing/EMIR/SI budgets."
                ),
                engineering_reason=(
                    "Architecture review should cover nominal and stress conditions."
                ),
            )
        )

    return sorted(recs, key=lambda item: (item.priority, item.risk_level.value))


def recommendations_to_dataframe(recommendations: list[Recommendation]) -> pd.DataFrame:
    """
    Convert recommendation list to a UI-friendly DataFrame.
    """

    return pd.DataFrame(
        [
            {
                "Priority": rec.priority,
                "Risk Level": rec.risk_level.value,
                "Title": rec.title,
                "Observation": rec.observation,
                "Recommended Action": rec.recommended_action,
                "Engineering Reason": rec.engineering_reason,
            }
            for rec in recommendations
        ]
    )


def build_recommendation_package(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
    timing: TimingResult,
) -> dict[str, object]:
    """
    Convenience package for UI and docs.
    """

    recommendations = generate_recommendations(
        inputs=inputs,
        core_math=core_math,
        timing=timing,
    )

    table = recommendations_to_dataframe(recommendations)

    return {
        "recommendations": recommendations,
        "table": table,
    }


__all__ = [
    "build_recommendation_package",
    "generate_recommendations",
    "recommendations_to_dataframe",
]