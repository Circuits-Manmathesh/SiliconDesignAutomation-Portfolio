from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from core.models import (
    CoreMathResult,
    CrosstalkMode,
    HeatmapResult,
    MathAnalysisRow,
    PlaybookInputs,
    Recommendation,
    TimingResult,
    WaveformResult,
)
from ui.cards import (
    render_architecture_insight,
    render_dataframe_with_note,
    render_explanation_grid,
    render_formula_rows,
    render_intro_panel,
    render_markdown_card,
    render_metric_row,
    render_model_scope_note,
    render_recommendations,
    render_risk_summary,
    render_section_header,
    render_status_metrics_from_timing,
    render_timing_status_banner,
    render_two_column_tables,
)
from ui.plots import (
    plot_clock_waveforms,
    plot_combined_node_dashboard,
    plot_ir_drop_heatmap,
    plot_jitter_budget,
    plot_math_snapshot,
    plot_skew_budget,
    plot_soc_journey_map,
    plot_timing_diagram,
)
from ui.styles import insight_box


def build_jitter_budget_table(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
) -> pd.DataFrame:
    """
    Build jitter budget table from core math.

    This table is used for both chart and dataframe.

    Note:
        This is an architecture-level uncertainty budget.
        It is not final signoff jitter extracted from real STA/SI/EMIR data.
    """

    rows = [
        {
            "Category": "Jitter / Uncertainty",
            "Component": "PLL Random Jitter",
            "Value": inputs.clock.pll_random_jitter_fs,
            "Unit": "fs",
            "Meaning": "Source-clock random edge uncertainty from PLL/VCO behavior.",
        },
        {
            "Category": "Jitter / Uncertainty",
            "Component": "RC Slew Uncertainty",
            "Value": core_math.rc_uncertainty_fs,
            "Unit": "fs",
            "Meaning": "Architecture-level sensitivity term derived from effective segment RC.",
        },
        {
            "Category": "Jitter / Uncertainty",
            "Component": "PSIJ",
            "Value": core_math.psij_jitter_fs,
            "Unit": "fs",
            "Meaning": "Power-supply-induced jitter caused by dynamic VDD droop.",
        },
        {
            "Category": "Jitter / Uncertainty",
            "Component": "Crosstalk",
            "Value": core_math.crosstalk_jitter_fs,
            "Unit": "fs",
            "Meaning": "Clock uncertainty contribution from aggressor coupling alignment.",
        },
        {
            "Category": "Jitter / Uncertainty",
            "Component": "Before Mitigation Total",
            "Value": core_math.before_total_jitter_fs,
            "Unit": "fs",
            "Meaning": "Root-sum-square uncertainty before architecture mitigation.",
        },
        {
            "Category": "Jitter / Uncertainty",
            "Component": "After Mitigation Total",
            "Value": core_math.after_total_jitter_fs,
            "Unit": "fs",
            "Meaning": "Residual endpoint uncertainty after mitigation factor is applied.",
        },
    ]

    return pd.DataFrame(rows)


def build_skew_budget_table(
    inputs: PlaybookInputs,
) -> pd.DataFrame:
    """
    Build skew budget table.

    This table separates spatial skew from useful skew so the user can
    understand the setup/hold tradeoff.
    """

    interconnect = inputs.interconnect
    noise = inputs.noise
    timing = inputs.timing

    trunk_mismatch_ps = 0.0025 * interconnect.global_wire_length_um
    regional_mismatch_ps = 2.5 + 0.25 * interconnect.repeater_count
    local_buffer_mismatch_ps = 1.5 + 0.03 * noise.dynamic_vdd_droop_mv
    final_effective_skew_ps = timing.spatial_clock_skew_ps + timing.useful_skew_ps

    rows = [
        {
            "Category": "Skew",
            "Component": "Trunk Mismatch",
            "Value": trunk_mismatch_ps,
            "Unit": "ps",
            "Meaning": "Architecture-level mismatch trend for the global trunk.",
        },
        {
            "Category": "Skew",
            "Component": "Regional Mismatch",
            "Value": regional_mismatch_ps,
            "Unit": "ps",
            "Meaning": "Mismatch trend from regional clock distribution and buffers.",
        },
        {
            "Category": "Skew",
            "Component": "Local Buffer Mismatch",
            "Value": local_buffer_mismatch_ps,
            "Unit": "ps",
            "Meaning": "Local leaf-buffer mismatch and droop sensitivity term.",
        },
        {
            "Category": "Skew",
            "Component": "Spatial Clock Skew",
            "Value": timing.spatial_clock_skew_ps,
            "Unit": "ps",
            "Meaning": "User-controlled launch/capture spatial skew.",
        },
        {
            "Category": "Skew",
            "Component": "Useful Skew",
            "Value": timing.useful_skew_ps,
            "Unit": "ps",
            "Meaning": "Intentional skew applied to trade setup and hold margin.",
        },
        {
            "Category": "Skew",
            "Component": "Final Effective Skew",
            "Value": final_effective_skew_ps,
            "Unit": "ps",
            "Meaning": "Spatial skew plus useful skew used by the timing engine.",
        },
    ]

    return pd.DataFrame(rows)


