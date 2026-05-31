# Silicon Design Automation Portfolio

## Physics-Aware Analog / Mixed-Signal CAD Methodology Portfolio

This repository is a public, non-confidential technical portfolio focused on **analog / mixed-signal IC design automation**, **semiconductor CAD methodology**, **gm/Id lookup-table based sizing**, **SPICE simulation evidence**, **clock-distribution architecture**, **RFIC design study**, and **reusable topology validation**.

The goal is to show how device physics, circuit knowledge, scripting, simulation, measurement extraction, validation gates, and reusable topology thinking can be combined into a structured silicon-design methodology.

---

## 3-Minute Reviewer Path

For a quick technical review, start here:

1. Review the Skynet Analog Agent architecture below.
2. Check the gm/Id LUT device-physics foundation.
3. Check the validated analog design evidence section.
4. Open the common-source amplifier, differential pair, and two-stage op-amp evidence folders.
5. Review the CAD methodology notes: simulation truth gate, closed-loop optimization, and golden regression validation.
6. Review the clock-distribution playbook for SoC timing and methodology context.
7. Review the RFIC research track for mm-wave design background.

---

## Core Theme

**From device physics to circuit verification.**

```text
User Requirement
→ Topology Knowledge Pack
→ gm/Id + LUT-Based Device Selection
→ Testbench / Netlist Generation
→ Real Simulation
→ Measurement Extraction
→ Spec Truth Gate
→ Closed-Loop Correction
→ Final Evidence Package
→ Reusable Golden Topology

```

---

## System Architecture

The following architecture model explains the **Skynet Analog Agent** as a deterministic, physics-aware analog CAD methodology engine.

![Skynet Analog Agent Architecture](architecture/skynet_analog_agent_architecture.png)

Start here:

- [`architecture/`](architecture/)

---

## gm/Id LUT Device Physics Foundation

The Skynet Analog Agent uses a device-level LUT database as the physics foundation for transistor sizing. This section shows how the engine connects device physics, gm/Id methodology, LUT-backed operating-point selection, and real LTspice-verified analog design.

This section is intentionally placed immediately after the architecture diagram because the LUT is the device-physics memory behind the validated analog projects shown later.

### LUT Generation and gm/Id Methodology in Our Engine

- Our engine uses a **device-level LUT database** as the physics foundation for transistor sizing. Instead of randomly choosing `W/L/current` values, the engine queries pre-characterized NMOS/PMOS operating points and selects candidates based on real device behavior.

- The LUT is generated from transistor sweeps over **bias, length, multiplicity, and process corner conditions**. For each NMOS/PMOS device point, the LUT stores key analog design quantities such as:

  - drain current `Id`
  - transconductance `gm`
  - output conductance `gds`
  - `gm/Id`
  - `gm/gds`
  - intrinsic gain
  - output resistance
  - capacitances such as `cgg`, `cgs`, `cgd`
  - threshold/overdrive information
  - `ft`
  - current density
  - power
  - region flag
  - saturation/headroom validity

- The current Skynet engine reads the production LUT from:

```text
lut_characterizer\generated_lut

```

- The LUT contains both **NMOS and PMOS device physics**, with thousands of valid operating-point rows. In our validated engine runs, the LUT service discovered around:

```text
NMOS rows ≈ 24,640
PMOS rows ≈ 24,640

```

- The LUT grid has been matured around practical gm/Id design needs:

  - multiple transistor lengths
  - multiple `VGS/VSG` bias points
  - multiple `VDS/VSD` operating points
  - current-density awareness
  - region/saturation flags
  - valid/invalid operating-point filtering
  - PMOS/NMOS sign-normalized quantities for easier design automation

- In the broader LUT framework, the device sweep philosophy supports grids such as:

  - `VGS/VSG` sweep across the usable supply range
  - `VDS/VSD` sweep across output-headroom regions
  - multiple channel lengths for gain/bandwidth trade-off
  - multiplicity `m` scaling for layout-aware current and width scaling
  - process corners such as `TT/SS/FF` for robustness

