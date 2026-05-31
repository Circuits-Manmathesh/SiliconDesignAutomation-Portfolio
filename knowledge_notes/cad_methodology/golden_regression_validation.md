# Golden Regression Validation

## Purpose

This note explains how the Skynet Analog Agent promotes a validated topology into reusable design knowledge.

A topology is not considered golden because it produced one attractive plot. It becomes golden only when the required specifications, real measurements, plots, tables, reports, and public-safe artifacts are complete and consistent.

The core rule:

```text
Measured PASS
+ complete evidence package
+ clean validation gates
+ reusable topology identity
= Golden reusable topology
```

---

## Why Golden Regression Is Needed

A single successful simulation is not enough for a reusable CAD methodology.

A reusable topology must answer:

- Was the design actually simulated?
- Were all required measurements extracted?
- Did every required spec pass?
- Are the plots linked to the measured run?
- Is the folder structure complete?
- Are the notes and reports reviewable?
- Is the design public-safe?
- Can this validated topology seed future projects?

Golden regression validation converts one successful design into reusable methodology knowledge.

---

## Position in the Engine Flow

```text
User Requirement
-> Topology Knowledge Pack
-> LUT-Based Candidate
-> Real Simulation
-> Measurement Extraction
-> Spec Truth Gate
-> Final Evidence Package
-> Golden Regression Validation
-> Topology Maturity Map
-> Reusable Knowledge
```

The golden stage happens after the truth gate. It does not replace simulation; it depends on it.

---

## Golden Promotion Rule

A topology can be promoted only when the following conditions are satisfied:

| Condition | Meaning |
|---|---|
| Topology identity is locked | The result belongs to the correct circuit |
| Required simulations completed | OP/DC/AC/TRAN or required analyses ran |
| Measurements are real | Metrics come from simulation outputs |
| Spec table is complete | No missing required rows |
| Required specs passed | Every required target is satisfied |
| Plot evidence exists | PNG/SVG/JPG plots are available for review |
| Report exists | Summary explains objective, method, result, limitation |
| Metadata exists | Public-safe run context is available |
| No unsafe artifact included | No private model, PDK, raw deck, or confidential file |
| Regression status is clean | Existing validated behavior is not broken |

---

## Topology Maturity Levels

| Maturity Level | Meaning |
|---|---|
| Draft topology | Idea or topology description exists |
| Candidate topology | Sizing/netlist candidate generated |
| Simulated topology | Real simulation completed |
| Truth-gated topology | Measurements extracted and evaluated |
| Validated topology | Required specs passed |
| Golden topology | Complete evidence package generated |
| Mature topology | Can seed future related designs |

This gives the engine a self-learning style: each validated block becomes reusable prior knowledge for the next project.

---

## What Golden Regression Checks

| Check | Example |
|---|---|
| Folder contract | `plots/`, `reports/`, `notes/`, `metadata/` exist |
| Spec coverage | all required specs are evaluated |
| Measurement table | measured values are non-empty |
| Plot package | reviewable result plots exist |
| Report summary | objective, flow, result, limitation are explained |
| Topology identity | common-source data is not mixed with op-amp data |
| Public-safety scan | unsafe or confidential files are excluded |
| Reuse readiness | topology can be referenced by future knowledge packs |

---

## Current Validated Topology Examples

| Topology | Validation Role |
|---|---|
| Inverter 3 GHz Clock Buffer | Unit-cell / switching validation |
| Common-Source Amplifier | Single-ended gain-cell validation |
| Differential Pair / Differential Amplifier | Matched differential-stage validation |
| Two-Stage Operational Amplifier | Compensated multi-stage analog product validation |

These examples demonstrate increasing topology complexity while keeping the same CAD methodology.

---

## Golden Regression vs. One-Time Simulation

| One-Time Simulation | Golden Regression Validation |
|---|---|
| Produces a waveform or plot | Produces full evidence package |
| May not check all specs | Requires complete spec evaluation |
| May be manually interpreted | Uses structured measured metrics |
| May not be reusable | Promotes reusable topology knowledge |
| May hide failed cases | Records failure or limitation behavior |
| May not be public-safe | Enforces sanitized artifact boundary |

Golden regression is therefore a methodology step, not just a result label.

---

## Reusable Topology Knowledge

After promotion, the topology becomes part of the reusable knowledge base.

Reusable knowledge can include:

- design objective,
- topology role,
- known valid operating envelope,
- sizing intuition,
- measured performance,
- spec limitations,
- plots and reports,
- correction behavior,
- future extension notes.

This allows future projects to start from validated prior knowledge instead of starting from zero.

---

## Example: Common-Source Amplifier

The common-source amplifier acts as a gain-cell validation project.

Reusable knowledge from this project includes:

| Knowledge Item | Reuse Value |
|---|---|
| Gain-cell sizing flow | Useful for later analog blocks |
| gm/Id-based candidate selection | Reusable for transistor sizing |
| OP/DC/AC measurement contract | Reusable measurement template |
| Gain/UGB evidence plots | Reviewable validation artifacts |
| Output-bias sanity behavior | Useful for headroom planning |

---

## Example: Differential Pair

The differential pair validates matched-device behavior.

Reusable knowledge from this project includes:

| Knowledge Item | Reuse Value |
|---|---|
| Matched input-device handling | Useful for OTA/op-amp input stages |
| Tail-current checks | Reusable bias sanity check |
| Output common-mode validation | Reusable headroom check |
| Differential AC extraction | Reusable measurement method |
| Balance-error checking | Useful for symmetry validation |

---

## Example: Two-Stage Op-Amp

The two-stage op-amp validates multi-stage analog product behavior.

Reusable knowledge from this project includes:

| Knowledge Item | Reuse Value |
|---|---|
| Gain-budget split | Useful for future OTA/op-amp studies |
| Compensation concept | Useful for stability-aware design |
| Phase-margin validation | Reusable stability check |
| Slew/settling extraction | Reusable transient measurement method |
| Honest design-space limitation | Prevents fake pass for unrealistic targets |

---

## Regression Protection Philosophy

Future changes to sizing logic, measurement extraction, plot generation, or report generation should not break already validated topology behavior.

A golden topology acts as a reference point. If a later engine update changes the result, the difference must be explainable.

Possible regression questions:

| Question | Why It Matters |
|---|---|
| Did the measured gain change unexpectedly? | May reveal extraction/sizing bug |
| Did UGB or PM disappear? | May reveal AC parser or testbench issue |
| Did a required plot vanish? | May reveal report packaging bug |
| Did a previously passed spec fail? | May reveal design or methodology regression |
| Did unsafe files appear? | May reveal publication safety problem |

---

## What This Proves

Golden regression validation shows that the engine is not only producing isolated designs.

It is building:

- reusable topology knowledge,
- reviewable evidence packages,
- regression-protected methodology,
- public-safe technical documentation,
- a growing analog CAD portfolio library.

This is the behavior expected from a mature semiconductor CAD methodology flow.

---

## Public-Safe Boundary

This note describes public methodology and sanitized evidence behavior only. It does not include proprietary PDK files, foundry models, confidential client information, internal company reports, or protected design data.
