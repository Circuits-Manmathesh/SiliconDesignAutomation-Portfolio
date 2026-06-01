from __future__ import annotations

import streamlit as st
from pydantic import ValidationError

from core.models import (
    ClockSourceInputs,
    CrosstalkMode,
    InterconnectInputs,
    PlaybookInputs,
    SiliconModelConstants,
    SiliconNoiseInputs,
    TimingInputs,
    default_ai_soc_5ghz_inputs,
)


def render_sidebar_inputs(
    defaults: PlaybookInputs | None = None,
) -> PlaybookInputs:
    """
    Render the complete Streamlit sidebar and return validated PlaybookInputs.

    This is the only place where user-facing slider controls are defined.

    Flow:
        sidebar sliders
            -> typed input sections
            -> PlaybookInputs
            -> core engines

    Keeping this centralized avoids mismatch between UI labels and model fields.
    """

    if defaults is None:
        defaults = default_ai_soc_5ghz_inputs()

    st.sidebar.title("Clock Architecture Controls")
    st.sidebar.caption(
        "Tune the SoC clock-distribution conditions and observe waveform, "
        "map, timing, budget, and recommendation changes live."
    )

    design_name = st.sidebar.text_input(
        "Design / Demo Name",
        value=defaults.design_name,
        help="Human-readable label used in the dashboard.",
    )

    st.sidebar.divider()

    clock_inputs = _render_clock_source_section(defaults.clock)

    st.sidebar.divider()

    interconnect_inputs = _render_interconnect_section(defaults.interconnect)

    st.sidebar.divider()

    noise_inputs = _render_silicon_noise_section(defaults.noise)

    st.sidebar.divider()

    timing_inputs = _render_timing_section(defaults.timing, clock_inputs.frequency_ghz)

    constants = SiliconModelConstants()

    try:
        return PlaybookInputs(
            design_name=design_name,
            clock=clock_inputs,
            interconnect=interconnect_inputs,
            noise=noise_inputs,
            timing=timing_inputs,
            constants=constants,
        )

    except ValidationError as exc:
        st.sidebar.error("Input validation failed. Please review slider values.")
        st.sidebar.exception(exc)
        return defaults


def _render_clock_source_section(defaults: ClockSourceInputs) -> ClockSourceInputs:
    """
    PLL/source clock controls.

    These controls describe how the clock starts before entering the distribution network.
    """

    st.sidebar.subheader("1. PLL / Clock Source")

    frequency_ghz = st.sidebar.slider(
        "Clock Frequency (GHz)",
        min_value=0.5,
        max_value=12.0,
        value=float(defaults.frequency_ghz),
        step=0.1,
        help=(
            "Main SoC clock frequency. Higher frequency reduces clock period "
            "and makes jitter/skew more critical."
        ),
    )

    pll_random_jitter_fs = st.sidebar.slider(
        "PLL Random Jitter RMS (fs)",
        min_value=0.0,
        max_value=1000.0,
        value=float(defaults.pll_random_jitter_fs),
        step=5.0,
        help=(
            "Source clock edge uncertainty caused by PLL/VCO noise. "
            "This is an architecture-level input, not measured phase-noise integration."
        ),
    )

    pll_duty_cycle_percent = st.sidebar.slider(
        "PLL Duty Cycle (%)",
        min_value=45.0,
        max_value=55.0,
        value=float(defaults.pll_duty_cycle_percent),
        step=0.1,
        help=(
            "Output high-time percentage. 50% is ideal. Deviation represents "
            "duty-cycle distortion caused by asymmetry or conditioning error."
        ),
    )

    return ClockSourceInputs(
        frequency_ghz=frequency_ghz,
        pll_random_jitter_fs=pll_random_jitter_fs,
        pll_duty_cycle_percent=pll_duty_cycle_percent,
    )


def _render_interconnect_section(defaults: InterconnectInputs) -> InterconnectInputs:
    """
    Global clock interconnect and repeater controls.

    These controls determine RC loading, segmentation, and insertion delay.
    """

    st.sidebar.subheader("2. Global Interconnect / CDN")

    global_wire_length_um = st.sidebar.slider(
        "Global Wire Length (µm)",
        min_value=50.0,
        max_value=10000.0,
        value=float(defaults.global_wire_length_um),
        step=50.0,
        help=(
            "Representative global trunk length. Increasing this raises both "
            "wire resistance and capacitance."
        ),
    )

    top_metal_sheet_resistance_mohm_sq = st.sidebar.slider(
        "Top Metal Sheet Resistance (mΩ/sq)",
        min_value=1.0,
        max_value=200.0,
        value=float(defaults.top_metal_sheet_resistance_mohm_sq),
        step=1.0,
        help=(
            "Approximate sheet resistance of the selected global clock metal layer. "
            "Lower value means stronger routing layer."
        ),
    )

    wire_capacitance_af_um = st.sidebar.slider(
        "Wire Capacitance (aF/µm)",
        min_value=1.0,
        max_value=500.0,
        value=float(defaults.wire_capacitance_af_um),
        step=5.0,
        help=(
            "Effective distributed capacitance per micron. Higher value increases load "
            "and slows clock edge transitions."
        ),
    )

    repeater_count = st.sidebar.slider(
        "Repeater / Buffer Count",
        min_value=0,
        max_value=64,
        value=int(defaults.repeater_count),
        step=1,
        help=(
            "Repeaters divide a long RC route into smaller segments. More repeaters "
            "improve slew but add insertion delay and power."
        ),
    )

    return InterconnectInputs(
        global_wire_length_um=global_wire_length_um,
        top_metal_sheet_resistance_mohm_sq=top_metal_sheet_resistance_mohm_sq,
        wire_capacitance_af_um=wire_capacitance_af_um,
        repeater_count=repeater_count,
    )


