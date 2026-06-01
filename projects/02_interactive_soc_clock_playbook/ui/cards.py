from __future__ import annotations

from textwrap import dedent
from typing import Iterable, Sequence
import re

import pandas as pd
import streamlit as st

from core.models import (
    MathAnalysisRow,
    Recommendation,
    RiskLevel,
    TimingResult,
    TimingStatus,
)
from ui.styles import (
    explanation_card,
    formula_card,
    insight_box,
    metric_card,
    risk_box,
)


def render_markdown_card(html: str) -> None:
    """
    Render trusted project-generated HTML.

    Defensive cleanup prevents Streamlit from treating indented multiline HTML
    as a code block.
    """

    clean_html = dedent(html).strip()
    clean_html = re.sub(r">\s+<", "><", clean_html)
    st.markdown(clean_html, unsafe_allow_html=True)


def render_section_header(
    title: str,
    subtitle: str | None = None,
) -> None:
    st.header(title)

    if subtitle:
        st.caption(subtitle)


def render_metric_row(
    metrics: Sequence[tuple[str, str] | tuple[str, str, str]],
    columns: int | None = None,
) -> None:
    if not metrics:
        return

    col_count = columns or len(metrics)
    col_count = max(1, min(col_count, len(metrics)))

    cols = st.columns(col_count)

    for index, metric in enumerate(metrics):
        label = metric[0]
        value = metric[1]
        subtitle = metric[2] if len(metric) >= 3 else None

        with cols[index % col_count]:
            render_markdown_card(metric_card(label, value, subtitle))


def render_explanation_grid(
    cards: Sequence[tuple[str, str]],
    columns: int = 2,
) -> None:
    if not cards:
        return

    col_count = max(1, min(columns, len(cards)))
    cols = st.columns(col_count)

    for index, (title, body) in enumerate(cards):
        with cols[index % col_count]:
            render_markdown_card(explanation_card(title, body))


def render_architecture_insight(
    observation: str,
    physical_cause: str,
    architecture_action: str,
    note: str | None = None,
) -> None:
    note_html = ""
    if note:
        note_html = f"<br><br><b>Note:</b> {note}"

    html = f"""
    <b>Observation:</b> {observation}<br>
    <b>Physical Cause:</b> {physical_cause}<br>
    <b>Architecture Action:</b> {architecture_action}
    {note_html}
    """

    render_markdown_card(insight_box(html))


def render_formula_highlight(
    title: str,
    formula: str,
    explanation: str | None = None,
) -> None:
    render_markdown_card(
        formula_card(
            title=title,
            formula=formula,
            explanation=explanation,
        )
    )


def render_formula_rows(
    rows: Iterable[MathAnalysisRow],
    max_rows: int | None = None,
) -> None:
    count = 0

    for row in rows:
        if max_rows is not None and count >= max_rows:
            break

        explanation = (
            f"<b>Substitution:</b> {row.substitution}<br>"
            f"<b>Calculated Value:</b> {row.calculated_value}<br><br>"
            f"<b>Physical Meaning:</b> {row.physical_meaning}<br>"
            f"<b>Risk / Action:</b> {row.risk_or_action}"
        )

        render_formula_highlight(
            title=row.section,
            formula=row.formula,
            explanation=explanation,
        )

        count += 1


def render_timing_status_banner(result: TimingResult) -> None:
    if result.status == TimingStatus.PASS:
        level = "LOW"
        body = (
            f"<b>Timing Status:</b> PASS<br>"
            f"Setup Slack = <b>{result.setup_slack_ps:.3f} ps</b>, "
            f"Hold Slack = <b>{result.hold_slack_ps:.3f} ps</b>.<br>"
            "Both setup and hold are positive in the current simplified architecture model."
        )

    elif result.status == TimingStatus.SETUP_VIOLATION:
        level = "HIGH"
        body = (
            f"<b>Timing Status:</b> SETUP VIOLATION<br>"
            f"Setup Slack = <b>{result.setup_slack_ps:.3f} ps</b>.<br>"
            "Data is arriving too late relative to the capture clock edge."
        )

    elif result.status == TimingStatus.HOLD_VIOLATION:
        level = "HIGH"
        body = (
            f"<b>Timing Status:</b> HOLD VIOLATION<br>"
            f"Hold Slack = <b>{result.hold_slack_ps:.3f} ps</b>.<br>"
            "Data is changing too early relative to the hold requirement."
        )

    else:
        level = "HIGH"
        body = (
            f"<b>Timing Status:</b> SETUP + HOLD RISK<br>"
            f"Setup Slack = <b>{result.setup_slack_ps:.3f} ps</b>, "
            f"Hold Slack = <b>{result.hold_slack_ps:.3f} ps</b>.<br>"
            "Both long-path and short-path risk indicators need architecture review."
        )

    render_markdown_card(risk_box(level, body))


