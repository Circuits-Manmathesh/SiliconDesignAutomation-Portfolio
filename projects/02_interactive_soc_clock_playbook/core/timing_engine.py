from __future__ import annotations

import pandas as pd

from core.clock_math import compute_core_math
from core.models import (
    BudgetRow,
    CoreMathResult,
    PlaybookInputs,
    TimingResult,
    TimingStatus,
)


def compute_timing_result(
    inputs: PlaybookInputs,
    core_math: CoreMathResult | None = None,
) -> TimingResult:
    """
    Compute setup and hold timing for a launch-capture flip-flop path.

    Timing model:

        Launch clock edge is taken as 0 ps.

        Capture clock edge:
            CaptureClock = Period + SpatialSkew + UsefulSkew

        Data arrival:
            DataArrival = LogicPathDelay

        Setup slack:
            SetupSlack = CaptureClock - SetupRequirement - DataArrival

        Hold slack:
            HoldSlack = DataArrival - (SpatialSkew + UsefulSkew + HoldRequirement)

    Why this model is useful:
        It clearly demonstrates how useful skew can improve setup
        but can also reduce hold margin for short paths.

    Technical positioning:
        This is a transparent architecture-level timing model.
        Signoff STA requires full library timing, propagated clocks,
        derates, OCV/AOCV/POCV, SI, EMIR, PVT and extracted parasitics.
    """

    if core_math is None:
        core_math = compute_core_math(inputs)

    timing = inputs.timing

    period_ps = core_math.clock_period_ps
    launch_clock_ps = 0.0

    final_effective_skew_ps = (
        timing.spatial_clock_skew_ps + timing.useful_skew_ps
    )

    capture_clock_ps = period_ps + final_effective_skew_ps
    data_arrival_ps = timing.logic_path_delay_ps

    setup_slack_ps = (
        capture_clock_ps
        - timing.setup_requirement_ps
        - data_arrival_ps
    )

    hold_slack_ps = (
        data_arrival_ps
        - (
            final_effective_skew_ps
            + timing.hold_requirement_ps
        )
    )

    status = classify_timing_status(
        setup_slack_ps=setup_slack_ps,
        hold_slack_ps=hold_slack_ps,
    )

    explanation = build_timing_explanation(
        status=status,
        setup_slack_ps=setup_slack_ps,
        hold_slack_ps=hold_slack_ps,
    )

    return TimingResult(
        period_ps=period_ps,
        launch_clock_ps=launch_clock_ps,
        capture_clock_ps=capture_clock_ps,
        data_arrival_ps=data_arrival_ps,
        setup_requirement_ps=timing.setup_requirement_ps,
        hold_requirement_ps=timing.hold_requirement_ps,
        spatial_skew_ps=timing.spatial_clock_skew_ps,
        useful_skew_ps=timing.useful_skew_ps,
        final_effective_skew_ps=final_effective_skew_ps,
        setup_slack_ps=setup_slack_ps,
        hold_slack_ps=hold_slack_ps,
        status=status,
        explanation=explanation,
    )


def classify_timing_status(
    setup_slack_ps: float,
    hold_slack_ps: float,
) -> TimingStatus:
    """
    Convert slack values into a timing status.
    """

    setup_pass = setup_slack_ps >= 0.0
    hold_pass = hold_slack_ps >= 0.0

    if setup_pass and hold_pass:
        return TimingStatus.PASS

    if not setup_pass and hold_pass:
        return TimingStatus.SETUP_VIOLATION

    if setup_pass and not hold_pass:
        return TimingStatus.HOLD_VIOLATION

    return TimingStatus.SETUP_AND_HOLD_RISK


