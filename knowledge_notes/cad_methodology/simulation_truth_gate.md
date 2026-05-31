# Simulation Truth Gate

## Purpose

This note explains how the Skynet Analog Agent prevents false design validation.

The core rule is simple:

```text
No real simulation -> no valid measurement
No valid measurement -> no spec decision
No spec decision -> no final evidence package
No final evidence package -> no golden topology
```

The engine is designed to behave like a CAD verification flow, not like a script that always prints `PASS`.

---

## Why a Truth Gate Is Needed

In analog automation, the dangerous failure is not only a failed circuit. A more dangerous failure is a **false pass**.

A false pass can happen when:

- a target value is copied from the user specification instead of measured from simulation,
- an old measurement file is reused accidentally,
- a simulation did not run but a report was still generated,
- a parser produced an empty value and the evaluator treated it as valid,
- a plot was generated from stale data,
- a partial result was treated as a complete design pass.

The simulation truth gate blocks these cases.

The engine does not accept a topology as valid until real simulation evidence exists and the required measured values satisfy the user specification.

---

## Position in the Engine Flow

```text
User Requirement
-> Topology Knowledge Pack
-> gm/Id + LUT-Based Device Selection
-> Testbench / Netlist Generation
-> Real Simulation
-> Measurement Extraction
-> Spec Truth Gate
-> Final Evidence Package
```

The truth gate sits after measurement extraction. It uses simulator-derived values, not guessed values.

---

## Engine Stage Mapping

| Stage | Responsibility | Truth-Gate Role |
|---|---|---|
| S8 Design Intent Parser | Converts user requirement into measurable design intent | Defines what must be checked |
| S9 Physics-Aware Sizing Plan | Derives gm/current/headroom/speed targets | Creates expected physical design envelope |
| S10 LUT-Based Initial Sizer | Selects real NMOS/PMOS candidates | Prevents fake or invalid devices |
| S11 Testbench Planner | Decides OP/DC/AC/TRAN analyses | Ensures required simulations are planned |
| S12 Netlist Writer | Generates LTspice-ready netlists | Confirms topology is actually rendered |
| S13 Verification Runner | Runs real LTspice simulation | Produces real simulation artifacts |
| S14 Measurement Extractor | Extracts gain, UGB, PM, current, bias, settling, etc. | Converts simulator output into structured metrics |
| S15 Spec Evaluator | Compares measured metrics against targets | Declares PASS/FAIL |
| S19 Final Report Package | Generates final plots, tables, and summaries | Publishes only evidence-backed results |

---

## Truth Gate Checks

| Check | Purpose | Rejects |
|---|---|---|
| Topology identity check | Confirms the measured result belongs to the requested circuit | Mixed topology results |
| Netlist existence check | Confirms the circuit was actually rendered | Missing or skipped design generation |
| Simulation completion check | Confirms LTspice actually ran | Fake simulation status |
| Measurement source check | Confirms values came from fresh simulation outputs | Stale measurement reuse |
| Non-empty metric check | Confirms every required spec row has a real value | Empty rows and silent parser failure |
| Unit sanity check | Confirms values are interpreted consistently | Wrong unit comparisons |
| Spec comparison check | Confirms measured value satisfies target | Target-only or estimate-only pass |
| Plot evidence check | Confirms reviewable visual evidence exists | Report without plots |
| Final artifact check | Confirms tables, reports, and summaries exist | Incomplete evidence package |

---

## Measurement Contract

Each topology knowledge pack defines what must be measured.

The measurement contract may include:

| Metric Type | Example |
|---|---|
| Bias metrics | output bias, common-mode, tail current, branch current |
| Gain metrics | DC gain, differential gain, open-loop gain |
| Frequency metrics | UGB, bandwidth, phase margin |
| Transient metrics | slew rate, settling time, step response |
| Power metrics | average power, bias current, dynamic power trend |
| Validity metrics | operating region, gm/Id validity, headroom, saturation margin |
| Evidence metrics | required plots, required tables, final report availability |

If a required metric is missing, the truth gate must fail.

---

## Example: Common-Source Amplifier

The common-source amplifier cannot pass just because the target says gain must be above a threshold. It passes only after the engine obtains measured values from simulation.

Typical truth-gated measurements:

| Metric | Measured Result | Decision |
|---|---:|---|
| DC gain | approximately 27.98 dB | PASS |
| UGB | approximately 20.57 MHz | PASS |
| Output bias | valid mid-supply region | PASS |
| Required plots | generated | PASS |

What this proves:

```text
The gain cell is not only theoretically sized.
It is rendered, simulated, measured, and truth-gated.
```

---

## Example: Differential Pair

The differential-pair flow requires more than gain. It must also validate current, common-mode, and balance.

Typical truth-gated measurements:

| Metric | Measured Result | Decision |
|---|---:|---|
| Differential gain | approximately 28.16 dB | PASS |
| UGB | approximately 55.14 MHz | PASS |
| Average power | approximately 8.98 µW | PASS |
| Tail current | approximately 8.98 µA | PASS |
| Output common-mode | approximately 0.497 V | PASS |
| Output balance error | approximately 0 V | PASS |

What this proves:

```text
The engine can evaluate matched differential behavior,
not only single-ended gain.
```

---

## Example: Two-Stage Op-Amp

The two-stage op-amp requires gain, speed, stability, and transient validation.

Typical truth-gated measurements:

| Metric | Measured Result | Decision |
|---|---:|---|
| Open-loop gain | approximately 45–46 dB | PASS |
| UGB | approximately 15.63 MHz | PASS |
| Phase margin | approximately 64.8° | PASS |
| Slew rate | approximately 15.96 V/µs | PASS |
| 1% settling time | approximately 189.5 ns | PASS |

What this proves:

```text
The engine can validate a multi-stage analog product
using real AC and transient simulation evidence.
```

---

## Failure Cases the Truth Gate Must Catch

| Failure Case | Expected Engine Behavior |
|---|---|
| Missing netlist | Stop and report missing generation artifact |
| Missing RAW/CSV/log output | Stop and report simulation output missing |
| Parser returns empty metric | Fail spec evaluation |
| Spec row has no measurement source | Reject the row |
| Plot exists but spec fails | Do not promote topology |
| Measurement belongs to different topology | Reject through topology identity gate |
| Candidate violates LUT/device validity | Reject before final report |
| Required spec is not evaluated | Do not mark project as complete |

---

## Why This Matters for CAD / Methodology

A CAD methodology engineer must be able to build automation that is trustworthy, debuggable, and reproducible.

The truth gate demonstrates:

- measurement integrity,
- artifact sanity,
- stage-level debug visibility,
- spec completeness checking,
- public evidence generation,
- protection against fake pass behavior.

This is the difference between a plotting script and a verification-aware design automation flow.

---

## Public-Safe Boundary

This note explains methodology only. It does not include proprietary PDK data, foundry models, client information, internal company reports, or private simulator files.

Only public-safe methodology, sanitized results, and generated evidence concepts are described.