def build_math_analysis_rows(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
    timing: TimingResult,
) -> list[MathAnalysisRow]:
    """
    Build formula-by-formula math explanation rows.

    These rows are displayed in the Live Math Analysis tab.
    They make waveform and timing changes traceable.
    """

    clock = inputs.clock
    interconnect = inputs.interconnect
    noise = inputs.noise

    rows = [
        MathAnalysisRow(
            section="Clock Period",
            formula="Tclk = 1000 / fGHz",
            substitution=f"1000 / {clock.frequency_ghz:.3f}",
            calculated_value=f"{core_math.clock_period_ps:.3f} ps",
            physical_meaning="Total time available for one clock cycle.",
            risk_or_action="Higher frequency reduces available timing margin.",
        ),
        MathAnalysisRow(
            section="Duty-Cycle Error",
            formula="DCD = |Duty - 50%|",
            substitution=f"|{clock.pll_duty_cycle_percent:.3f} - 50|",
            calculated_value=f"{core_math.duty_cycle_error_percent:.3f} %",
            physical_meaning="Deviation from ideal 50% high/low clock symmetry.",
            risk_or_action="Review duty-cycle correction if DCD becomes large.",
        ),
        MathAnalysisRow(
            section="Wire Squares",
            formula="Squares = WireLength / WireWidth",
            substitution=(
                f"{interconnect.global_wire_length_um:.3f} / "
                f"{core_math.wire_width_um:.3f}"
            ),
            calculated_value=f"{core_math.wire_squares:.3f}",
            physical_meaning="Longer/narrower wires have more sheet-resistance squares.",
            risk_or_action="Use wider top metal or split long clock trunks.",
        ),
        MathAnalysisRow(
            section="Wire Resistance",
            formula="Rwire = Rsheet × Squares",
            substitution=(
                f"{interconnect.top_metal_sheet_resistance_mohm_sq:.3f} mΩ/sq × "
                f"{core_math.wire_squares:.3f}"
            ),
            calculated_value=f"{core_math.wire_resistance_ohm:.3f} Ω",
            physical_meaning="Resistance limits edge charging/discharging current.",
            risk_or_action="Reduce resistance using wider/stronger top metal routing.",
        ),
        MathAnalysisRow(
            section="Wire Capacitance",
            formula="Cwire = Cper_um × WireLength",
            substitution=(
                f"{interconnect.wire_capacitance_af_um:.3f} aF/µm × "
                f"{interconnect.global_wire_length_um:.3f} µm"
            ),
            calculated_value=f"{core_math.wire_capacitance_ff:.3f} fF",
            physical_meaning="Capacitance is the load that the clock network must charge.",
            risk_or_action="Reduce unnecessary loading and optimize routing/layer choice.",
        ),
        MathAnalysisRow(
            section="Total RC Tau",
            formula="τRC = Rwire × Cwire",
            substitution=(
                f"{core_math.wire_resistance_ohm:.3f} Ω × "
                f"{core_math.wire_capacitance_ff:.3f} fF"
            ),
            calculated_value=f"{core_math.total_rc_tau_ps:.3f} ps",
            physical_meaning="Unbuffered RC severity indicator for the global route.",
            risk_or_action="Use segment RC for practical buffered-clock interpretation.",
        ),
        MathAnalysisRow(
            section="Segment RC Tau",
            formula="τsegment = τRC / (Nrepeaters + 1)²",
            substitution=(
                f"{core_math.total_rc_tau_ps:.3f} / "
                f"({interconnect.repeater_count} + 1)²"
            ),
            calculated_value=f"{core_math.segment_rc_tau_ps:.3f} ps",
            physical_meaning="Effective RC severity per buffered segment.",
            risk_or_action="Increase repeaters or shorten segments if this becomes large.",
        ),
        MathAnalysisRow(
            section="Insertion Delay",
            formula="Delayinsert = Nrepeaters × BufferDelay",
            substitution=(
                f"{interconnect.repeater_count} × "
                f"{inputs.constants.buffer_delay_ps:.3f}"
            ),
            calculated_value=f"{core_math.insertion_delay_ps:.3f} ps",
            physical_meaning="Latency added by clock repeaters/buffers.",
            risk_or_action="Balance slew recovery against insertion delay and power.",
        ),
        MathAnalysisRow(
            section="Before Slew",
            formula="Slewbefore = BaseSlew + k × τsegment",
            substitution=(
                f"{inputs.constants.base_slew_ps:.3f} + "
                f"{inputs.constants.rc_slew_gain:.3f} × "
                f"{core_math.segment_rc_tau_ps:.3f}"
            ),
            calculated_value=f"{core_math.before_slew_ps:.3f} ps",
            physical_meaning="Clock edge transition time before mitigation.",
            risk_or_action="Large slew means edge is slow and more noise-sensitive.",
        ),
        MathAnalysisRow(
            section="After Slew",
            formula="Slewafter = max(BaseSlew, Slewbefore × MitigationFactor)",
            substitution=(
                f"max({inputs.constants.base_slew_ps:.3f}, "
                f"{core_math.before_slew_ps:.3f} × "
                f"{core_math.mitigation_factor:.3f})"
            ),
            calculated_value=f"{core_math.after_slew_ps:.3f} ps",
            physical_meaning="Residual edge slew after mitigation.",
            risk_or_action="Use mitigation and segmentation to restore clock edge quality.",
        ),
        MathAnalysisRow(
            section="PSIJ Shift",
            formula="ΔtPSIJ = kdroop × Vdroop",
            substitution=(
                f"{inputs.constants.psij_delay_coeff_ps_per_mv:.4f} × "
                f"{noise.dynamic_vdd_droop_mv:.3f}"
            ),
            calculated_value=f"{core_math.psij_edge_shift_ps:.3f} ps",
            physical_meaning="Clock edge movement caused by supply droop.",
            risk_or_action="Use decaps, stronger power grid, and placement-aware clock buffers.",
        ),
        MathAnalysisRow(
            section="Crosstalk Shift",
            formula="ΔtXTALK = alignment-dependent shift",
            substitution=f"Mode = {noise.crosstalk_mode.value}",
            calculated_value=f"{core_math.crosstalk_edge_shift_ps:.3f} ps",
            physical_meaning="Aggressor nets can shift clock edge timing.",
            risk_or_action="Use shielding, spacing, and SI-aware routing.",
        ),
        MathAnalysisRow(
            section="Total Jitter Before Fix",
            formula="Jtotal = sqrt(Jpll² + Jrc² + Jpsij² + Jxtalk²)",
            substitution=(
                f"sqrt({clock.pll_random_jitter_fs:.3f}² + "
                f"{core_math.rc_uncertainty_fs:.3f}² + "
                f"{core_math.psij_jitter_fs:.3f}² + "
                f"{core_math.crosstalk_jitter_fs:.3f}²)"
            ),
            calculated_value=f"{core_math.before_total_jitter_fs:.3f} fs",
            physical_meaning="Architecture-level endpoint uncertainty before mitigation.",
            risk_or_action="Identify dominant uncertainty contributor and optimize first.",
        ),
        MathAnalysisRow(
            section="Total Jitter After Fix",
            formula="Jafter = Jbefore × MitigationFactor",
            substitution=(
                f"{core_math.before_total_jitter_fs:.3f} × "
                f"{core_math.mitigation_factor:.3f}"
            ),
            calculated_value=f"{core_math.after_total_jitter_fs:.3f} fs",
            physical_meaning="Residual endpoint uncertainty after mitigation.",
            risk_or_action="Use before/after comparison to justify architecture fixes.",
        ),
        MathAnalysisRow(
            section="Setup Slack",
            formula="SetupSlack = CaptureClock - SetupReq - DataArrival",
            substitution=(
                f"{timing.capture_clock_ps:.3f} - "
                f"{timing.setup_requirement_ps:.3f} - "
                f"{timing.data_arrival_ps:.3f}"
            ),
            calculated_value=f"{timing.setup_slack_ps:.3f} ps",
            physical_meaning="Positive value means data arrives before setup deadline.",
            risk_or_action="Negative setup needs faster data path, useful skew, or pipelining.",
        ),
        MathAnalysisRow(
            section="Hold Slack",
            formula="HoldSlack = DataArrival - (EffectiveSkew + HoldReq)",
            substitution=(
                f"{timing.data_arrival_ps:.3f} - "
                f"({timing.final_effective_skew_ps:.3f} + "
                f"{timing.hold_requirement_ps:.3f})"
            ),
            calculated_value=f"{timing.hold_slack_ps:.3f} ps",
            physical_meaning="Positive value means data does not change too early.",
            risk_or_action="Negative hold needs hold buffers or reduced useful skew.",
        ),
    ]

    return rows