def build_timing_explanation(
    status: TimingStatus,
    setup_slack_ps: float,
    hold_slack_ps: float,
) -> str:
    """
    Human-readable timing explanation for the UI and docs.
    """

    if status == TimingStatus.PASS:
        return (
            f"Timing passes. Setup slack is {setup_slack_ps:.3f} ps "
            f"and hold slack is {hold_slack_ps:.3f} ps. "
            "Both data arrival and clock arrival are currently consistent "
            "with the simplified setup/hold constraints."
        )

    if status == TimingStatus.SETUP_VIOLATION:
        return (
            f"Setup violation detected. Setup slack is {setup_slack_ps:.3f} ps. "
            "The data is arriving too late relative to the capture clock edge. "
            "Possible fixes include reducing logic delay, improving slew, "
            "using useful skew carefully, pipelining, or improving local voltage conditions."
        )

    if status == TimingStatus.HOLD_VIOLATION:
        return (
            f"Hold violation detected. Hold slack is {hold_slack_ps:.3f} ps. "
            "The data is changing too early relative to the hold requirement. "
            "Possible fixes include adding hold buffers, reducing positive useful skew, "
            "or balancing local clock/data paths."
        )

    return (
        f"Combined setup/hold risk detected. Setup slack is {setup_slack_ps:.3f} ps "
        f"and hold slack is {hold_slack_ps:.3f} ps. "
        "This usually indicates that the path requires architectural rebalance, "
        "not only local timing repair."
    )


def build_timing_event_table(result: TimingResult) -> pd.DataFrame:
    """
    Build timing events used by the timing diagram and explanation table.

    This table is intentionally simple and readable:
        Launch edge
        Data arrival
        Capture edge
        Setup deadline
        Hold boundary
    """

    setup_deadline_ps = result.capture_clock_ps - result.setup_requirement_ps
    hold_boundary_ps = result.final_effective_skew_ps + result.hold_requirement_ps

    rows = [
        {
            "Event": "Launch Clock Edge",
            "Time (ps)": result.launch_clock_ps,
            "Meaning": "Reference launch edge where the data path starts.",
        },
        {
            "Event": "Data Arrival",
            "Time (ps)": result.data_arrival_ps,
            "Meaning": "Data reaches the capture flip-flop input.",
        },
        {
            "Event": "Capture Clock Edge",
            "Time (ps)": result.capture_clock_ps,
            "Meaning": "Capture edge where the destination flip-flop samples data.",
        },
        {
            "Event": "Setup Deadline",
            "Time (ps)": setup_deadline_ps,
            "Meaning": "Data must arrive before this time to meet setup.",
        },
        {
            "Event": "Hold Boundary",
            "Time (ps)": hold_boundary_ps,
            "Meaning": "Data should not change before this boundary to meet hold.",
        },
    ]

    return pd.DataFrame(rows)


def build_timing_formula_table(result: TimingResult) -> pd.DataFrame:
    """
    Build formula-by-formula explanation for timing closure.
    """

    rows = [
        {
            "Check": "Clock Period",
            "Formula": "Tclk = 1000 / fGHz",
            "Substitution": f"{result.period_ps:.3f} ps already computed by clock_math",
            "Calculated Value": f"{result.period_ps:.3f} ps",
            "Meaning": "Total time available for one clock cycle.",
        },
        {
            "Check": "Effective Skew",
            "Formula": "EffectiveSkew = SpatialSkew + UsefulSkew",
            "Substitution": (
                f"{result.spatial_skew_ps:.3f} + "
                f"{result.useful_skew_ps:.3f}"
            ),
            "Calculated Value": f"{result.final_effective_skew_ps:.3f} ps",
            "Meaning": "Relative shift between launch and capture clock domains.",
        },
        {
            "Check": "Capture Clock",
            "Formula": "CaptureClock = Period + EffectiveSkew",
            "Substitution": (
                f"{result.period_ps:.3f} + "
                f"{result.final_effective_skew_ps:.3f}"
            ),
            "Calculated Value": f"{result.capture_clock_ps:.3f} ps",
            "Meaning": "Time at which destination flip-flop samples the data.",
        },
        {
            "Check": "Setup Slack",
            "Formula": "SetupSlack = CaptureClock - SetupReq - DataArrival",
            "Substitution": (
                f"{result.capture_clock_ps:.3f} - "
                f"{result.setup_requirement_ps:.3f} - "
                f"{result.data_arrival_ps:.3f}"
            ),
            "Calculated Value": f"{result.setup_slack_ps:.3f} ps",
            "Meaning": "Positive value means data arrives before the setup deadline.",
        },
        {
            "Check": "Hold Slack",
            "Formula": "HoldSlack = DataArrival - (EffectiveSkew + HoldReq)",
            "Substitution": (
                f"{result.data_arrival_ps:.3f} - "
                f"({result.final_effective_skew_ps:.3f} + "
                f"{result.hold_requirement_ps:.3f})"
            ),
            "Calculated Value": f"{result.hold_slack_ps:.3f} ps",
            "Meaning": "Positive value means data does not change too early after launch.",
        },
    ]

    return pd.DataFrame(rows)


