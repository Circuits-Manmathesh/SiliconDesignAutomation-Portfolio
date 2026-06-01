from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictBaseModel(BaseModel):
    """
    Base model used across the playbook.

    extra='forbid' helps catch spelling mistakes or unexpected fields early.
    validate_assignment=True helps during development if values are updated later.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )


class CrosstalkMode(str, Enum):
    IN_PHASE = "In-Phase"
    OUT_OF_PHASE = "Out-of-Phase"
    QUIET = "Quiet / Orthogonal"


class TimingStatus(str, Enum):
    PASS = "PASS"
    SETUP_VIOLATION = "SETUP VIOLATION"
    HOLD_VIOLATION = "HOLD VIOLATION"
    SETUP_AND_HOLD_RISK = "SETUP + HOLD RISK"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class SiliconModelConstants(StrictBaseModel):
    """
    Centralized architecture-level modeling constants.

    These are not foundry signoff constants.
    They are sensitivity-model constants used to make the playbook explainable.
    Future versions can calibrate these using SPEF, Liberty, STA, SI and EMIR data.
    """

    wire_width_um: float = Field(
        default=0.08,
        gt=0.0,
        description="Assumed effective top-metal clock route width in microns.",
    )

    base_slew_ps: float = Field(
        default=0.8,
        gt=0.0,
        description="Minimum idealized local clock edge slew in ps.",
    )

    rc_slew_gain: float = Field(
        default=2.4,
        gt=0.0,
        description="Architecture sensitivity factor mapping segment RC to slew degradation.",
    )

    buffer_delay_ps: float = Field(
        default=3.2,
        gt=0.0,
        description="Approximate delay per clock repeater/buffer stage in ps.",
    )

    psij_delay_coeff_ps_per_mv: float = Field(
        default=0.0048,
        ge=0.0,
        description="Delay shift sensitivity to dynamic VDD droop in ps/mV.",
    )

    psij_jitter_coeff_fs_per_mv: float = Field(
        default=1.8,
        ge=0.0,
        description="Jitter sensitivity to dynamic VDD droop in fs/mV.",
    )

    rc_uncertainty_coeff: float = Field(
        default=0.18,
        ge=0.0,
        description="Maps effective segment RC in ps to architecture-level uncertainty in fs.",
    )

    shielded_mitigation_factor: float = Field(
        default=0.35,
        gt=0.0,
        le=1.0,
        description="Residual uncertainty factor when shielding and decaps are enabled.",
    )

    unshielded_mitigation_factor: float = Field(
        default=0.72,
        gt=0.0,
        le=1.0,
        description="Residual uncertainty factor when mitigation is partial or disabled.",
    )

    nominal_vdd_v: float = Field(
        default=0.75,
        gt=0.0,
        description="Nominal illustrative VDD used for waveform amplitude.",
    )


class ClockSourceInputs(StrictBaseModel):
    """
    User-facing PLL/source clock controls.
    """

    frequency_ghz: float = Field(
        default=5.0,
        ge=0.5,
        le=12.0,
        description="Clock frequency in GHz.",
    )

    pll_random_jitter_fs: float = Field(
        default=120.0,
        ge=0.0,
        le=1000.0,
        description="PLL random jitter RMS in femtoseconds.",
    )

    pll_duty_cycle_percent: float = Field(
        default=51.5,
        ge=40.0,
        le=60.0,
        description="PLL output duty cycle percentage.",
    )

    @field_validator("pll_duty_cycle_percent")
    @classmethod
    def warn_realistic_duty_range(cls, value: float) -> float:
        """
        Keep model mathematically valid while allowing deliberate stress cases.

        UI should normally expose 45% to 55%.
        The model allows 40% to 60% only for controlled stress experiments.
        """
        return value


class InterconnectInputs(StrictBaseModel):
    """
    User-facing global clock distribution network controls.
    """

    global_wire_length_um: float = Field(
        default=2400.0,
        ge=50.0,
        le=10000.0,
        description="Representative global clock trunk length in microns.",
    )

    top_metal_sheet_resistance_mohm_sq: float = Field(
        default=28.0,
        ge=1.0,
        le=200.0,
        description="Top-metal sheet resistance in milliohm per square.",
    )

    wire_capacitance_af_um: float = Field(
        default=95.0,
        ge=1.0,
        le=500.0,
        description="Wire capacitance in attofarad per micron.",
    )

    repeater_count: int = Field(
        default=4,
        ge=0,
        le=64,
        description="Number of inserted repeaters/buffers along the clock route.",
    )


class SiliconNoiseInputs(StrictBaseModel):
    """
    User-facing real-silicon disturbance controls.
    """

    dynamic_vdd_droop_mv: float = Field(
        default=45.0,
        ge=0.0,
        le=200.0,
        description="Dynamic supply droop in millivolts.",
    )

    crosstalk_mode: CrosstalkMode = Field(
        default=CrosstalkMode.QUIET,
        description="Aggressor alignment relative to the victim clock.",
    )

    shielding_decaps_enabled: bool = Field(
        default=True,
        description="Whether shielding and decap mitigation are enabled.",
    )


class TimingInputs(StrictBaseModel):
    """
    User-facing flip-flop timing controls.
    """

    logic_path_delay_ps: float = Field(
        default=175.0,
        ge=0.0,
        le=1000.0,
        description="Data path delay from launch flop to capture flop in ps.",
    )

    spatial_clock_skew_ps: float = Field(
        default=8.0,
        ge=-200.0,
        le=200.0,
        description="Spatial clock skew between launch and capture domains in ps.",
    )

    useful_skew_ps: float = Field(
        default=0.0,
        ge=-200.0,
        le=200.0,
        description="Intentional useful skew applied to improve timing margin.",
    )

    setup_requirement_ps: float = Field(
        default=8.0,
        ge=0.0,
        le=100.0,
        description="Flip-flop setup requirement in ps.",
    )

    hold_requirement_ps: float = Field(
        default=5.0,
        ge=0.0,
        le=100.0,
        description="Flip-flop hold requirement in ps.",
    )


class PlaybookInputs(StrictBaseModel):
    """
    Complete set of user inputs used by all engines.
    """

    clock: ClockSourceInputs = Field(default_factory=ClockSourceInputs)
    interconnect: InterconnectInputs = Field(default_factory=InterconnectInputs)
    noise: SiliconNoiseInputs = Field(default_factory=SiliconNoiseInputs)
    timing: TimingInputs = Field(default_factory=TimingInputs)
    constants: SiliconModelConstants = Field(default_factory=SiliconModelConstants)

    design_name: str = Field(
        default="AI SoC 5 GHz Clock Distribution Demo",
        min_length=1,
        description="Human-readable demo/design name.",
    )


class CoreMathResult(StrictBaseModel):
    """
    Core calculated values shared by waveform, budget, timing, and math-analysis engines.
    """

    clock_period_ps: float

    duty_cycle_error_percent: float

    wire_width_um: float
    wire_squares: float
    wire_resistance_ohm: float
    wire_capacitance_ff: float

    total_rc_tau_ps: float
    segment_count: int
    segment_rc_tau_ps: float

    insertion_delay_ps: float

    before_slew_ps: float
    after_slew_ps: float

    psij_edge_shift_ps: float
    psij_jitter_fs: float

    crosstalk_edge_shift_ps: float
    crosstalk_jitter_fs: float

    rc_uncertainty_fs: float

    before_total_jitter_fs: float
    after_total_jitter_fs: float

    mitigation_factor: float

    before_edge_shift_ps: float
    after_edge_shift_ps: float


class ClockNodeResult(StrictBaseModel):
    """
    One row in the PLL-to-flip-flop SoC journey map.
    """

    node: str
    x_norm: float = Field(ge=0.0, le=1.0)
    y_norm: float = Field(ge=0.0, le=1.0)

    accumulated_delay_ps: float
    jitter_rms_fs: float
    local_skew_ps: float
    vdd_droop_mv: float
    slew_ps: float

    physical_role: str
    key_risk: str
    mitigation_hint: str


class BudgetRow(StrictBaseModel):
    """
    Generic row for jitter/skew/delay budget tables.
    """

    category: str
    component: str
    value: float
    unit: str
    meaning: str


class MathAnalysisRow(StrictBaseModel):
    """
    Formula-by-formula explainability row.
    """

    section: str
    formula: str
    substitution: str
    calculated_value: str
    physical_meaning: str
    risk_or_action: str


class TimingResult(StrictBaseModel):
    """
    Final setup/hold timing calculation result.
    """

    period_ps: float
    launch_clock_ps: float
    capture_clock_ps: float
    data_arrival_ps: float

    setup_requirement_ps: float
    hold_requirement_ps: float

    spatial_skew_ps: float
    useful_skew_ps: float
    final_effective_skew_ps: float

    setup_slack_ps: float
    hold_slack_ps: float

    status: TimingStatus
    explanation: str


class Recommendation(StrictBaseModel):
    """
    Architecture action generated from observed risk.
    """

    priority: int = Field(ge=1, le=10)
    risk_level: RiskLevel
    title: str
    observation: str
    recommended_action: str
    engineering_reason: str


class WaveformResult(StrictBaseModel):
    """
    Waveform vectors are stored as lists to keep the model JSON/GitHub friendly.

    Plotting engines can convert these lists back to NumPy arrays.
    """

    time_ps: list[float]
    ideal_clock_v: list[float]
    degraded_clock_v: list[float]
    mitigated_clock_v: list[float]

    @model_validator(mode="after")
    def validate_vector_lengths(self) -> "WaveformResult":
        lengths = {
            len(self.time_ps),
            len(self.ideal_clock_v),
            len(self.degraded_clock_v),
            len(self.mitigated_clock_v),
        }
        if len(lengths) != 1:
            raise ValueError("All waveform vectors must have the same length.")
        return self


class HeatmapResult(StrictBaseModel):
    """
    IR-drop heatmap result stored in JSON-friendly format.
    """

    x_axis: list[float]
    y_axis: list[float]
    droop_grid_mv: list[list[float]]
    clock_path_x: list[float]
    clock_path_y: list[float]


class PlaybookResults(StrictBaseModel):
    """
    Complete result packet produced by the engines.
    """

    inputs: PlaybookInputs
    core_math: CoreMathResult
    nodes: list[ClockNodeResult]
    jitter_budget: list[BudgetRow]
    skew_budget: list[BudgetRow]
    math_analysis: list[MathAnalysisRow]
    timing: TimingResult
    recommendations: list[Recommendation]
    waveform: WaveformResult | None = None
    heatmap: HeatmapResult | None = None


def default_ai_soc_5ghz_inputs() -> PlaybookInputs:
    """
    Canonical baseline case used in examples, docs, and validation.

    This is the first demo scenario:
    a 5 GHz AI SoC clock distribution review case.
    """

    return PlaybookInputs(
        design_name="AI SoC 5 GHz Clock Distribution Baseline",
        clock=ClockSourceInputs(
            frequency_ghz=5.0,
            pll_random_jitter_fs=120.0,
            pll_duty_cycle_percent=51.5,
        ),
        interconnect=InterconnectInputs(
            global_wire_length_um=2400.0,
            top_metal_sheet_resistance_mohm_sq=28.0,
            wire_capacitance_af_um=95.0,
            repeater_count=4,
        ),
        noise=SiliconNoiseInputs(
            dynamic_vdd_droop_mv=45.0,
            crosstalk_mode=CrosstalkMode.QUIET,
            shielding_decaps_enabled=True,
        ),
        timing=TimingInputs(
            logic_path_delay_ps=175.0,
            spatial_clock_skew_ps=8.0,
            useful_skew_ps=0.0,
            setup_requirement_ps=8.0,
            hold_requirement_ps=5.0,
        ),
        constants=SiliconModelConstants(),
    )


__all__ = [
    "BudgetRow",
    "ClockNodeResult",
    "ClockSourceInputs",
    "CoreMathResult",
    "CrosstalkMode",
    "HeatmapResult",
    "InterconnectInputs",
    "MathAnalysisRow",
    "PlaybookInputs",
    "PlaybookResults",
    "Recommendation",
    "RiskLevel",
    "SiliconModelConstants",
    "SiliconNoiseInputs",
    "TimingInputs",
    "TimingResult",
    "TimingStatus",
    "WaveformResult",
    "default_ai_soc_5ghz_inputs",
]