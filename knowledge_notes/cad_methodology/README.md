# CAD Methodology

## Physics-Aware Analog Design Automation Methodology

This section explains the CAD methodology behind the Skynet Analog Agent. The goal is not only to design one circuit, but to demonstrate a reusable, deterministic, and verification-aware analog design flow.

The methodology treats analog circuit design as a staged CAD problem:

```text
User Requirement
-> Topology Knowledge Pack
-> gm/Id + LUT-Based Device Selection
-> Testbench / Netlist Generation
-> Real Simulation
-> Measurement Extraction
-> Spec Truth Gate
-> Closed-Loop Correction
-> Final Evidence Package
-> Golden Regression Validation
-> Reusable Topology Knowledge
```

![Skynet Analog Agent Architecture](../../architecture/skynet_analog_agent_architecture.png)

---

## Why This CAD Methodology Exists

Analog design often fails silently when the workflow depends only on manual sizing, estimated equations, stale plots, or incomplete measurements.

This methodology is built around a stricter rule:

> A design is not considered valid until the measured simulation evidence satisfies the user specification through a truth-gated evaluation flow.

The engine therefore separates:

| Layer                       | Responsibility                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------ |
| User requirement            | Defines target gain, bandwidth, current, swing, power, stability, or timing behavior |
| Topology knowledge pack     | Defines circuit structure, device roles, sizing rules, measurements, and plots       |
| gm/Id + LUT engine          | Converts device physics into valid sizing candidates                                 |
| Netlist/testbench generator | Creates topology-aware simulation artifacts                                          |
| Simulation runner           | Executes real LTspice simulation                                                     |
| Measurement extractor       | Extracts metrics from simulation outputs                                             |
| Spec truth gate             | Decides PASS/FAIL from real measured values                                          |
| Closed-loop optimizer       | Adjusts design variables when specs fail                                             |
| Golden regression           | Promotes only validated reusable topologies                                          |

---

## 1. Simulation Truth Gate

The simulation truth gate prevents the engine from producing fake or stale results.

A design cannot pass only because the target value was written in a specification file. It must pass because the simulator output was generated, parsed, measured, and checked.

### Truth Gate Checks

| Check                           | Purpose                                          |
| ------------------------------- | ------------------------------------------------ |
| Netlist exists                  | Confirms that the topology was actually rendered |
| Simulation completed            | Confirms real simulator execution                |
| RAW/CSV/log evidence exists     | Confirms measurable output artifacts             |
| Measurement source is valid     | Prevents stale or fake measurement reuse         |
| Required metrics are non-empty  | Prevents empty spec rows from passing            |
| Measured value satisfies target | Confirms actual spec compliance                  |
| Plot evidence exists            | Confirms public evidence was generated           |

### Example Metrics Checked

| Topology                | Example Measurements                                             |
| ----------------------- | ---------------------------------------------------------------- |
| Common-source amplifier | DC gain, UGB, output bias, power                                 |
| Differential pair       | Differential gain, UGB, common-mode, balance error, tail current |
| Two-stage op-amp        | Open-loop gain, UGB, phase margin, slew rate, settling time      |
| Inverter / clock buffer | Delay, duty cycle, waveform integrity, power trend               |

### Why It Matters

In a real CAD/methodology environment, the dangerous failure mode is not only a failed design. The more dangerous case is a false pass.

The simulation truth gate ensures:

```text
No real simulation -> no valid measurement
No valid measurement -> no spec pass
No spec pass -> no golden topology
```

---

## 2. Closed-Loop Optimization

The closed-loop optimizer is used when a candidate design fails one or more required specifications.

The engine does not randomly resize devices. It reads the failed spec, checks the topology knowledge pack, and applies physics-aware correction rules.

### Closed-Loop Flow

```text
Measured Spec Fails
-> Identify failed metric
-> Check topology-specific correction rules
-> Select new LUT-backed device candidate
-> Regenerate netlist/testbench
-> Rerun LTspice simulation
-> Extract new measurements
-> Re-evaluate truth gate
```

### What the Loop Can Adjust