### Representative LUT Sweep Grid

| Sweep Variable | Representative Grid / Meaning |
| --- | --- |
| `VGS / VSG` | 0 V to 1.1 V, step 0.1 V |
| `VDS / VSD` | 0 V to 1.25 V, step 0.25 V |
| `VBody` | 0 V, 0.3 V, 0.5 V |
| `L` | 50 nm, 100 nm, 200 nm, 600 nm, 900 nm, 1 µm |
| `W` | 1 µm reference width |
| `m` | 1 to 10 multiplicity for layout-aware scaling |

For the current public portfolio view, the landing page shows representative `VDS/VSD = 0.5 V` gm/Id-related plots for NMOS and PMOS devices. The broader engine architecture is capable of expanding this same methodology across separate `TT`, `SS`, and `FF` process corners and temperature points such as `-40 C`, `27 C`, and `125 C`, as long as the corresponding public-safe LUT artifacts are generated and placed in the portfolio structure.

### How the Engine Converts Specs into LUT Queries

- The gm/Id methodology is directly connected to this LUT. The engine first converts the user requirement into circuit-level targets:

  - required gain
  - required UGB/bandwidth
  - required load driving
  - power/current limit
  - output swing/headroom
  - topology-specific bias constraints

- Then it derives sizing quantities using gm/Id logic:

```text
Required bandwidth/load → required gm
Required gm and selected gm/Id → required Id
Required Id and LUT current density → required W/m
Gain target → gm/gds and gds/Id constraint
Swing/headroom target → valid VDS/VSD and saturation margin

```

- After this, the engine queries the LUT and filters candidates using:

  - correct device type: NMOS/PMOS
  - gm/Id target range
  - length target
  - current target
  - region validity
  - saturation margin
  - gm/gds requirement
  - ft margin
  - width/current-density limits
  - output headroom compatibility

- This makes the sizing process **deterministic and physics-aware**. The engine does not simply tune numbers until a plot looks good. It searches only valid device operating points available in the LUT.

- The LUT also helps the closed-loop optimizer. If a design fails gain, bandwidth, output bias, phase margin, eye opening, or power, the engine uses the LUT to move toward physically meaningful alternatives rather than random guesses.

- In short, the LUT acts as the **device physics memory** of the engine, and gm/Id acts as the **design reasoning method**. Together, they allow the engine to size devices, reject invalid regions, explain failures, and converge toward real LTspice-verified analog designs.

### NMOS gm/Id Representative Plots at VDS = 0.5 V

| Plot | Plot |
| --- | --- |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/01_gmid_vs_vctrl_nmos_full_vds_0p55V.png" width="430"><br><sub>01 gm/Id Vs Vctrl Nmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/02_gmid_vs_vov_nmos_full_vds_0p55V.png" width="430"><br><sub>02 gm/Id Vs Vov Nmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/03_id_over_w_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>03 Id Over W Vs gm/Id Nmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/04_gm_over_w_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>04 Gm Over W Vs gm/Id Nmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/05_gm_over_gds_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>05 Gm Over Gds Vs gm/Id Nmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/06_gds_over_id_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>06 Gds Over Id Vs gm/Id Nmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/07_gain_db_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>07 Gain Db Vs gm/Id Nmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/08_ft_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>08 ft Vs gm/Id Nmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/09_ft_gmid_product_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>09 ft gm/Id Product Vs gm/Id Nmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/nmos_gmid_plots/vds_0p55V/10_cgg_over_w_vs_gmid_nmos_full_vds_0p55V.png" width="430"><br><sub>10 Cgg Over W Vs gm/Id Nmos Full VDS 0.55v</sub> |

### PMOS gm/Id Representative Plots at VSD = 0.5 V