def build_math_analysis_table(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
    timing: TimingResult,
) -> pd.DataFrame:
    """
    Convert math analysis rows into a DataFrame.
    """

    rows = build_math_analysis_rows(inputs, core_math, timing)

    return pd.DataFrame(
        [
            {
                "Section": row.section,
                "Formula": row.formula,
                "Substitution": row.substitution,
                "Calculated Value": row.calculated_value,
                "Physical Meaning": row.physical_meaning,
                "Risk / Action": row.risk_or_action,
            }
            for row in rows
        ]
    )


def build_ir_drop_heatmap(
    inputs: PlaybookInputs,
    node_table: pd.DataFrame,
    grid_size: int = 70,
) -> HeatmapResult:
    """
    Build synthetic IR-drop heatmap for visualization.

    This uses normalized SoC coordinates.
    It is not an extracted EMIR map.

    The goal:
        show how local switching hotspots can overlap with clock path.
    """

    x_axis = np.linspace(0.0, 1.0, grid_size)
    y_axis = np.linspace(0.0, 1.0, grid_size)
    xx, yy = np.meshgrid(x_axis, y_axis)

    droop_mv = inputs.noise.dynamic_vdd_droop_mv
    mitigation = (
        inputs.constants.shielded_mitigation_factor
        if inputs.noise.shielding_decaps_enabled
        else inputs.constants.unshielded_mitigation_factor
    )

    # Synthetic hotspots placed near regional and local areas.
    # These match the visual concept of high-activity AI compute regions.
    regional_hotspot = np.exp(-((xx - 0.66) ** 2 + (yy - 0.68) ** 2) / 0.020)
    local_hotspot = 0.80 * np.exp(-((xx - 0.82) ** 2 + (yy - 0.42) ** 2) / 0.018)
    trunk_gradient = 0.18 * xx

    droop_grid = droop_mv * mitigation * (
        regional_hotspot + local_hotspot + trunk_gradient
    )

    return HeatmapResult(
        x_axis=x_axis.tolist(),
        y_axis=y_axis.tolist(),
        droop_grid_mv=droop_grid.tolist(),
        clock_path_x=node_table["x"].astype(float).tolist(),
        clock_path_y=node_table["y"].astype(float).tolist(),
    )