| Design Variable             | Example Purpose                                           |
| --------------------------- | --------------------------------------------------------- |
| gm/Id target                | Shift current efficiency or speed region                  |
| Device length               | Improve gain, output resistance, or capacitance trade-off |
| Device width / multiplicity | Adjust current, gm, capacitance, and drive strength       |
| Bias current                | Tune bandwidth, slew rate, and power                      |
| Load device selection       | Improve gain, headroom, and output bias                   |
| Compensation capacitor      | Improve op-amp stability and phase margin                 |
| Output bias target          | Keep the design inside valid swing/headroom range         |

### Stop Conditions

The loop stops only when:

1. all required specs pass using real measurements, or
2. the valid LUT/device candidate space is exhausted.

This is important because the engine must be honest about physics limitations. If a target is unrealistic for the available device space, the engine should report the limitation instead of generating a fake pass.

---

## 3. Golden Regression Validation

A topology becomes reusable only after it passes the validation flow cleanly.

Golden regression means the topology is not just a one-time result. It becomes a reusable reference for future designs.

### Promotion Rule

```text
Spec PASS
+ valid measured evidence
+ complete plots/tables/report
+ clean topology identity
+ no stale measurement source
+ no missing required artifact
= Golden reusable topology
```

### Golden Topology Artifacts

| Artifact                | Purpose                                          |
| ----------------------- | ------------------------------------------------ |
| Final measurement table | Shows measured performance                       |
| Spec pass/fail table    | Shows requirement-by-requirement result          |
| PNG plot evidence       | Makes result reviewable                          |
| Project summary         | Explains design objective and outcome            |
| Metadata                | Records public-safe run context                  |
| Limitations note        | Documents what the topology cannot yet guarantee |

### Current Validated Topology Examples

| Topology                    | Validation Role                                   |
| --------------------------- | ------------------------------------------------- |
| Inverter 3 GHz clock buffer | Unit-cell / timing-style validation               |
| Common-source amplifier     | Single-ended analog gain-cell validation          |
| Differential pair           | Matched differential-stage validation             |
| Two-stage op-amp            | Multi-stage compensated analog product validation |

---

## 4. How This Looks Like a CAD/Methodology Flow

This project is not intended to look like a set of disconnected analog plots. It is organized like a CAD methodology system.

| CAD Concern       | How the Engine Handles It                                                           |
| ----------------- | ----------------------------------------------------------------------------------- |
| Collateral sanity | Uses topology knowledge packs and expected artifact contracts                       |
| Reproducibility   | Uses project manifests, structured folders, and generated reports                   |
| Debug visibility  | Writes stage-level outputs and failure reasons                                      |
| Measurement trust | Uses real simulation extraction and truth-gated evaluation                          |
| Automation        | Generates testbenches, runs simulation, extracts measurements, and creates evidence |
| Reuse             | Promotes validated blocks into a golden topology library                            |
| Public safety     | Publishes only sanitized plots, notes, and summaries                                |

---

## 5. Why This Matters for Semiconductor Roles

This methodology demonstrates skills relevant to analog design, CAD/methodology, IP enablement, and design automation roles.

### For Analog / Mixed-Signal Design

It shows the ability to connect device physics, gm/Id sizing, headroom, gain, bandwidth, power, stability, and simulation evidence.

### For CAD / Methodology

It shows the ability to build structured flows, sanity checks, measurement gates, automation scripts, report generation, failure handling, and reusable validation logic.

### For IP Enablement

It shows how a topology can be treated as a reusable design asset only after collateral, simulation, measurement, and reporting evidence are complete.

### For Research Review

It shows a repeatable framework where the topology changes, but the methodology remains consistent.

---

## 6. Deep-Dive Notes

Planned detailed notes:

* [`simulation_truth_gate.md`](simulation_truth_gate.md)
* [`closed_loop_optimization.md`](closed_loop_optimization.md)
* [`golden_regression_validation.md`](golden_regression_validation.md)

These notes will expand the methodology into individual reviewable topics.

---

## Public-Safe Disclosure

This CAD methodology page is a public, educational, non-confidential explanation of the automation flow. It does not include proprietary PDK files, foundry models, confidential client data, commercial IP, internal reports, or protected technology information.