def build_timing_margin_budget(
    result: TimingResult,
    core_math: CoreMathResult,
) -> list[BudgetRow]:
    """
    Build a timing-margin budget table.

    This does not modify nominal setup/hold slack.
    It gives a separate uncertainty-aware view for architecture discussion.

    Endpoint jitter is converted from fs to ps:
        jitter_ps = after_total_jitter_fs / 1000

    We keep this separate because the base slack formula should remain
    transparent and easy to verify.
    """

    endpoint_jitter_ps = core_math.after_total_jitter_fs / 1000.0

    uncertainty_aware_setup_margin_ps = (
        result.setup_slack_ps - endpoint_jitter_ps
    )

    uncertainty_aware_hold_margin_ps = (
        result.hold_slack_ps - endpoint_jitter_ps
    )

    return [
        BudgetRow(
            category="Timing Margin",
            component="Nominal Setup Slack",
            value=result.setup_slack_ps,
            unit="ps",
            meaning="Setup slack before subtracting endpoint jitter sensitivity.",
        ),
        BudgetRow(
            category="Timing Margin",
            component="Nominal Hold Slack",
            value=result.hold_slack_ps,
            unit="ps",
            meaning="Hold slack before subtracting endpoint jitter sensitivity.",
        ),
        BudgetRow(
            category="Timing Margin",
            component="Endpoint Jitter Sensitivity",
            value=endpoint_jitter_ps,
            unit="ps",
            meaning="Architecture-level endpoint jitter converted from fs to ps.",
        ),
        BudgetRow(
            category="Timing Margin",
            component="Uncertainty-Aware Setup Margin",
            value=uncertainty_aware_setup_margin_ps,
            unit="ps",
            meaning="Setup margin after subtracting endpoint jitter sensitivity.",
        ),
        BudgetRow(
            category="Timing Margin",
            component="Uncertainty-Aware Hold Margin",
            value=uncertainty_aware_hold_margin_ps,
            unit="ps",
            meaning="Hold margin after subtracting endpoint jitter sensitivity.",
        ),
    ]


def timing_budget_to_dataframe(rows: list[BudgetRow]) -> pd.DataFrame:
    """
    Convert timing budget rows to a UI-friendly DataFrame.
    """

    return pd.DataFrame(
        [
            {
                "Category": row.category,
                "Component": row.component,
                "Value": row.value,
                "Unit": row.unit,
                "Meaning": row.meaning,
            }
            for row in rows
        ]
    )


def build_timing_package(
    inputs: PlaybookInputs,
    core_math: CoreMathResult | None = None,
) -> dict[str, object]:
    """
    Convenience package for UI tabs.

    Returns:
        result:
            TimingResult pydantic model.

        event_table:
            Launch/data/capture/setup/hold event table.

        formula_table:
            Formula-by-formula timing table.

        margin_budget:
            Timing BudgetRow list.

        margin_budget_table:
            DataFrame version of the timing budget.
    """

    if core_math is None:
        core_math = compute_core_math(inputs)

    result = compute_timing_result(inputs, core_math)
    event_table = build_timing_event_table(result)
    formula_table = build_timing_formula_table(result)

    margin_budget = build_timing_margin_budget(result, core_math)
    margin_budget_table = timing_budget_to_dataframe(margin_budget)

    return {
        "result": result,
        "event_table": event_table,
        "formula_table": formula_table,
        "margin_budget": margin_budget,
        "margin_budget_table": margin_budget_table,
    }


__all__ = [
    "build_timing_event_table",
    "build_timing_formula_table",
    "build_timing_margin_budget",
    "build_timing_package",
    "classify_timing_status",
    "compute_timing_result",
    "timing_budget_to_dataframe",
]