def render_playbook_tabs(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
    waveform: WaveformResult,
    soc_package: dict[str, object],
    timing_package: dict[str, object],
    recommendation_package: dict[str, object],
) -> None:
    """
    Render all application tabs.

    This is the main UI orchestration function used by app.py.
    """

    timing_result = timing_package["result"]
    node_table = soc_package["node_table"]
    edge_table = soc_package["edge_table"]
    recommendation_table = recommendation_package["table"]
    recommendations = recommendation_package["recommendations"]

    jitter_budget_table = build_jitter_budget_table(inputs, core_math)
    skew_budget_table = build_skew_budget_table(inputs)
    math_analysis_table = build_math_analysis_table(inputs, core_math, timing_result)
    heatmap = build_ir_drop_heatmap(inputs, node_table)

    tabs = st.tabs(
        [
            "1. Overview",
            "2. SoC Journey Map",
            "3. Waveform Lab",
            "4. Live Math",
            "5. Jitter / Skew Budget",
            "6. IR-Drop / Crosstalk",
            "7. Timing Closure",
            "8. Recommendations",
        ]
    )

    with tabs[0]:
        render_overview_tab(inputs, core_math, timing_result)

    with tabs[1]:
        render_soc_journey_tab(node_table, edge_table)

    with tabs[2]:
        render_waveform_tab(waveform, core_math)

    with tabs[3]:
        render_live_math_tab(math_analysis_table)

    with tabs[4]:
        render_budget_tab(
            jitter_budget_table=jitter_budget_table,
            skew_budget_table=skew_budget_table,
            timing_margin_table=timing_package["margin_budget_table"],
        )

    with tabs[5]:
        render_ir_drop_tab(inputs, core_math, heatmap)

    with tabs[6]:
        render_timing_closure_tab(timing_result, timing_package)

    with tabs[7]:
        render_recommendation_tab(recommendations, recommendation_table)