| Plot | Plot |
| --- | --- |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/01_gmid_vs_vctrl_pmos_full_vds_0p55V.png" width="430"><br><sub>01 gm/Id Vs Vctrl Pmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/02_gmid_vs_vov_pmos_full_vds_0p55V.png" width="430"><br><sub>02 gm/Id Vs Vov Pmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/03_id_over_w_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>03 Id Over W Vs gm/Id Pmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/04_gm_over_w_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>04 Gm Over W Vs gm/Id Pmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/05_gm_over_gds_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>05 Gm Over Gds Vs gm/Id Pmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/06_gds_over_id_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>06 Gds Over Id Vs gm/Id Pmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/07_gain_db_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>07 Gain Db Vs gm/Id Pmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/08_ft_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>08 ft Vs gm/Id Pmos Full VDS 0.55v</sub> |
| <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/09_ft_gmid_product_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>09 ft gm/Id Product Vs gm/Id Pmos Full VDS 0.55v</sub> | <img src="projects/01_skynet_analog_agent/lut_gmid_database/pmos_gmid_plots/vds_0p55V/10_cgg_over_w_vs_gmid_pmos_full_vds_0p55V.png" width="430"><br><sub>10 Cgg Over W Vs gm/Id Pmos Full VDS 0.55v</sub> |

### Why This Matters for the Validated Projects

| Validated Project | How the LUT Helps |
| --- | --- |
| Common-source amplifier | Converts gain/UGB/load requirements into gm, current, intrinsic-gain and headroom-aware candidates |
| Differential pair | Selects matched device candidates while checking gm/Id, current, common-mode and saturation constraints |
| Two-stage op-amp | Supports gm budgeting, gain-stage sizing, compensation trade-off, slew-rate/power awareness and failure correction |
| Inverter / clock buffer | Supports unit-cell drive/current/timing exploration with reusable device-level characterization |

This is the key difference between a simple automation script and a physics-aware CAD methodology engine.

---

## Validated Analog Design Evidence

The following analog design projects were generated and validated using the same staged Skynet Analog Agent flow:

```text
User Requirement
→ Topology Knowledge Pack
→ gm/Id + LUT-Based Device Selection
→ LTspice Netlist Generation
→ Real Simulation
→ Measurement Extraction
→ Spec Truth Gate
→ Closed-Loop Correction
→ Final Evidence Package
→ Golden Regression / Topology Maturity Map

```

This is not a manual plot collection. Each design is treated as a topology-driven CAD task. The engine reads the user specification, loads the corresponding topology knowledge pack, derives physics-aware sizing targets, selects LUT-backed devices, generates LTspice simulations, extracts real measurements, checks the required specifications, and iterates when needed.

### 1. Common-Source Amplifier

**Status:** `VALIDATED / PASS`

**Problem solved:**

Validate a short-channel analog gain cell where gain, bandwidth, output bias, power, and device operating region trade against each other.

**User specification used by the engine:**

| Parameter | Target |
| --- | --- |
| Technology setup | 50 nm educational CMOS model |
| Supply | Around 1.0 V |
| Load | Capacitive load included in the testbench |
| DC gain | Approximately ≥ 26 dB |
| UGB | Approximately ≥ 20 MHz |
| Output bias | Valid operating range |
| Power | Below project limit |
| Device validity | LUT-backed, physically valid operating point |

**Engine process:**

The common-source knowledge pack defines topology structure, sizing rules, device roles, testbench requirements, measurement rules, and report plots. The engine derives the required gm and bias current from the target UGB and load, selects NMOS/PMOS candidates from the gm/Id LUT, generates LTspice OP/DC/AC/transient testbenches, extracts measurements from real simulator outputs, and evaluates the design using the spec truth gate.

**Validated result:**

| Metric | Measured Result | Status |
| --- | --- | --- |
| DC gain | ~27.98 dB | `PASS` |
| UGB | ~20.57 MHz | `PASS` |
| Output bias | Valid mid-supply region | `PASS` |
| Gain + bandwidth target | Met | `PASS` |

**What this proves:**

The engine can convert a simple analog gain-cell requirement into a reproducible transistor-level design using gm/Id, LUT-backed device selection, and real simulation measurements instead of random sizing.

