# Architecture

This repository is the public portfolio export of a larger private SiliconDesignAutomation framework. The private framework contains executable automation, simulator integration, device model configuration, internal LUT assets, and optimizer implementation. The public repository exposes only the technical structure, selected evidence, and review-safe interfaces.

## Private Framework vs Public Portfolio

The private framework is the working design automation system. It owns the full implementation of LUT generation, device selection, sizing search, simulator execution, measurement extraction, correction loops, and project packaging.

The public portfolio is deliberately narrower. It shows how the system is organized and what kind of evidence it produces, while excluding PDK files, model files, raw simulation artifacts, private databases, and restricted implementation details.

## Master Product Runner Concept

The master product runner is the orchestration layer. It accepts a project specification, identifies the circuit family, selects an implementation strategy, performs preflight checks, launches sizing, builds simulator-ready testbenches, measures DC / AC / transient behavior, and writes the final evidence package.

The public runner skeleton shows the interfaces and control flow. The production runner contains the private execution logic.

## Spec-Driven Design Flow

Projects begin from a structured YAML specification. The spec describes the design type, operating point, supply, load, timing targets, waveform constraints, and optimization objective. The framework converts those requirements into candidate transistor-level implementations and evaluates them against measurable pass/fail criteria.

## LUT Intelligence Database Concept

The private framework uses SPICE-generated gm/Id lookup tables as a transistor intelligence database. These tables represent device behavior across bias, length, width-normalized current density, intrinsic gain, transition frequency, gate capacitance, and region margins.

The public version documents the concept but does not include private LUT files.

## DC / AC / Transient Evidence Package

A project is not considered complete until it produces reviewable evidence:

- DC transfer behavior and operating point consistency.
- AC small-signal gain, phase, bandwidth, and loading checks.
- Transient timing, duty-cycle, edge-rate, and power verification.
- Final summary dashboard and pass/fail report.

## Project-Level Output Structure

Each public example is organized into:

- `spec/` for sanitized project requirements.
- `reports/` for public Markdown summaries.
- `plots/` for selected review-safe evidence figures.
