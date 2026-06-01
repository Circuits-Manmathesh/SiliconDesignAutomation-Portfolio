from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from core.models import BudgetRow, HeatmapResult, TimingResult, WaveformResult


PLOT_TEMPLATE = "plotly_dark"
PAPER_BG = "#070b16"
PLOT_BG = "#0f172a"
FONT_COLOR = "#e5e7eb"
GRID_COLOR = "rgba(255,255,255,0.08)"


def apply_engineering_layout(
    fig: go.Figure,
    title: str,
    height: int = 520,
    x_title: str | None = None,
    y_title: str | None = None,
    show_legend: bool = True,
) -> go.Figure:
    """
    Apply a consistent dark engineering dashboard layout.

    This keeps all charts visually aligned across the app.
    """

    fig.update_layout(
        template=PLOT_TEMPLATE,
        title=dict(
            text=title,
            x=0.02,
            font=dict(size=22, color="#f8fafc"),
        ),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(
            family="Inter, Segoe UI, Arial, sans-serif",
            size=13,
            color=FONT_COLOR,
        ),
        margin=dict(l=45, r=25, t=78, b=48),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zeroline=False,
        title=x_title,
    )

    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zeroline=False,
        title=y_title,
    )

    return fig


def plot_clock_waveforms(waveform: WaveformResult) -> go.Figure:
    """
    Plot ideal, degraded, and mitigated clock waveforms.

    This is the main visual proof that slider-controlled parameters
    affect clock edge quality, shift, and shape.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=waveform.time_ps,
            y=waveform.ideal_clock_v,
            mode="lines",
            name="Ideal Clock",
            line=dict(width=2),
            hovertemplate="Time=%{x:.3f} ps<br>V=%{y:.3f} V<extra>Ideal</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=waveform.time_ps,
            y=waveform.degraded_clock_v,
            mode="lines",
            name="Degraded Clock",
            line=dict(width=3),
            hovertemplate="Time=%{x:.3f} ps<br>V=%{y:.3f} V<extra>Degraded</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=waveform.time_ps,
            y=waveform.mitigated_clock_v,
            mode="lines",
            name="Mitigated Clock",
            line=dict(width=3, dash="dash"),
            hovertemplate="Time=%{x:.3f} ps<br>V=%{y:.3f} V<extra>Mitigated</extra>",
        )
    )

    return apply_engineering_layout(
        fig,
        title="Clock Waveform Lab — Ideal vs Degraded vs Mitigated",
        height=560,
        x_title="Time (ps)",
        y_title="Voltage (V)",
    )


def plot_soc_journey_map(node_table: pd.DataFrame) -> go.Figure:
    """
    Plot the PLL-to-flip-flop journey map.

    Required columns:
        Node
        x
        y
        Accum Delay (ps)
        Jitter RMS (fs)
        Local Skew (ps)
        VDD Droop (mV)
        Slew (ps)
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=node_table["x"],
            y=node_table["y"],
            mode="lines+markers+text",
            text=node_table["Node"],
            textposition="top center",
            marker=dict(
                size=20,
                color=node_table["Jitter RMS (fs)"],
                colorscale="Turbo",
                showscale=True,
                colorbar=dict(title="Jitter fs"),
                line=dict(width=1, color="rgba(255,255,255,0.75)"),
            ),
            line=dict(width=5),
            customdata=node_table[
                [
                    "Accum Delay (ps)",
                    "Jitter RMS (fs)",
                    "Local Skew (ps)",
                    "VDD Droop (mV)",
                    "Slew (ps)",
                ]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Accum Delay: %{customdata[0]:.3f} ps<br>"
                "Jitter: %{customdata[1]:.3f} fs<br>"
                "Local Skew: %{customdata[2]:.3f} ps<br>"
                "VDD Droop: %{customdata[3]:.3f} mV<br>"
                "Slew: %{customdata[4]:.3f} ps<br>"
                "<extra></extra>"
            ),
            name="Clock Path",
        )
    )

    fig.update_xaxes(
        range=[0.0, 1.0],
        tickvals=[0, 0.25, 0.5, 0.75, 1.0],
    )

    fig.update_yaxes(
        range=[0.20, 0.85],
        tickvals=[0.25, 0.50, 0.75],
    )

    return apply_engineering_layout(
        fig,
        title="SoC Clock Journey Map — PLL to Flip-Flop",
        height=560,
        x_title="Normalized SoC X",
        y_title="Normalized SoC Y",
    )