**Evidence links:**

- [Full project folder](projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/)
- [Plots](projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/plots/)
- [Reports](projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/reports/)
- [Notes](projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/notes/)
- [Screenshots](projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/screenshots/)
- [Metadata](projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/metadata/)

**Verified result plots:**

| Plot | Plot |
| --- | --- |
| <img src="projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/plots/02_dc_transfer_vout_vs_vin.png" width="430"><br><sub>02 DC Transfer Vout Vs Vin</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/plots/07_ac_bode_gain.png" width="430"><br><sub>07 AC Bode Gain</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/01_common_source_amplifier/plots/08_ac_phase_diagnostic.png" width="430"><br><sub>08 AC Phase Diagnostic</sub> |  |

---

### 2. Differential Pair / Differential Amplifier

**Status:** `VALIDATED / PASS`

**Problem solved:**

Validate a differential input stage with real differential gain, output common-mode, tail current, output balance, power, and device operating-point extraction.

**User specification used by the engine:**

| Parameter | Target |
| --- | --- |
| Differential gain | ≥ 20 dB |
| UGB | ≥ 50 MHz |
| Power | ≤ 300 µW |
| Tail current | ≤ 150 µA |
| Output common-mode | ~0.35 V to 0.70 V |
| Output balance error | ≤ 20 mV |
| Measurement source | Real OP/DC/AC/transient simulation |
| Device validity | gm/Id and saturation checks required |

**Engine process:**

The differential-pair knowledge pack defines matched NMOS input devices, PMOS load behavior, tail-current constraints, common-mode checks, balance checks, and differential measurement rules. The engine selects matched device groups from the LUT, verifies OP bias and region validity, extracts differential gain and UGB from real AC simulation, checks transient behavior, and rejects fake or empty spec rows.

**Validated result:**

| Metric | Measured Result | Status |
| --- | --- | --- |
| Differential gain | ~28.16 dB | `PASS` |
| UGB | ~55.14 MHz | `PASS` |
| Average power | ~8.98 µW | `PASS` |
| Tail current | ~8.98 µA | `PASS` |
| Output common-mode | ~0.497 V | `PASS` |
| Output balance error | ~0 V | `PASS` |

**What this proves:**

The engine can handle matched differential devices, common-mode constraints, tail-current checks, balance checks, and differential AC extraction using real simulation-backed measurements.

**Evidence links:**

- [Full project folder](projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/)
- [Plots](projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/plots/)
- [Reports](projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/reports/)
- [Notes](projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/notes/)
- [Screenshots](projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/screenshots/)
- [Metadata](projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/metadata/)

**Verified result plots:**

| Plot | Plot |
| --- | --- |
| <img src="projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/plots/02_dc_differential_transfer.png" width="430"><br><sub>02 DC Differential Transfer</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/plots/03_dc_output_common_mode_and_balance.png" width="430"><br><sub>03 DC Output Common Mode And Balance</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/plots/04_ac_differential_gain_ugb.png" width="430"><br><sub>04 AC Differential Gain UGB</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/plots/05_tran_differential_step_response.png" width="430"><br><sub>05 TRAN Differential Step Response</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/02_differential_pair/plots/08_ac_phase_diagnostic.png" width="430"><br><sub>08 AC Phase Diagnostic</sub> |  |

---

### 3. Two-Stage Operational Amplifier

**Status:** `VALIDATED / PASS`

**Problem solved:**

Build a higher-level analog product using matured common-source and differential-pair concepts: a two-stage Miller-compensated op-amp with gain, UGB, phase margin, slew rate, settling, power, and operating-point validation.

**User specification used by the engine:**

| Parameter | Target |
| --- | --- |
| Supply | Around 1.0 V |
| Open-loop gain | ≥ 40 dB |
| UGB | ≥ 10 MHz for validated V1 demo |
| Phase margin | ≥ 55° |
| Output bias | Valid operating range |
| Transient behavior | Slew-rate and settling required |
| Final plots | PNG-only public evidence |
| Verification | Real OP/DC/AC/transient LTspice simulation |
| Device sizing | LUT-backed |

