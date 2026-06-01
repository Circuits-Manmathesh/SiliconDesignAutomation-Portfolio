from __future__ import annotations

import streamlit as st

from core.clock_math import compute_core_math
from core.recommendation_engine import build_recommendation_package
from core.soc_path_engine import build_soc_path_package
from core.timing_engine import build_timing_package
from core.validation_cases import (
    run_all_validation_cases,
    validation_results_to_dataframe,
)
from core.waveform_engine import generate_waveforms
from ui.cards import (
    render_dataframe_with_note,
    render_metric_row,
    render_model_scope_note,
)
from ui.sidebar import render_sidebar_inputs, render_sidebar_scope_note
from ui.styles import (
    APP_PAGE_ICON,
    APP_PAGE_TITLE,
    footer_note,
    get_global_css,
)
from ui.tabs import render_playbook_tabs


def configure_page() -> None:
    """
    Configure Streamlit page.

    This must run before any other Streamlit UI rendering call.
    """

    st.set_page_config(
        page_title=APP_PAGE_TITLE,
        page_icon=APP_PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_app_header() -> None:
    """
    Render application title and top description.
    """

    st.title("Interactive SoC Clock Distribution Playbook")

    st.caption(
        "PLL-to-flip-flop clock-distribution analysis with live waveforms, "
        "SoC journey mapping, RC/slew modeling, jitter/skew budgeting, "
        "IR-drop/crosstalk awareness, setup/hold timing, and architecture recommendations."
    )


def build_engine_outputs(inputs):
    """
    Run all core engines in a single consistent sequence.

    Flow:
        inputs
            -> core math
            -> waveform
            -> SoC path package
            -> timing package
            -> recommendation package

    This keeps app.py readable and makes the dataflow explicit.
    """

    core_math = compute_core_math(inputs)

    waveform = generate_waveforms(
        inputs=inputs,
        core_math=core_math,
    )

    soc_package = build_soc_path_package(
        inputs=inputs,
        core_math=core_math,
    )

    timing_package = build_timing_package(
        inputs=inputs,
        core_math=core_math,
    )

    timing_result = timing_package["result"]

    recommendation_package = build_recommendation_package(
        inputs=inputs,
        core_math=core_math,
        timing=timing_result,
    )

    return {
        "core_math": core_math,
        "waveform": waveform,
        "soc_package": soc_package,
        "timing_package": timing_package,
        "recommendation_package": recommendation_package,
    }


def render_top_metric_strip(outputs) -> None:
    """
    Render top-level metrics that summarize current design condition.
    """

    core_math = outputs["core_math"]
    timing_result = outputs["timing_package"]["result"]

    render_metric_row(
        [
            (
                "Clock Period",
                f"{core_math.clock_period_ps:.3f} ps",
                "Tclk = 1000 / fGHz",
            ),
            (
                "RC Segment Tau",
                f"{core_math.segment_rc_tau_ps:.3f} ps",
                "Effective buffered segment",
            ),
            (
                "Endpoint Jitter",
                f"{core_math.after_total_jitter_fs:.3f} fs",
                "After mitigation metric",
            ),
            (
                "Setup Slack",
                f"{timing_result.setup_slack_ps:.3f} ps",
                timing_result.status.value,
            ),
            (
                "Hold Slack",
                f"{timing_result.hold_slack_ps:.3f} ps",
                timing_result.status.value,
            ),
        ],
        columns=5,
    )


def render_validation_panel() -> None:
    """
    Optional validation runner in sidebar.

    This is useful for GitHub users who want to confirm that core formulas
    are internally consistent after installation.
    """

    with st.sidebar.expander("Validation / Self-Check", expanded=False):
        st.caption(
            "Run internal baseline and stress-case checks. "
            "This validates model consistency, not silicon signoff accuracy."
        )

        if st.button("Run Validation Cases", use_container_width=True):
            results = run_all_validation_cases()
            df = validation_results_to_dataframe(results)

            passed = int(df["Passed"].sum())
            total = len(df)

            if passed == total:
                st.success(f"All validation cases passed: {passed}/{total}")
            else:
                st.error(f"Validation failures: {total - passed}/{total}")

            render_dataframe_with_note(
                df,
                note="Validation checks baseline math, stress cases, waveform sanity, timing status, and recommendations.",
                height=260,
            )


def main() -> None:
    configure_page()

    st.markdown(get_global_css(), unsafe_allow_html=True)

    render_app_header()

    inputs = render_sidebar_inputs()
    render_sidebar_scope_note()
    render_validation_panel()

    outputs = build_engine_outputs(inputs)

    render_top_metric_strip(outputs)

    render_playbook_tabs(
        inputs=inputs,
        core_math=outputs["core_math"],
        waveform=outputs["waveform"],
        soc_package=outputs["soc_package"],
        timing_package=outputs["timing_package"],
        recommendation_package=outputs["recommendation_package"],
    )

    render_model_scope_note()
    st.markdown(footer_note(), unsafe_allow_html=True)


if __name__ == "__main__":
    main()