def budget_rows_to_dataframe(rows: Sequence[BudgetRow]) -> pd.DataFrame:
    """
    Convert BudgetRow objects to DataFrame.

    This function is useful because some engines may return BudgetRow list
    while UI tabs may prefer DataFrames.
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


def plot_budget_bar(
    budget: pd.DataFrame | Sequence[BudgetRow],
    title: str,
    value_column: str = "Value",
    label_column: str = "Component",
    unit_column: str = "Unit",
    height: int = 500,
) -> go.Figure:
    """
    Generic budget bar chart.

    Works for:
        jitter budget
        skew budget
        timing margin budget
        delay budget
    """

    if not isinstance(budget, pd.DataFrame):
        df = budget_rows_to_dataframe(budget)
    else:
        df = budget.copy()

    if df.empty:
        fig = go.Figure()
        return apply_engineering_layout(
            fig,
            title=title,
            height=height,
            show_legend=False,
        )

    fig = go.Figure()

    text_values = [
        f"{value:.3f} {unit}"
        for value, unit in zip(df[value_column], df[unit_column])
    ]

    fig.add_trace(
        go.Bar(
            x=df[label_column],
            y=df[value_column],
            text=text_values,
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Value=%{y:.4f}<br>"
                "<extra></extra>"
            ),
            name="Budget",
        )
    )

    y_unit = str(df[unit_column].iloc[0]) if unit_column in df.columns else ""

    fig.update_xaxes(tickangle=-20)

    return apply_engineering_layout(
        fig,
        title=title,
        height=height,
        x_title="Component",
        y_title=y_unit,
        show_legend=False,
    )


def plot_jitter_budget(budget: pd.DataFrame | Sequence[BudgetRow]) -> go.Figure:
    """
    Dedicated jitter budget plot wrapper.
    """

    return plot_budget_bar(
        budget=budget,
        title="Jitter Budget — Source-to-Endpoint Uncertainty",
        height=500,
    )


def plot_skew_budget(budget: pd.DataFrame | Sequence[BudgetRow]) -> go.Figure:
    """
    Dedicated skew budget plot wrapper.
    """

    return plot_budget_bar(
        budget=budget,
        title="Skew Budget — Spatial and Useful Skew Contributions",
        height=500,
    )


def plot_ir_drop_heatmap(heatmap: HeatmapResult) -> go.Figure:
    """
    Plot dynamic IR-drop heatmap with clock path overlay.

    HeatmapResult will be generated later by the IR-drop/noise engine.
    This function is defined now so the UI architecture is ready.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            x=heatmap.x_axis,
            y=heatmap.y_axis,
            z=heatmap.droop_grid_mv,
            colorscale="Turbo",
            colorbar=dict(title="Droop mV"),
            name="VDD Droop",
            hovertemplate="X=%{x:.3f}<br>Y=%{y:.3f}<br>Droop=%{z:.3f} mV<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=heatmap.clock_path_x,
            y=heatmap.clock_path_y,
            mode="lines+markers",
            name="Clock Path",
            line=dict(width=5, color="white"),
            marker=dict(size=10, color="white"),
            hovertemplate="Clock Path<br>X=%{x:.3f}<br>Y=%{y:.3f}<extra></extra>",
        )
    )

    fig.update_xaxes(range=[0.0, 1.0])
    fig.update_yaxes(range=[0.0, 1.0])

    return apply_engineering_layout(
        fig,
        title="Dynamic IR-Drop Heatmap with Clock Path Overlay",
        height=560,
        x_title="Normalized SoC X",
        y_title="Normalized SoC Y",
    )


