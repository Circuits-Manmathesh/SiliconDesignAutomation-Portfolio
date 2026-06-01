from __future__ import annotations

import math

import networkx as nx
import pandas as pd

from core.clock_math import compute_core_math
from core.models import ClockNodeResult, CoreMathResult, PlaybookInputs


def _rss(*values: float) -> float:
    """
    Root-sum-square helper.

    Used for combining independent architecture-level uncertainty terms.
    """
    return math.sqrt(sum(v * v for v in values))


def build_clock_path_graph() -> nx.DiGraph:
    """
    Build the logical PLL-to-flip-flop clock journey graph.

    This is a conceptual architecture graph, not a physical DEF/LEF graph.

    Path:
        PLL -> Divider -> Global Trunk -> Regional Branch -> Local Leaf -> Flip-Flop
    """

    graph = nx.DiGraph()

    graph.add_node(
        "PLL",
        role="Clock source",
        description="Clock origin with phase noise and duty-cycle distortion.",
    )

    graph.add_node(
        "Divider",
        role="Clock conditioning",
        description="Frequency division and duty-cycle cleanup stage.",
    )

    graph.add_node(
        "Global Trunk",
        role="Long-distance distribution",
        description="Top-metal global route carrying clock across the SoC.",
    )

    graph.add_node(
        "Regional Branch",
        role="Regional distribution",
        description="Clock distribution into compute/memory/NoC regions.",
    )

    graph.add_node(
        "Local Leaf",
        role="Local delivery",
        description="Local clock buffering close to sequential cells.",
    )

    graph.add_node(
        "Flip-Flop",
        role="Timing endpoint",
        description="Final capture point where setup/hold are judged.",
    )

    graph.add_edge(
        "PLL",
        "Divider",
        physical_meaning="Source clock conditioning path.",
    )
    graph.add_edge(
        "Divider",
        "Global Trunk",
        physical_meaning="Conditioned clock enters global clock spine.",
    )
    graph.add_edge(
        "Global Trunk",
        "Regional Branch",
        physical_meaning="Global clock branches into regional distribution.",
    )
    graph.add_edge(
        "Regional Branch",
        "Local Leaf",
        physical_meaning="Regional clock reaches local clock buffers.",
    )
    graph.add_edge(
        "Local Leaf",
        "Flip-Flop",
        physical_meaning="Final local clock reaches sequential endpoint.",
    )

    return graph