def render_overview_tab(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
    timing: TimingResult,
) -> None:
    """
    Render project overview tab.
    """

    render_section_header(
        "Project Overview",
        "PLL-to-flip-flop interactive clock-distribution review.",
    )

    render_intro_panel()

    render_metric_row(
        [
            ("Design", inputs.design_name),
            ("Clock Frequency", f"{inputs.clock.frequency_ghz:.2f} GHz"),
            ("Clock Period", f"{core_math.clock_period_ps:.3f} ps"),
            ("Timing Status", timing.status.value),
        ],
        columns=4,
    )

    render_explanation_grid(
        [
            (
                "What this playbook shows",
                "It follows the clock from PLL to divider, global trunk, regional branch, local leaf, and final flip-flop capture.",
            ),
            (
                "Why it matters",
                "A modern SoC clock is an analog timing signal. It accumulates jitter, skew, RC delay, IR-drop sensitivity, and crosstalk effects.",
            ),
            (
                "How to use it",
                "Change sidebar sliders and observe how the waveform, node map, budgets, timing diagram, formulas, and recommendations update together.",
            ),
            (
                "Technical scope",
                "This is an architecture-level sensitivity model for learning and early review. It is not a replacement for signoff STA/SI/EMIR tools.",
            ),
        ],
        columns=2,
    )

    render_architecture_insight(
        observation=(
            f"At {inputs.clock.frequency_ghz:.2f} GHz, the clock period is "
            f"{core_math.clock_period_ps:.3f} ps."
        ),
        physical_cause=(
            "As frequency increases, the cycle time shrinks and small edge movements become significant."
        ),
        architecture_action=(
            "Track jitter, skew, slew, IR-drop, crosstalk, setup and hold as a connected architecture budget."
        ),
    )

    render_model_scope_note()


def render_soc_journey_tab(
    node_table: pd.DataFrame,
    edge_table: pd.DataFrame,
) -> None:
    """
    Render SoC journey map tab.
    """

    render_section_header(
        "SoC Clock Journey Map",
        "Normalized PLL-to-flip-flop view of clock quality evolution.",
    )

    st.plotly_chart(
        plot_soc_journey_map(node_table),
        use_container_width=True,
    )

    st.plotly_chart(
        plot_combined_node_dashboard(node_table),
        use_container_width=True,
    )

    render_two_column_tables(
        left_title="Live Per-Node Clock Quality",
        left_df=node_table,
        right_title="Logical Clock Path Edges",
        right_df=edge_table,
        left_note=(
            "Coordinates are normalized visualization coordinates, not physical micron coordinates."
        ),
        right_note=(
            "The edge table shows the conceptual PLL-to-flip-flop clock journey."
        ),
    )

    render_architecture_insight(
        observation="Clock quality changes stage by stage from PLL to flip-flop.",
        physical_cause=(
            "Each stage adds delay, jitter, skew, droop sensitivity, or slew degradation."
        ),
        architecture_action=(
            "Use node-level visibility to identify where clock quality starts degrading."
        ),
    )


