# Silicon Design Automation Portfolio

## Physics-Aware Analog / Mixed-Signal CAD Methodology Portfolio

This repository is a public, non-confidential technical portfolio focused on **analog / mixed-signal IC design automation**, **semiconductor CAD methodology**, **gm/Id lookup-table based sizing**, **SPICE simulation evidence**, **clock-distribution architecture**, **RFIC design study**, and **reusable topology validation**.

The goal is to show how device physics, circuit knowledge, scripting, simulation, measurement extraction, validation gates, and reusable topology thinking can be combined into a structured silicon-design methodology.

---

## Core Theme

**From device physics to circuit verification.**

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
-> Reusable Golden Topology
```

---

## System Architecture

The following architecture model explains the **Skynet Analog Agent** as a deterministic, physics-aware analog CAD methodology engine.

![Skynet Analog Agent Architecture](architecture/skynet_analog_agent_architecture.png)

Start here:

- [`architecture/`](architecture/)

---

## Featured Portfolio Modules

| Module | Purpose | Status |
|---|---|---|
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

- [`Simulation truth gate`](knowledge_notes/cad_methodology/)
- [`Closed-loop optimization`](knowledge_notes/cad_methodology/)
- [`Golden regression validation`](knowledge_notes/cad_methodology/)

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

- Recruiters: start with this landing page and featured modules.
- Analog / mixed-signal reviewers: start with Skynet Analog Agent and gm/Id notes.
- CAD / methodology reviewers: start with architecture, truth gates, and closed-loop validation.
- RFIC reviewers: start with RFIC Research and Thesis Track.
- SoC / timing reviewers: start with Interactive SoC Clock Distribution Playbook.

Guide:

- [`HOW_TO_REVIEW_THIS_PORTFOLIO.md`](HOW_TO_REVIEW_THIS_PORTFOLIO.md)

---

## Roadmap

- [`PORTFOLIO_ROADMAP.md`](PORTFOLIO_ROADMAP.md)

---

## Build Timestamp

Last local landing-page build: `2026-05-31 12:34:31`