def build_clock_nodes(
    inputs: PlaybookInputs,
    core_math: CoreMathResult | None = None,
) -> list[ClockNodeResult]:
    """
    Build node-by-node SoC clock quality results.

    Each node includes:
        - normalized map coordinate
        - accumulated delay
        - jitter RMS
        - local skew
        - local VDD droop
        - slew
        - physical role
        - risk
        - mitigation hint

    Engineering positioning:
        These values are architecture-level explainability values.
        They help understand trend and sensitivity.
        They are not signoff extracted node delays.
    """

    if core_math is None:
        core_math = compute_core_math(inputs)

    clock = inputs.clock
    noise = inputs.noise
    interconnect = inputs.interconnect

    mitigation = core_math.mitigation_factor

    # ------------------------------------------------------------------
    # Incremental delay model
    #
    # The goal is not to claim extracted physical delays.
    # The goal is to give a realistic directional clock-latency trend.
    #
    # PLL node starts at 0.
    # Divider has small conditioning delay.
    # Global trunk sees a large share of insertion + segment RC contribution.
    # Regional/local nodes see remaining buffer and local RC/noise effects.
    # ------------------------------------------------------------------
    divider_delay_ps = 2.0

    global_increment_ps = (
        0.50 * core_math.insertion_delay_ps
        + 0.80 * core_math.segment_rc_tau_ps
    )

    regional_increment_ps = (
        0.30 * core_math.insertion_delay_ps
        + 0.45 * core_math.segment_rc_tau_ps
        + 0.50 * core_math.psij_edge_shift_ps
    )

    local_increment_ps = (
        0.20 * core_math.insertion_delay_ps
        + 0.25 * core_math.segment_rc_tau_ps
        + 0.50 * core_math.psij_edge_shift_ps
        + 0.20 * abs(core_math.crosstalk_edge_shift_ps)
    )

    flop_increment_ps = 0.25

    pll_acc_delay_ps = 0.0
    divider_acc_delay_ps = pll_acc_delay_ps + divider_delay_ps
    global_acc_delay_ps = divider_acc_delay_ps + global_increment_ps
    regional_acc_delay_ps = global_acc_delay_ps + regional_increment_ps
    local_acc_delay_ps = regional_acc_delay_ps + local_increment_ps
    flop_acc_delay_ps = local_acc_delay_ps + flop_increment_ps

    # ------------------------------------------------------------------
    # Jitter propagation model
    #
    # Jitter starts from PLL.
    # Divider reduces source jitter partially.
    # RC, PSIJ, and crosstalk uncertainty gradually appear along path.
    # Mitigation reduces the effective observed uncertainty.
    # ------------------------------------------------------------------
    pll_jitter_fs = clock.pll_random_jitter_fs

    divider_jitter_fs = _rss(0.72 * pll_jitter_fs, 5.0)

    global_jitter_fs = _rss(
        0.78 * pll_jitter_fs,
        0.40 * core_math.rc_uncertainty_fs,
    )

    regional_jitter_fs = _rss(
        0.90 * pll_jitter_fs,
        0.65 * core_math.rc_uncertainty_fs,
        0.60 * core_math.psij_jitter_fs,
    )

    local_jitter_fs = _rss(
        1.00 * pll_jitter_fs,
        0.85 * core_math.rc_uncertainty_fs,
        0.80 * core_math.psij_jitter_fs,
        0.60 * core_math.crosstalk_jitter_fs,
    )

    flop_jitter_fs = core_math.after_total_jitter_fs

    # Apply mitigation only where distribution/environment starts to dominate.
    # PLL/source value is not reduced by shielding/decaps.
    divider_jitter_fs *= 1.0
    global_jitter_fs *= mitigation
    regional_jitter_fs *= mitigation
    local_jitter_fs *= mitigation

    # ------------------------------------------------------------------
    # Droop distribution model
    #
    # Droop is spatial. It is usually low near PLL/divider and higher in
    # compute/local regions where switching activity is stronger.
    # ------------------------------------------------------------------
    pll_droop_mv = 0.00
    divider_droop_mv = 0.05 * noise.dynamic_vdd_droop_mv * mitigation
    global_droop_mv = 0.25 * noise.dynamic_vdd_droop_mv * mitigation
    regional_droop_mv = 0.65 * noise.dynamic_vdd_droop_mv * mitigation
    local_droop_mv = 1.00 * noise.dynamic_vdd_droop_mv * mitigation
    flop_droop_mv = 0.85 * noise.dynamic_vdd_droop_mv * mitigation

    # ------------------------------------------------------------------
    # Skew distribution model
    #
    # Spatial skew is shown mainly toward endpoint side.
    # Small internal mismatch is shown along the path.
    # ------------------------------------------------------------------
    trunk_mismatch_ps = 0.0025 * interconnect.global_wire_length_um
    regional_mismatch_ps = 2.5 + 0.25 * interconnect.repeater_count
    local_mismatch_ps = 1.5 + 0.03 * noise.dynamic_vdd_droop_mv

    pll_skew_ps = 0.0
    divider_skew_ps = 0.2
    global_skew_ps = trunk_mismatch_ps
    regional_skew_ps = regional_mismatch_ps
    local_skew_ps = local_mismatch_ps
    flop_skew_ps = inputs.timing.spatial_clock_skew_ps + inputs.timing.useful_skew_ps

    # ------------------------------------------------------------------
    # Slew distribution model
    #
    # PLL/divider are cleaner.
    # Global trunk is most RC-sensitive.
    # Regional/local improve depending on buffers/mitigation.
    # ------------------------------------------------------------------
    base_slew = inputs.constants.base_slew_ps

    pll_slew_ps = base_slew
    divider_slew_ps = base_slew + 0.2
    global_slew_ps = core_math.before_slew_ps
    regional_slew_ps = 0.75 * core_math.before_slew_ps + 0.25 * core_math.after_slew_ps
    local_slew_ps = core_math.after_slew_ps
    flop_slew_ps = core_math.after_slew_ps

    nodes = [
        ClockNodeResult(
            node="PLL",
            x_norm=0.08,
            y_norm=0.50,
            accumulated_delay_ps=pll_acc_delay_ps,
            jitter_rms_fs=pll_jitter_fs,
            local_skew_ps=pll_skew_ps,
            vdd_droop_mv=pll_droop_mv,
            slew_ps=pll_slew_ps,
            physical_role="Clock source / PLL output.",
            key_risk="Phase noise and duty-cycle distortion start at the source.",
            mitigation_hint="Use low-noise PLL design, clock conditioning, and duty-cycle correction.",
        ),
        ClockNodeResult(
            node="Divider",
            x_norm=0.22,
            y_norm=0.50,
            accumulated_delay_ps=divider_acc_delay_ps,
            jitter_rms_fs=divider_jitter_fs,
            local_skew_ps=divider_skew_ps,
            vdd_droop_mv=divider_droop_mv,
            slew_ps=divider_slew_ps,
            physical_role="Frequency division and duty-cycle cleanup.",
            key_risk="Divider can add residual delay/jitter but improves clock symmetry.",
            mitigation_hint="Use balanced divider layout and verify duty-cycle recovery.",
        ),
        ClockNodeResult(
            node="Global Trunk",
            x_norm=0.42,
            y_norm=0.50,
            accumulated_delay_ps=global_acc_delay_ps,
            jitter_rms_fs=global_jitter_fs,
            local_skew_ps=global_skew_ps,
            vdd_droop_mv=global_droop_mv,
            slew_ps=global_slew_ps,
            physical_role="Long top-metal clock spine across the SoC.",
            key_risk="Wire RC can degrade slew and create timing uncertainty.",
            mitigation_hint="Use top metal, shielding, proper segmentation, and repeater optimization.",
        ),
        ClockNodeResult(
            node="Regional Branch",
            x_norm=0.64,
            y_norm=0.68,
            accumulated_delay_ps=regional_acc_delay_ps,
            jitter_rms_fs=regional_jitter_fs,
            local_skew_ps=regional_skew_ps,
            vdd_droop_mv=regional_droop_mv,
            slew_ps=regional_slew_ps,
            physical_role="Clock distribution into compute/memory/NoC regions.",
            key_risk="Different regions see different activity, droop, and skew behavior.",
            mitigation_hint="Apply region-aware CTS, local decaps, and activity-aware clock planning.",
        ),
        ClockNodeResult(
            node="Local Leaf",
            x_norm=0.80,
            y_norm=0.40,
            accumulated_delay_ps=local_acc_delay_ps,
            jitter_rms_fs=local_jitter_fs,
            local_skew_ps=local_skew_ps,
            vdd_droop_mv=local_droop_mv,
            slew_ps=local_slew_ps,
            physical_role="Local clock buffers near sequential cells.",
            key_risk="Local IR-drop and buffer variation can move final clock edge.",
            mitigation_hint="Strengthen local power grid, add decaps, and balance leaf buffers.",
        ),
        ClockNodeResult(
            node="Flip-Flop",
            x_norm=0.93,
            y_norm=0.40,
            accumulated_delay_ps=flop_acc_delay_ps,
            jitter_rms_fs=flop_jitter_fs,
            local_skew_ps=flop_skew_ps,
            vdd_droop_mv=flop_droop_mv,
            slew_ps=flop_slew_ps,
            physical_role="Final capture endpoint.",
            key_risk="Setup/hold margin depends on final clock and data arrival relationship.",
            mitigation_hint="Check setup/hold slack, useful skew, hold buffers, and path balance.",
        ),
    ]

    return nodes