def plot_timing_diagram(result: TimingResult) -> go.Figure:
    """
    Plot launch clock, data arrival, capture clock, setup window and hold boundary.

    This diagram visually explains:
        - how useful skew moves capture edge
        - how setup slack is created or lost
        - how hold boundary can be violated on short paths
    """

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(
            "Launch Clock",
            "Data Path",
            "Capture Clock + Setup/Hold Windows",
        ),
    )

    def add_clock_pulse(row: int, center_ps: float, label: str) -> None:
        fig.add_trace(
            go.Scatter(
                x=[center_ps - 6, center_ps, center_ps + 6, center_ps + 22],
                y=[0.0, 1.0, 0.0, 0.0],
                mode="lines",
                name=label,
                line=dict(width=3),
                hovertemplate=f"{label}<br>Time=%{{x:.3f}} ps<extra></extra>",
            ),
            row=row,
            col=1,
        )

    add_clock_pulse(1, result.launch_clock_ps, "Launch Edge")
    add_clock_pulse(3, result.capture_clock_ps, "Capture Edge")

    fig.add_trace(
        go.Scatter(
            x=[result.launch_clock_ps, result.data_arrival_ps],
            y=[0.5, 0.5],
            mode="lines+markers",
            name="Logic Path Delay",
            line=dict(width=5),
            marker=dict(size=8),
            hovertemplate="Time=%{x:.3f} ps<extra>Data Path</extra>",
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=[result.data_arrival_ps, result.data_arrival_ps],
            y=[0.0, 1.0],
            mode="lines",
            name="Data Arrival",
            line=dict(width=3, dash="dash"),
            hovertemplate="Data Arrival=%{x:.3f} ps<extra></extra>",
        ),
        row=3,
        col=1,
    )

    setup_deadline_ps = result.capture_clock_ps - result.setup_requirement_ps
    hold_boundary_start_ps = result.final_effective_skew_ps
    hold_boundary_end_ps = result.final_effective_skew_ps + result.hold_requirement_ps

    fig.add_vrect(
        x0=setup_deadline_ps,
        x1=result.capture_clock_ps,
        fillcolor="rgba(245, 158, 11, 0.25)",
        line_width=0,
        annotation_text="Setup Window",
        annotation_position="top left",
        row=3,
        col=1,
    )

    fig.add_vrect(
        x0=hold_boundary_start_ps,
        x1=hold_boundary_end_ps,
        fillcolor="rgba(244, 63, 94, 0.25)",
        line_width=0,
        annotation_text="Hold Window",
        annotation_position="bottom left",
        row=3,
        col=1,
    )

    x_max = max(
        result.period_ps + 80.0,
        result.capture_clock_ps + 80.0,
        result.data_arrival_ps + 80.0,
        hold_boundary_end_ps + 80.0,
    )

    fig.update_xaxes(
        range=[-30.0, x_max],
        title="Time (ps)",
        row=3,
        col=1,
    )

    fig.update_yaxes(showticklabels=False, range=[-0.1, 1.2])

    return apply_engineering_layout(
        fig,
        title=f"Timing Closure Diagram — {result.status.value}",
        height=720,
        show_legend=True,
    )