def _risk_icon(level: RiskLevel) -> str:
    if level == RiskLevel.HIGH:
        return "🔴 HIGH"

    if level == RiskLevel.MEDIUM:
        return "🟠 MEDIUM"

    return "🟢 LOW"


def render_recommendations(
    recommendations: Sequence[Recommendation],
    max_items: int | None = None,
) -> None:
    """
    Render recommendations using Streamlit-native components only.

    Important:
    - This function avoids raw HTML for recommendation cards.
    - The visible card number is a serial display index.
    - The priority remains visible separately as engineering priority.
    """

    if not recommendations:
        st.info(
            "No recommendation generated. Current condition does not trigger "
            "any rule-based architecture action."
        )
        return

    for index, rec in enumerate(recommendations, start=1):
        if max_items is not None and index > max_items:
            break

        with st.container(border=True):
            st.markdown(
                f"### Recommendation {index} | Priority {rec.priority} — {rec.title}"
            )

            st.markdown(f"**Risk Level:** {_risk_icon(rec.risk_level)}")
            st.markdown(f"**Observation:** {rec.observation}")
            st.markdown(f"**Recommended Action:** {rec.recommended_action}")
            st.markdown(f"**Engineering Reason:** {rec.engineering_reason}")


def render_dataframe_with_note(
    df: pd.DataFrame,
    note: str | None = None,
    height: int | str | None = None,
) -> None:
    """
    Render a dataframe with optional explanation note.

    Streamlit compatibility:
    height=None must not be passed into st.dataframe().
    """

    if note:
        st.caption(note)

    dataframe_kwargs = {
        "data": df,
        "use_container_width": True,
    }

    if height is not None:
        dataframe_kwargs["height"] = height

    st.dataframe(**dataframe_kwargs)


def render_two_column_tables(
    left_title: str,
    left_df: pd.DataFrame,
    right_title: str,
    right_df: pd.DataFrame,
    left_note: str | None = None,
    right_note: str | None = None,
    left_height: int | str | None = None,
    right_height: int | str | None = None,
) -> None:
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader(left_title)
        render_dataframe_with_note(
            df=left_df,
            note=left_note,
            height=left_height,
        )

    with right_col:
        st.subheader(right_title)
        render_dataframe_with_note(
            df=right_df,
            note=right_note,
            height=right_height,
        )


def render_risk_summary(
    title: str,
    items: Sequence[tuple[str, str]],
    level: str = "LOW",
) -> None:
    lines = [f"<b>{label}:</b> {value}" for label, value in items]
    body = f"<b>{title}</b><br>" + "<br>".join(lines)

    render_markdown_card(risk_box(level, body))


def render_model_scope_note() -> None:
    render_markdown_card(
        risk_box(
            "LOW",
            "<b>Model Scope:</b><br>"
            "This playbook uses architecture-level sensitivity models. "
            "It is designed for learning, early architecture review, and explainable tradeoff analysis. "
            "Final silicon signoff still requires SPEF, Liberty, STA, SI, EMIR, PVT and OCV correlation.",
        )
    )


def render_intro_panel() -> None:
    render_markdown_card(
        insight_box(
            "<b>Interactive SoC Clock Distribution Playbook</b><br><br>"
            "This app visualizes how a clock signal evolves from PLL to flip-flop. "
            "It connects clock source quality, interconnect RC, repeater strategy, "
            "IR-drop, crosstalk, skew, setup/hold timing, and architecture recommendations "
            "into one explainable workflow."
        )
    )


def render_status_metrics_from_timing(result: TimingResult) -> None:
    render_metric_row(
        [
            ("Timing Status", result.status.value),
            ("Setup Slack", f"{result.setup_slack_ps:.3f} ps"),
            ("Hold Slack", f"{result.hold_slack_ps:.3f} ps"),
            ("Effective Skew", f"{result.final_effective_skew_ps:.3f} ps"),
        ],
        columns=4,
    )


def risk_level_from_value(
    value: float,
    medium_threshold: float,
    high_threshold: float,
) -> RiskLevel:
    if value >= high_threshold:
        return RiskLevel.HIGH

    if value >= medium_threshold:
        return RiskLevel.MEDIUM

    return RiskLevel.LOW


__all__ = [
    "render_architecture_insight",
    "render_dataframe_with_note",
    "render_explanation_grid",
    "render_formula_highlight",
    "render_formula_rows",
    "render_intro_panel",
    "render_markdown_card",
    "render_metric_row",
    "render_model_scope_note",
    "render_recommendations",
    "render_risk_summary",
    "render_section_header",
    "render_status_metrics_from_timing",
    "render_timing_status_banner",
    "render_two_column_tables",
    "risk_level_from_value",
]