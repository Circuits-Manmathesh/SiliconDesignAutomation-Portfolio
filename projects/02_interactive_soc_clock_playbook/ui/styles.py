from __future__ import annotations


APP_PAGE_TITLE = "Interactive SoC Clock Distribution Playbook"
APP_PAGE_ICON = "⏱️"


def get_global_css() -> str:
    """
    Global CSS for the Streamlit application.

    Design intent:
        - dark engineering dashboard
        - readable cards
        - clean technical hierarchy
        - not overly flashy
        - suitable for GitHub screenshots and LinkedIn demo video
    """

    return """
<style>
/* ---------------------------------------------------------
   Global page styling
--------------------------------------------------------- */

html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #050816 0%, #0b1020 45%, #111827 100%);
    color: #e5e7eb;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.0rem;
    max-width: 1500px;
}

/* ---------------------------------------------------------
   Headings
--------------------------------------------------------- */

h1 {
    color: #f8fafc;
    font-weight: 850;
    letter-spacing: -0.04em;
}

h2, h3 {
    color: #f8fafc;
    font-weight: 750;
}

p, li {
    color: #d1d5db;
    line-height: 1.55;
}

/* ---------------------------------------------------------
   Sidebar
--------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.18);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f8fafc;
}

/* ---------------------------------------------------------
   Tabs
--------------------------------------------------------- */

button[data-baseweb="tab"] {
    font-weight: 700;
    color: #cbd5e1;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #38bdf8;
    border-bottom-color: #38bdf8;
}

/* ---------------------------------------------------------
   Metric card
--------------------------------------------------------- */

.metric-card {
    padding: 1rem;
    border-radius: 18px;
    background:
        radial-gradient(circle at top left, rgba(56, 189, 248, 0.12), transparent 34%),
        linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(148, 163, 184, 0.18);
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.28);
    min-height: 95px;
}

.metric-label {
    color: #94a3b8;
    font-size: 0.82rem;
    font-weight: 650;
    letter-spacing: 0.02em;
    margin-bottom: 0.35rem;
}

.metric-value {
    color: #f8fafc;
    font-size: 1.30rem;
    font-weight: 850;
    letter-spacing: -0.02em;
}

.metric-subtitle {
    color: #9ca3af;
    font-size: 0.78rem;
    margin-top: 0.30rem;
}

/* ---------------------------------------------------------
   Explanation card
--------------------------------------------------------- */

.explain-card {
    padding: 1.05rem 1.1rem;
    border-radius: 18px;
    background:
        radial-gradient(circle at top right, rgba(99, 102, 241, 0.14), transparent 36%),
        linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid rgba(148, 163, 184, 0.16);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.22);
    margin-bottom: 0.85rem;
}

.explain-title {
    color: #93c5fd;
    font-weight: 850;
    font-size: 0.98rem;
    margin-bottom: 0.45rem;
}

.explain-body {
    color: #e5e7eb;
    font-size: 0.93rem;
    line-height: 1.58;
}

/* ---------------------------------------------------------
   Architecture / insight box
--------------------------------------------------------- */

.insight-box {
    padding: 1.15rem 1.2rem;
    border-radius: 18px;
    background:
        linear-gradient(135deg, rgba(14, 165, 233, 0.11), rgba(15, 23, 42, 0.96)),
        linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-left: 5px solid #38bdf8;
    color: #e5e7eb;
    line-height: 1.60;
    margin-bottom: 1rem;
}

.insight-box b {
    color: #f8fafc;
}

/* ---------------------------------------------------------
   Risk boxes
--------------------------------------------------------- */

.risk-low {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background: rgba(22, 163, 74, 0.10);
    border: 1px solid rgba(34, 197, 94, 0.28);
    border-left: 5px solid #22c55e;
    color: #dcfce7;
    margin-bottom: 0.8rem;
}

.risk-medium {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background: rgba(245, 158, 11, 0.11);
    border: 1px solid rgba(245, 158, 11, 0.30);
    border-left: 5px solid #f59e0b;
    color: #fef3c7;
    margin-bottom: 0.8rem;
}

.risk-high {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background: rgba(239, 68, 68, 0.11);
    border: 1px solid rgba(248, 113, 113, 0.32);
    border-left: 5px solid #ef4444;
    color: #fee2e2;
    margin-bottom: 0.8rem;
}

/* ---------------------------------------------------------
   Formula card
--------------------------------------------------------- */

.formula-card {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background:
        radial-gradient(circle at top left, rgba(16, 185, 129, 0.13), transparent 36%),
        linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(16, 185, 129, 0.25);
    margin-bottom: 0.85rem;
}

.formula-title {
    color: #6ee7b7;
    font-weight: 850;
    margin-bottom: 0.45rem;
}

.formula-body {
    color: #d1fae5;
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 0.92rem;
    line-height: 1.55;
}

/* ---------------------------------------------------------
   Recommendation card
--------------------------------------------------------- */

.recommendation-card {
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(148, 163, 184, 0.18);
    margin-bottom: 0.75rem;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.20);
}

.recommendation-title {
    color: #f8fafc;
    font-size: 1rem;
    font-weight: 850;
    margin-bottom: 0.4rem;
}

.recommendation-meta {
    color: #94a3b8;
    font-size: 0.82rem;
    margin-bottom: 0.45rem;
}

.recommendation-body {
    color: #e5e7eb;
    font-size: 0.92rem;
    line-height: 1.55;
}

/* ---------------------------------------------------------
   Small badges
--------------------------------------------------------- */

.badge {
    display: inline-block;
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.03em;
}

.badge-low {
    background: rgba(34, 197, 94, 0.14);
    color: #86efac;
    border: 1px solid rgba(34, 197, 94, 0.32);
}

.badge-medium {
    background: rgba(245, 158, 11, 0.16);
    color: #fcd34d;
    border: 1px solid rgba(245, 158, 11, 0.34);
}

.badge-high {
    background: rgba(239, 68, 68, 0.16);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.34);
}

/* ---------------------------------------------------------
   Dataframe polish
--------------------------------------------------------- */

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* ---------------------------------------------------------
   Footer note
--------------------------------------------------------- */

.footer-note {
    color: #94a3b8;
    font-size: 0.85rem;
    text-align: center;
    padding-top: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(148, 163, 184, 0.16);
}
</style>
"""