def _extract_first_numeric_value(text: str) -> float:
    """
    Extract first numeric value from a calculated value string.

    Examples:
        "200.000 ps" -> 200.0
        "1.500 %" -> 1.5

    Used only for compact live-math snapshot bars.
    """

    cleaned = ""
    started = False

    for ch in text:
        if ch.isdigit() or ch in ".-":
            cleaned += ch
            started = True
        elif started:
            break

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def plot_math_snapshot(math_df: pd.DataFrame) -> go.Figure:
    """
    Plot selected live-math calculated values as a compact snapshot.

    Required columns:
        Section
        Calculated Value
    """

    if math_df.empty:
        fig = go.Figure()
        return apply_engineering_layout(
            fig,
            title="Live Math Snapshot",
            height=500,
            show_legend=False,
        )

    preferred_sections = [
        "Clock Period",
        "Wire Resistance",
        "Wire Capacitance",
        "Total RC Tau",
        "Segment RC Tau",
        "Insertion Delay",
        "Before Slew",
        "After Slew",
        "PSIJ Shift",
        "Setup Slack",
        "Hold Slack",
    ]

    filtered = math_df[math_df["Section"].isin(preferred_sections)].copy()

    if filtered.empty:
        filtered = math_df.head(10).copy()

    filtered["numeric_value"] = filtered["Calculated Value"].astype(str).map(
        _extract_first_numeric_value
    )

    fig = go.Figure(
        go.Bar(
            x=filtered["Section"],
            y=filtered["numeric_value"],
            text=filtered["Calculated Value"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
            name="Live Math",
        )
    )

    fig.update_xaxes(tickangle=-25)

    return apply_engineering_layout(
        fig,
        title="Live Math Snapshot — Formula-Linked Calculated Values",
        height=540,
        x_title="Calculation",
        y_title="Mixed engineering units",
        show_legend=False,
    )


def plot_node_metric_trend(
    node_table: pd.DataFrame,
    metric: str,
    title: str | None = None,
) -> go.Figure:
    """
    Plot a selected node metric across PLL-to-flip-flop path.

    Example metrics:
        Accum Delay (ps)
        Jitter RMS (fs)
        VDD Droop (mV)
        Slew (ps)
    """

    if title is None:
        title = f"Node Trend — {metric}"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=node_table["Node"],
            y=node_table[metric],
            mode="lines+markers",
            name=metric,
            line=dict(width=4),
            marker=dict(size=10),
            hovertemplate="<b>%{x}</b><br>%{y:.3f}<extra></extra>",
        )
    )

    return apply_engineering_layout(
        fig,
        title=title,
        height=460,
        x_title="Clock Path Node",
        y_title=metric,
        show_legend=False,
    )


def plot_combined_node_dashboard(node_table: pd.DataFrame) -> go.Figure:
    """
    Multi-row compact dashboard for delay, jitter, droop and slew trends.

    This is useful in the SoC journey tab.
    """

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.055,
        subplot_titles=(
            "Accumulated Delay (ps)",
            "Jitter RMS (fs)",
            "VDD Droop (mV)",
            "Slew (ps)",
        ),
    )

    metrics = [
        "Accum Delay (ps)",
        "Jitter RMS (fs)",
        "VDD Droop (mV)",
        "Slew (ps)",
    ]

    for row_index, metric in enumerate(metrics, start=1):
        fig.add_trace(
            go.Scatter(
                x=node_table["Node"],
                y=node_table[metric],
                mode="lines+markers",
                name=metric,
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate=f"<b>%{{x}}</b><br>{metric}=%{{y:.3f}}<extra></extra>",
            ),
            row=row_index,
            col=1,
        )

    fig.update_xaxes(tickangle=-15)
    fig.update_yaxes(gridcolor=GRID_COLOR, zeroline=False)

    return apply_engineering_layout(
        fig,
        title="Node-by-Node Clock Quality Trend",
        height=820,
        show_legend=False,
    )


__all__ = [
    "apply_engineering_layout",
    "budget_rows_to_dataframe",
    "plot_budget_bar",
    "plot_clock_waveforms",
    "plot_combined_node_dashboard",
    "plot_ir_drop_heatmap",
    "plot_jitter_budget",
    "plot_math_snapshot",
    "plot_node_metric_trend",
    "plot_skew_budget",
    "plot_soc_journey_map",
    "plot_timing_diagram",
]