**Engine process:**

The two-stage op-amp knowledge pack defines the input differential stage, second gain stage, compensation capacitor, biasing rules, measurement extraction, and final plots. The engine derives gm/Id targets, compensation seed, input-stage current, second-stage current, gain budget, UGB target, and output bias target. It then generates LTspice testbenches, extracts gain, UGB, phase margin, power, slew rate, and settling from real simulation outputs, and performs closed-loop correction when required.

**Validated result:**

| Metric | Measured Result | Status |
| --- | --- | --- |
| Open-loop gain | ~45–46 dB | `PASS` |
| UGB | ~15.63 MHz | `PASS` |
| Phase margin | ~64.8° | `PASS` |
| Slew rate | ~15.96 V/µs | `PASS` |
| 1% settling time | ~189.5 ns | `PASS` |
| V1 design target | Met | `PASS` |

**What this proves:**

The engine can move beyond primitive cells and design a compensated multi-stage analog product. The earlier aggressive 30 MHz UGB target exposed a valid design-space limitation, and the engine reported the limitation instead of producing a fake pass. After realistic V1 retargeting, the design passed gain, stability, transient, and reporting checks.

**Evidence links:**

- [Full project folder](projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/)
- [Plots](projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/)
- [Reports](projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/reports/)
- [Notes](projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/notes/)
- [Screenshots](projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/screenshots/)
- [Metadata](projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/metadata/)

**Verified result plots:**

| Plot | Plot |
| --- | --- |
| <img src="projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/02_dc_transfer_vout_vs_vin.png" width="430"><br><sub>02 DC Transfer Vout Vs Vin</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/03_ac_gain_phase_bode.png" width="430"><br><sub>03 AC Gain Phase Bode</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/04_phase_margin_marker.png" width="430"><br><sub>04 Phase Margin Marker</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/04_tran_input_output_waveform.png" width="430"><br><sub>04 TRAN Input Output Waveform</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/05_unity_gain_transient_step.png" width="430"><br><sub>05 Unity Gain Transient Step</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/06_slew_rate_and_settling.png" width="430"><br><sub>06 Slew Rate And Settling</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/03_two_stage_opamp/plots/07_ac_bode_gain.png" width="430"><br><sub>07 AC Bode Gain</sub> |  |

---

### 4. Inverter 3 GHz Clock Buffer

**Status:** `VALIDATED UNIT CELL`

**Problem solved:**

Validate a reusable high-speed switching unit cell before moving to larger analog and clock-buffer studies.

**User specification used by the engine:**

| Parameter | Target |
| --- | --- |
| Target use | 3 GHz clock-buffer / switching-cell demonstration |
| Verification | Public-safe plots, tables and report artifacts |
| Role in engine | Unit-cell validation before larger topology promotion |

**Engine process:**

The inverter/clock-buffer validation checks whether the flow can generate a simple topology, run real simulation, extract timing/power-style evidence, and promote a clean reusable block.

**Validated result:**

| Metric | Measured Result | Status |
| --- | --- | --- |
| Validation status | Evidence available in project folder | `UNIT-CELL VALIDATED` |

**What this proves:**

This project shows the engine can start from a simple reusable unit cell before scaling toward common-source, differential and op-amp level designs.

**Evidence links:**

- [Full project folder](projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/)
- [Plots](projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/plots/)
- [Reports](projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/reports/)
- [Notes](projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/notes/)
- [Screenshots](projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/screenshots/)

**Verified result plots:**