def _render_silicon_noise_section(defaults: SiliconNoiseInputs) -> SiliconNoiseInputs:
    """
    Real silicon disturbance controls:
        - dynamic VDD droop
        - crosstalk mode
        - shielding/decaps mitigation
    """

    st.sidebar.subheader("3. Real Silicon Enemies")

    dynamic_vdd_droop_mv = st.sidebar.slider(
        "Dynamic VDD Droop (mV)",
        min_value=0.0,
        max_value=200.0,
        value=float(defaults.dynamic_vdd_droop_mv),
        step=1.0,
        help=(
            "Supply droop caused by switching activity. Droop slows clock buffers "
            "and appears as power-supply-induced jitter."
        ),
    )

    crosstalk_mode_label = st.sidebar.selectbox(
        "Crosstalk Aggressor Alignment",
        options=[
            CrosstalkMode.QUIET.value,
            CrosstalkMode.IN_PHASE.value,
            CrosstalkMode.OUT_OF_PHASE.value,
        ],
        index=[
            CrosstalkMode.QUIET.value,
            CrosstalkMode.IN_PHASE.value,
            CrosstalkMode.OUT_OF_PHASE.value,
        ].index(defaults.crosstalk_mode.value),
        help=(
            "Shows how nearby high-toggle aggressor routes can shift the victim clock edge."
        ),
    )

    shielding_decaps_enabled = st.sidebar.toggle(
        "Enable Shielding + Decaps",
        value=bool(defaults.shielding_decaps_enabled),
        help=(
            "Models architectural mitigation: shielding reduces coupling, while decaps "
            "reduce local supply movement."
        ),
    )

    return SiliconNoiseInputs(
        dynamic_vdd_droop_mv=dynamic_vdd_droop_mv,
        crosstalk_mode=CrosstalkMode(crosstalk_mode_label),
        shielding_decaps_enabled=shielding_decaps_enabled,
    )


def _render_timing_section(
    defaults: TimingInputs,
    frequency_ghz: float,
) -> TimingInputs:
    """
    Flip-flop timing controls.

    The logic delay default range is independent of frequency, but the sidebar displays
    the current clock period so the user understands timing pressure.
    """

    st.sidebar.subheader("4. Flip-Flop Timing")

    period_ps = 1000.0 / frequency_ghz

    st.sidebar.metric(
        "Current Clock Period",
        f"{period_ps:.2f} ps",
        help="Tclk = 1000 / frequency(GHz)",
    )

    logic_path_delay_ps = st.sidebar.slider(
        "Logic Path Delay (ps)",
        min_value=0.0,
        max_value=1000.0,
        value=float(defaults.logic_path_delay_ps),
        step=1.0,
        help=(
            "Data path delay from launch flip-flop to capture flip-flop. "
            "Increasing this can create setup violation."
        ),
    )

    spatial_clock_skew_ps = st.sidebar.slider(
        "Spatial Clock Skew (ps)",
        min_value=-200.0,
        max_value=200.0,
        value=float(defaults.spatial_clock_skew_ps),
        step=1.0,
        help=(
            "Clock arrival difference between launch and capture domains caused by "
            "distribution mismatch."
        ),
    )

    useful_skew_ps = st.sidebar.slider(
        "Useful Skew Applied (ps)",
        min_value=-200.0,
        max_value=200.0,
        value=float(defaults.useful_skew_ps),
        step=1.0,
        help=(
            "Intentional capture-clock shift. Positive useful skew can improve setup "
            "but may reduce hold margin."
        ),
    )

    setup_requirement_ps = st.sidebar.slider(
        "Setup Requirement (ps)",
        min_value=0.0,
        max_value=100.0,
        value=float(defaults.setup_requirement_ps),
        step=0.5,
        help=(
            "Minimum time data must be stable before the capture clock edge."
        ),
    )

    hold_requirement_ps = st.sidebar.slider(
        "Hold Requirement (ps)",
        min_value=0.0,
        max_value=100.0,
        value=float(defaults.hold_requirement_ps),
        step=0.5,
        help=(
            "Minimum time data must remain stable after the launch/capture reference."
        ),
    )

    return TimingInputs(
        logic_path_delay_ps=logic_path_delay_ps,
        spatial_clock_skew_ps=spatial_clock_skew_ps,
        useful_skew_ps=useful_skew_ps,
        setup_requirement_ps=setup_requirement_ps,
        hold_requirement_ps=hold_requirement_ps,
    )


def render_sidebar_scope_note() -> None:
    """
    Small sidebar note about model scope.
    """

    st.sidebar.divider()
    st.sidebar.caption(
        "Model scope: architecture-level educational and sensitivity analysis. "
        "Final signoff requires SPEF, Liberty, STA, SI, EMIR, PVT and OCV correlation."
    )


__all__ = [
    "render_sidebar_inputs",
    "render_sidebar_scope_note",
]