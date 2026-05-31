# Closed-Loop Optimization

## Purpose

This note explains how the Skynet Analog Agent handles design failure.

The engine does not randomly change transistor sizes. It reads the failed specification, checks the topology knowledge pack, searches valid gm/Id and LUT-backed candidates, regenerates the testbench, reruns simulation, extracts measurements, and re-evaluates the truth gate.

The main idea:

```text
Measured failure -> physics-aware correction -> new simulation -> measured decision
```

---

## Why Closed-Loop Optimization Is Needed

A first analog candidate often fails. That is normal.

What matters is whether the automation can understand why it failed and how to move toward a better candidate.

Common analog failure examples:

| Failed Behavior | Possible Design Cause |
|---|---|
| Gain too low | low intrinsic gain, poor bias point, short channel effect, low output resistance |
| UGB too low | insufficient gm, excessive capacitance, low bias current |
| Power too high | excessive current or oversized devices |
| Output bias invalid | poor load bias, bad headroom, wrong current ratio |
| Phase margin low | compensation not suitable, second pole too close, wrong current split |
| Slew rate low | insufficient charging/discharging current |
| Common-mode invalid | tail/load bias mismatch |
| Balance error high | asymmetric sizing or mismatched operating point |

Closed-loop optimization turns these failures into structured design decisions.

---

## Position in the Engine Flow

```text
Candidate Design
-> Real Simulation
-> Measurement Extraction
-> Spec Truth Gate
-> Failed Spec Identification
-> Closed-Loop Correction
-> New LUT-Backed Candidate
-> Regenerated Netlist
-> Rerun Simulation
-> Re-evaluate
```

The loop continues only while valid physics-backed candidates exist.

---

## Closed-Loop Flow

```text
1. Run initial candidate
2. Extract measured metrics
3. Compare metrics with user specification
4. Identify failed metric
5. Map failed metric to topology-specific correction rule
6. Query LUT/device candidate space
7. Update sizing, bias, or compensation
8. Regenerate netlist/testbench
9. Rerun real simulation
10. Re-extract measurements
11. Re-evaluate truth gate
12. Stop at PASS or honest design-space exhaustion
```

---

## Failure-to-Correction Map

| Failed Spec | Possible Correction Strategy |
|---|---|
| DC gain too low | increase intrinsic gain, use longer device length, improve bias point, select higher gm/gds candidate |
| UGB too low | increase gm, adjust current, reduce effective capacitance, select faster candidate |
| Power too high | reduce bias current, choose more efficient gm/Id point, rebalance branch currents |
| Output bias too high/low | adjust load device, bias current, current ratio, or output headroom target |
| Phase margin too low | adjust compensation capacitor, second-stage current, pole location, or gain split |
| Slew rate too low | increase available current or reduce compensation load |
| Settling too slow | adjust bandwidth, phase margin, compensation, or drive current |
| Common-mode out of range | adjust tail current, load bias, or device operating point |
| Output balance error high | enforce matched pair sizing and symmetric bias |
| Invalid saturation/headroom | reject candidate and select a physically valid LUT point |
| Missing simulation output | stop and report infrastructure/artifact failure |
| Candidate space exhausted | report honest limitation instead of fake pass |

---

## Engine Correction Knobs

The closed-loop system can adjust topology-specific parameters.

| Knob | Used For |
|---|---|
| gm/Id target | shifts current efficiency, gain, and speed trade-off |
| Device length | improves gain/output resistance or changes capacitance |
| Width / multiplicity | controls current, gm, drive strength, and capacitance |
| Bias current | controls speed, power, slew rate, and operating point |
| Load device selection | affects gain, output bias, and headroom |
| Tail current | controls differential-pair gm, power, and common-mode behavior |
| Compensation capacitor | controls op-amp stability, UGB, and slew/settling trade-off |
| Second-stage current | affects op-amp drive, pole placement, and transient response |
| Output bias target | keeps the circuit inside valid swing/headroom range |
| Topology-specific values | supports future CTLE/OTA/comparator/SerDes extensions |

---

## Why It Is Physics-Aware

The correction loop is not a random optimizer.

Every candidate must remain inside valid device and topology constraints:

| Constraint | Meaning |
|---|---|
| LUT-backed device point | selected device data must exist in the generated LUT |
| gm/Id validity | candidate must operate in meaningful current-efficiency region |
| Region validity | device must not violate expected operating region |
| Headroom validity | bias must fit supply and swing constraints |
| Current validity | branch current must match design budget |
| Capacitance/speed trade-off | UGB and transient behavior must remain physically plausible |
| Topology rule validity | candidate must satisfy topology-specific roles |

If the correction would violate these constraints, the engine rejects the candidate.

---

## Example: Common-Source Amplifier

A common-source amplifier can fail because gain, UGB, current, and output bias trade against each other.

Example correction thinking:

| Failed Metric | Possible Action |
|---|---|
| Gain low | choose higher intrinsic gain candidate or longer device |
| UGB low | increase gm/current or reduce capacitance |
| Output bias invalid | adjust load/bias point |
| Power high | select more current-efficient gm/Id region |

The final validated case demonstrates that the engine can satisfy a gain-cell requirement with measured gain around 27.98 dB and UGB around 20.57 MHz.

---

## Example: Differential Pair

A differential pair needs both gain and bias symmetry.

Example correction thinking:

| Failed Metric | Possible Action |
|---|---|
| Differential gain low | improve gm/load resistance |
| Tail current high | reduce branch current or reselect gm/Id target |
| Common-mode invalid | adjust PMOS load or tail bias |
| Balance error high | enforce symmetric matched device selection |

The validated case demonstrates real differential gain, UGB, common-mode, power, and balance extraction.

---

## Example: Two-Stage Op-Amp

A two-stage op-amp adds stability and transient constraints.

Example correction thinking:

| Failed Metric | Possible Action |
|---|---|
| Gain low | adjust first/second stage gain budget |
| UGB low | increase gm or adjust compensation |
| Phase margin low | increase compensation or shift pole locations |
| Slew rate low | increase current or reduce compensation load |
| Settling slow | rebalance bandwidth and phase margin |

In development, an aggressive 30 MHz UGB target exposed a realistic design-space limitation. The engine did not create a fake pass. After V1 retargeting, the design passed gain, UGB, phase margin, slew-rate, settling, and reporting checks.

---

## Stop Conditions

The loop stops under two clean conditions.

### 1. Validated PASS

```text
All required specs pass
+ real measurements exist
+ plots/tables/reports generated
= final evidence package
```

### 2. Honest Limitation

```text
No valid LUT-backed candidate remains
or topology constraints cannot satisfy target
= report design-space limitation
```

This is important. A mature CAD system must be able to say:

```text
The requested specification is not reachable within the current device/topology/design-space constraints.
```

---

## Why This Matters for CAD / Methodology

Closed-loop optimization demonstrates:

- topology-aware debug,
- measured failure analysis,
- physics-aware correction,
- repeatable iteration,
- candidate-space boundary awareness,
- honest failure reporting,
- reusable methodology.

This is stronger than a one-shot design script because it shows a path from failure to engineering decision.

---

## Public-Safe Boundary

This note describes the public methodology only. It does not disclose private implementation details, proprietary models, confidential client data, or protected simulator decks.