| Plot | Plot |
| --- | --- |
| <img src="projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/plots/best_waveform_stacked.png" width="430"><br><sub>Best Waveform Stacked</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/plots/delay_power_tradeoff.png" width="430"><br><sub>Delay Power Tradeoff</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/plots/duty_cycle_check.png" width="430"><br><sub>Duty Cycle Check</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/plots/gain_phase_response.png" width="430"><br><sub>Gain Phase Response</sub> |
| <img src="projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/plots/gain_phase_response_vm.png" width="430"><br><sub>Gain Phase Response Vm</sub> | <img src="projects/01_skynet_analog_agent/validated_topologies/00_inverter_3ghz_clock_buffer/plots/vout_waveform.png" width="430"><br><sub>Vout Waveform</sub> |

---

## How the Engine Handles Failure

The engine does not silently hide design failures. Each stage writes a structured artifact that explains what passed, what failed, and which input caused the issue.

Example failure types include:

- missing LUT candidate
- invalid PMOS/NMOS operating region
- missing netlist
- missing RAW simulation output
- empty spec evaluation
- fake or stale measurement source
- failed gain / UGB / power / headroom / settling requirement
- exhausted candidate search space

This behavior is intentional. It shows that the framework behaves like a CAD verification system, not like a script that always prints `PASS`.

---

## Closed-Loop Optimization Philosophy

If a design fails, the engine does not randomly change device sizes. It reads the failed spec, checks the topology knowledge pack, and applies physics-aware correction rules.

The closed-loop engine can adjust:

- gm/Id target
- device length
- device width / multiplicity
- bias current
- load device selection
- compensation value
- output bias / headroom
- topology-specific parameters

After every candidate update, the engine reruns the real simulation chain:

```text
Netlist Generation
→ LTspice Simulation
→ Measurement Extraction
→ Spec Evaluation
→ Final Truth Gate

```

The loop stops only when all required specs pass with real measurements or the valid physics/LUT candidate space is exhausted.

---

## Why These Projects Matter

The same engine flow successfully handled:

- a single-ended analog gain cell
- a matched differential amplifier
- a compensated two-stage op-amp

This demonstrates that the framework is not hardcoded for one circuit. The topology knowledge pack changes, but the CAD methodology remains the same. Each validated topology becomes a reusable design capability for future circuits such as CTLE, OTA, current mirror, comparator, and SerDes receiver blocks.

---

## Featured Portfolio Modules

| Module | Purpose | Status |
| --- | --- | --- |
| [`Skynet Analog Agent`](projects/01_skynet_analog_agent/) | Physics-aware analog CAD methodology engine using topology packs, gm/Id LUTs, simulation truth gates, closed-loop correction, and reusable topology validation. | Active / Core |
| [`Interactive SoC Clock Distribution Playbook`](projects/02_interactive_soc_clock_playbook/) | Architecture-level study of clock distribution from PLL to flip-flop, including slew, load, delay, skew, jitter, duty cycle, setup/hold, and clock power. | Active / Separate Project |
| [`RFIC Research and Thesis Track`](projects/03_rfic_research_and_thesis/) | Public-safe RFIC study based on 47 GHz power amplifier design in 130 nm SiGe/BiCMOS technology. | Public-Safe Study |
| [`Cadence Design Projects`](projects/04_cadence_design_projects/) | Cadence-based high-speed analog design summaries including CTLE and future SerDes receiver blocks. | Public-Safe Summaries |
| [`Miscellaneous Circuit Studies`](projects/05_miscellaneous_circuit_studies/) | Basic-to-deep studies such as RC circuits, current mirrors, MOS behavior, and analog building blocks. | Growing Library |

---

## Skynet Analog Agent

Skynet Analog Agent is the main physics-aware analog design automation methodology project.

It connects:

- user circuit requirements
- topology knowledge packs
- gm/Id and LUT-based device selection
- topology-aware testbench and netlist generation
- real SPICE simulation
- measurement extraction
- specification truth gates
- closed-loop correction
- reusable golden topology validation

Current topology track:

- Inverter 3 GHz clock-buffer unit cell
- Common-source amplifier
- Differential pair
- Two-stage op-amp
- CTLE equalizer 2 Gb/s as upcoming / in refinement