def nodes_to_dataframe(nodes: list[ClockNodeResult]) -> pd.DataFrame:
    """
    Convert node results to a UI/GitHub-friendly table.
    """

    return pd.DataFrame(
        [
            {
                "Node": node.node,
                "x": node.x_norm,
                "y": node.y_norm,
                "Accum Delay (ps)": node.accumulated_delay_ps,
                "Jitter RMS (fs)": node.jitter_rms_fs,
                "Local Skew (ps)": node.local_skew_ps,
                "VDD Droop (mV)": node.vdd_droop_mv,
                "Slew (ps)": node.slew_ps,
                "Physical Role": node.physical_role,
                "Key Risk": node.key_risk,
                "Mitigation Hint": node.mitigation_hint,
            }
            for node in nodes
        ]
    )


def graph_edges_to_dataframe(graph: nx.DiGraph) -> pd.DataFrame:
    """
    Convert NetworkX graph edges into a readable table.
    """

    rows = []
    for source, target, data in graph.edges(data=True):
        rows.append(
            {
                "Source": source,
                "Target": target,
                "Physical Meaning": data.get("physical_meaning", ""),
            }
        )

    return pd.DataFrame(rows)


def build_soc_path_package(
    inputs: PlaybookInputs,
    core_math: CoreMathResult | None = None,
) -> dict[str, object]:
    """
    Convenience function used later by the UI.

    Returns:
        graph:
            NetworkX directed graph.

        nodes:
            List of ClockNodeResult.

        node_table:
            Pandas DataFrame for Streamlit.

        edge_table:
            Pandas DataFrame for Streamlit/docs.
    """

    if core_math is None:
        core_math = compute_core_math(inputs)

    graph = build_clock_path_graph()
    nodes = build_clock_nodes(inputs, core_math)
    node_table = nodes_to_dataframe(nodes)
    edge_table = graph_edges_to_dataframe(graph)

    return {
        "graph": graph,
        "nodes": nodes,
        "node_table": node_table,
        "edge_table": edge_table,
    }


__all__ = [
    "build_clock_nodes",
    "build_clock_path_graph",
    "build_soc_path_package",
    "graph_edges_to_dataframe",
    "nodes_to_dataframe",
]