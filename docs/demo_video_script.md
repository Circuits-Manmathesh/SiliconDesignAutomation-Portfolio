# Demo Video Script

## 3-5 Minute Portfolio Walkthrough

Hello, my name is Manmathesh Mishra. This is SiliconDesignAutomation, a spec-to-SPICE analog design automation framework built as a technical portfolio project.

The goal of this system is to move analog design from isolated scripts toward a structured engineering flow. A user starts with a specification: design type, supply voltage, load, speed target, waveform constraints, and pass/fail limits. The framework turns that specification into candidate transistor-level implementations using gm/Id intelligence, then verifies the result using DC, AC, and transient simulation evidence.

The important idea is that the automation is physics-aware. It does not treat transistor width as the starting point. The framework reasons through gm/Id, current density, intrinsic gain, transition frequency, capacitance, and operating-region margin. Width becomes an output of the sizing process.

In the private framework, the master product runner is the main orchestration layer. It parses a YAML spec, selects the design strategy, queries the device intelligence database, generates candidates, builds SPICE testbenches, runs measurements, and writes a final evidence package.

This public repository is intentionally sanitized. It includes the architecture, public code skeleton, selected plots, selected reports, and a demo specification. It does not include PDK files, model files, the private LUT database, raw simulation outputs, or the full optimization engine.

The first public demo is a 3 GHz CMOS inverter clock-buffer unit cell. The design runs at 1.0 V, drives a 20 fF load, and is checked across 45%, 50%, and 55% input duty-cycle stress cases.

The evidence package includes DC VTC and gain plots, static current and power, gm/Id trend, AC gain and phase response, bandwidth and input-capacitance checks, and transient timing plots. The final selected design passes the public specification, with representative delays around 16 ps, edge rates around 11 ps, and average power around 0.478 mW.

The broader point is not just that one inverter was sized. The point is the framework pattern: specification in, physics-aware device selection, candidate synthesis, simulator-backed verification, and a final evidence package that can be reviewed by another engineer.

This project is designed as a portfolio asset for analog, mixed-signal, EDA, and design automation roles. It demonstrates circuit knowledge, gm/Id methodology, software architecture, simulation automation, and disciplined project reporting.