Start here:

- [`projects/01_skynet_analog_agent/`](projects/01_skynet_analog_agent/)

---

## Interactive SoC Clock Distribution Playbook

This is a separate architecture-level project for understanding clock distribution from **PLL to flip-flop**.

Study areas:

- PLL / clock source
- root clock buffer
- global clock spine / H-tree
- regional and local clock distribution
- clock gating
- leaf buffers
- flip-flop and macro loads
- slew, load, delay, skew, jitter, duty-cycle distortion, setup/hold margin, and clock power

Start here:

- [`projects/02_interactive_soc_clock_playbook/`](projects/02_interactive_soc_clock_playbook/)

---

## Knowledge Notes / Technical Blog

The knowledge notes section works like a technical blog. It explains the circuit, device-physics, and CAD-methodology concepts behind the portfolio.

### Device Physics

- [`MOS current behavior`](knowledge_notes/device_physics/)
- [`gm/Id methodology`](knowledge_notes/device_physics/)
- [`LUT-based device selection`](knowledge_notes/device_physics/)

### Analog Building Blocks

- [`Common-source amplifier`](knowledge_notes/analog_blocks/)
- [`Differential pair`](knowledge_notes/analog_blocks/)
- [`Current mirror`](knowledge_notes/analog_blocks/)
- [`Two-stage op-amp compensation`](knowledge_notes/analog_blocks/)

### High-Speed Analog

- [`CTLE equalizer basics`](knowledge_notes/high_speed_analog/)
- [`SerDes receiver frontend notes`](knowledge_notes/high_speed_analog/)

### Clock Distribution

- [`PLL to flip-flop roadmap`](knowledge_notes/clock_distribution/)
- [`Clock slew, load, delay, skew and jitter`](knowledge_notes/clock_distribution/)

### RFIC Design

- [`47 GHz RF power amplifier overview`](knowledge_notes/rfic_design/)
- [`OP1dB and linearity`](knowledge_notes/rfic_design/)
- [`Impedance matching`](knowledge_notes/rfic_design/)

### CAD Methodology

- [`CAD methodology overview`](knowledge_notes/cad_methodology/)
- [`Simulation truth gate`](knowledge_notes/cad_methodology/simulation_truth_gate.md)
- [`Closed-loop optimization`](knowledge_notes/cad_methodology/closed_loop_optimization.md)
- [`Golden regression validation`](knowledge_notes/cad_methodology/golden_regression_validation.md)

Start here:

- [`knowledge_notes/`](knowledge_notes/)

---

## Evidence Packages

The evidence section contains selected public-safe outputs:

- generated plots
- measurement tables
- report summaries
- screenshots
- demo assets

Start here:

- [`evidence/`](evidence/)

---

## Public Disclosure

This repository presents an open, educational, non-confidential methodology portfolio. It does not include proprietary PDK files, foundry models, confidential client data, commercial IP, internal company reports, restricted technology files, private scripts, or protected customer information.

All published diagrams, notes, plots, and documentation are sanitized artifacts intended to explain methodology, circuit understanding, and software architecture.

More details:

- [`PUBLIC_DISCLOSURE.md`](PUBLIC_DISCLOSURE.md)

---

## How to Review

- Recruiters: start with this landing page and validated evidence snapshots.
- Analog / mixed-signal reviewers: start with Skynet Analog Agent, gm/Id notes, and validated topology evidence.
- CAD / methodology reviewers: start with architecture, truth gates, closed-loop validation, and failure-handling flow.
- RFIC reviewers: start with RFIC Research and Thesis Track.
- SoC / timing reviewers: start with Interactive SoC Clock Distribution Playbook.

Guide:

- [`HOW_TO_REVIEW_THIS_PORTFOLIO.md`](HOW_TO_REVIEW_THIS_PORTFOLIO.md)

---

## Roadmap

- [`PORTFOLIO_ROADMAP.md`](PORTFOLIO_ROADMAP.md)

---

_Last major portfolio update: May 2026_