def render_waveform_tab(
    waveform: WaveformResult,
    core_math: CoreMathResult,
) -> None:
    """
    Render waveform lab tab.
    """

    render_section_header(
        "Waveform Lab",
        "Equation-driven ideal, degraded, and mitigated clock waveforms.",
    )

    st.plotly_chart(
        plot_clock_waveforms(waveform),
        use_container_width=True,
    )

    render_metric_row(
        [
            ("Before Slew", f"{core_math.before_slew_ps:.3f} ps"),
            ("After Slew", f"{core_math.after_slew_ps:.3f} ps"),
            ("Before Jitter", f"{core_math.before_total_jitter_fs:.3f} fs"),
            ("After Jitter", f"{core_math.after_total_jitter_fs:.3f} fs"),
            ("DCD", f"{core_math.duty_cycle_error_percent:.3f} %"),
        ],
        columns=5,
    )

    render_architecture_insight(
        observation="The degraded waveform shifts and slows relative to the ideal reference.",
        physical_cause=(
            "PLL jitter, duty-cycle distortion, RC slew degradation, PSIJ, crosstalk and insertion delay move the clock edge."
        ),
        architecture_action=(
            "Improve edge quality using repeater optimization, top-metal routing, shielding, decaps and duty-cycle conditioning."
        ),
    )


def render_live_math_tab(
    math_analysis_table: pd.DataFrame,
) -> None:
    """
    Render live math analysis tab.
    """

    render_section_header(
        "Live Math Analysis",
        "Formula, substitution, calculated value, physical meaning and action.",
    )

    st.plotly_chart(
        plot_math_snapshot(math_analysis_table),
        use_container_width=True,
    )

    render_dataframe_with_note(
        math_analysis_table,
        note=(
            "Every row connects a visible app behavior to a transparent architecture-level formula."
        ),
        height=560,
    )

    selected_section = st.selectbox(
        "Inspect one calculation deeply",
        options=math_analysis_table["Section"].tolist(),
    )

    selected_row = math_analysis_table[
        math_analysis_table["Section"] == selected_section
    ].iloc[0]

    row_obj = MathAnalysisRow(
        section=selected_row["Section"],
        formula=selected_row["Formula"],
        substitution=selected_row["Substitution"],
        calculated_value=selected_row["Calculated Value"],
        physical_meaning=selected_row["Physical Meaning"],
        risk_or_action=selected_row["Risk / Action"],
    )

    render_formula_rows([row_obj])


def render_budget_tab(
    jitter_budget_table: pd.DataFrame,
    skew_budget_table: pd.DataFrame,
    timing_margin_table: pd.DataFrame,
) -> None:
    """
    Render jitter/skew/timing budget tab.
    """

    render_section_header(
        "Jitter / Skew / Timing Budget",
        "Budget decomposition for clock uncertainty, skew and timing margin.",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            plot_jitter_budget(jitter_budget_table),
            use_container_width=True,
        )
        render_dataframe_with_note(
            jitter_budget_table,
            note="Jitter values are architecture-level sensitivity terms.",
            height=320,
        )

    with col2:
        st.plotly_chart(
            plot_skew_budget(skew_budget_table),
            use_container_width=True,
        )
        render_dataframe_with_note(
            skew_budget_table,
            note="Skew separates spatial mismatch and intentional useful skew.",
            height=320,
        )

    st.subheader("Timing Margin Budget")
    render_dataframe_with_note(
        timing_margin_table,
        note=(
            "Nominal setup/hold slack is shown separately from endpoint jitter sensitivity."
        ),
        height=300,
    )

    render_architecture_insight(
        observation="Final clock uncertainty is not created by one source.",
        physical_cause=(
            "PLL jitter, RC slew uncertainty, PSIJ, crosstalk and skew terms combine into endpoint risk."
        ),
        architecture_action=(
            "Break the problem into budgets and optimize the dominant contributor first."
        ),
    )