def metric_card(label: str, value: str, subtitle: str | None = None) -> str:
    """
    HTML metric card used across the app.

    Example:
        metric_card("Clock Period", "200 ps", "5 GHz")
    """

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="metric-subtitle">{subtitle}</div>'

    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {subtitle_html}
    </div>
    """


def explanation_card(title: str, body: str) -> str:
    """
    Compact explanation card.
    """

    return f"""
    <div class="explain-card">
        <div class="explain-title">{title}</div>
        <div class="explain-body">{body}</div>
    </div>
    """


def insight_box(body: str) -> str:
    """
    Blue architecture insight box.
    """

    return f"""
    <div class="insight-box">
        {body}
    </div>
    """


def formula_card(title: str, formula: str, explanation: str | None = None) -> str:
    """
    Formula display card.
    """

    explanation_html = ""
    if explanation:
        explanation_html = f'<div class="explain-body" style="margin-top:0.55rem;">{explanation}</div>'

    return f"""
    <div class="formula-card">
        <div class="formula-title">{title}</div>
        <div class="formula-body">{formula}</div>
        {explanation_html}
    </div>
    """


def risk_box(level: str, body: str) -> str:
    """
    Risk box with LOW/MEDIUM/HIGH styling.

    level can be:
        LOW
        MEDIUM
        HIGH
    """

    level_normalized = level.strip().lower()

    if level_normalized == "high":
        css_class = "risk-high"
    elif level_normalized == "medium":
        css_class = "risk-medium"
    else:
        css_class = "risk-low"

    return f"""
    <div class="{css_class}">
        {body}
    </div>
    """


def risk_badge(level: str) -> str:
    """
    Small colored risk badge.
    """

    level_upper = level.strip().upper()
    level_lower = level_upper.lower()

    if level_lower not in {"low", "medium", "high"}:
        level_lower = "low"
        level_upper = "LOW"

    return f"""
    <span class="badge badge-{level_lower}">{level_upper}</span>
    """


def recommendation_card(
    priority: int,
    risk_level: str,
    title: str,
    observation: str,
    recommended_action: str,
    engineering_reason: str,
) -> str:
    """
    HTML card for architecture recommendation.
    """

    badge = risk_badge(risk_level)

    return f"""
    <div class="recommendation-card">
        <div class="recommendation-title">
            #{priority} — {title} {badge}
        </div>
        <div class="recommendation-meta">
            <b>Observation:</b> {observation}
        </div>
        <div class="recommendation-body">
            <b>Recommended Action:</b> {recommended_action}<br>
            <b>Engineering Reason:</b> {engineering_reason}
        </div>
    </div>
    """


def footer_note() -> str:
    """
    Standard footer used in the app.
    """

    return """
    <div class="footer-note">
        Interactive SoC Clock Distribution Playbook — architecture-level educational and sensitivity-analysis tool.
        Final silicon signoff requires SPEF, Liberty, STA, SI, EMIR, PVT and OCV correlation.
    </div>
    """


__all__ = [
    "APP_PAGE_ICON",
    "APP_PAGE_TITLE",
    "explanation_card",
    "footer_note",
    "formula_card",
    "get_global_css",
    "insight_box",
    "metric_card",
    "recommendation_card",
    "risk_badge",
    "risk_box",
]