def render_ir_drop_tab(
    inputs: PlaybookInputs,
    core_math: CoreMathResult,
    heatmap: HeatmapResult,
) -> None:
    """
    Render IR-drop and crosstalk awareness tab.
    """

    render_section_header(
        "IR-Drop / Crosstalk Awareness",
        "Visualizing how power and coupling effects move clock edges.",
    )

    st.plotly_chart(
        plot_ir_drop_heatmap(heatmap),
        use_container_width=True,
    )

    render_metric_row(
        [
            ("Dynamic VDD Droop", f"{inputs.noise.dynamic_vdd_droop_mv:.3f} mV"),
            ("PSIJ Edge Shift", f"{core_math.psij_edge_shift_ps:.3f} ps"),
            ("Crosstalk Mode", inputs.noise.crosstalk_mode.value),
            ("Crosstalk Shift", f"{core_math.crosstalk_edge_shift_ps:.3f} ps"),
            (
                "Shielding + Decaps",
                "ON" if inputs.noise.shielding_decaps_enabled else "OFF",
            ),
        ],
        columns=5,
    )

    if inputs.noise.crosstalk_mode == CrosstalkMode.QUIET:
        xtalk_observation = "Crosstalk is currently quiet or orthogonal."
    else:
        xtalk_observation = (
            f"Crosstalk is active in {inputs.noise.crosstalk_mode.value} mode."
        )

    render_architecture_insight(
        observation=(
            f"Dynamic droop creates {core_math.psij_edge_shift_ps:.3f} ps PSIJ shift. "
            f"{xtalk_observation}"
        ),
        physical_cause=(
            "VDD droop slows clock buffers, while nearby aggressor nets can inject coupling noise into the clock route."
        ),
        architecture_action=(
            "Use decaps, stronger power grid, shielding, spacing and activity-aware clock-buffer placement."
        ),
        note=(
            "The heatmap is synthetic and normalized. It is intended to explain the concept, not replace extracted EMIR maps."
        ),
    )


def render_timing_closure_tab(
    timing_result: TimingResult,
    timing_package: dict[str, object],
) -> None:
    """
    Render setup/hold timing closure tab.
    """

    render_section_header(
        "Setup / Hold Timing Closure",
        "Final flip-flop capture analysis with useful-skew tradeoff.",
    )

    render_status_metrics_from_timing(timing_result)
    render_timing_status_banner(timing_result)

    st.plotly_chart(
        plot_timing_diagram(timing_result),
        use_container_width=True,
    )

    render_two_column_tables(
        left_title="Timing Events",
        left_df=timing_package["event_table"],
        right_title="Timing Formulas",
        right_df=timing_package["formula_table"],
        left_note="Launch, data, capture, setup deadline and hold boundary.",
        right_note="Transparent setup/hold equations used by the playbook.",
    )

    render_architecture_insight(
        observation=timing_result.explanation,
        physical_cause=(
            "Capture clock position relative to data arrival determines setup and hold margin."
        ),
        architecture_action=(
            "Use useful skew carefully. It can improve setup but may reduce hold margin on short paths."
        ),
    )


def render_recommendation_tab(
    recommendations: list[Recommendation],
    recommendation_table: pd.DataFrame,
) -> None:
    """
    Render architecture recommendations tab.
    """

    render_section_header(
        "Architecture Recommendations",
        "Rule-based design actions generated from current clock-distribution state.",
    )

    render_recommendations(recommendations)

    st.subheader("Recommendation Table")
    render_dataframe_with_note(
        recommendation_table,
        note="Each recommendation is generated from live parameter values and timing status.",
        height=420,
    )

    render_markdown_card(
        insight_box(
            "<b>How to use this tab:</b><br>"
            "Use recommendations as architecture-review guidance. "
            "If a risk appears, go back to the relevant slider and observe how waveform, math, budget and timing respond."
        )
    )


__all__ = [
    "build_ir_drop_heatmap",
    "build_jitter_budget_table",
    "build_math_analysis_rows",
    "build_math_analysis_table",
    "build_skew_budget_table",
    "render_playbook_tabs",
]