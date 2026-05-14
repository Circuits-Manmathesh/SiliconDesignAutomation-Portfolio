# SiliconDesignAutomation: Spec-to-SPICE Agentic Analog Design Automation

SiliconDesignAutomation is a public portfolio version of a physics-aware, spec-driven analog/mixed-signal design automation framework. It demonstrates how a design specification can be converted into gm/Id-guided candidates, verified through SPICE-style DC / AC / transient evidence, and packaged for technical review.

## Architecture Flow

```text
User specification
↓
gm/Id transistor intelligence
↓
candidate circuit synthesis
↓
SPICE netlist generation
↓
DC / AC / transient verification
↓
final design evidence package
```

## First Demo

The first public evidence package is a 3 GHz CMOS inverter clock-buffer unit cell using a representative 50 nm CMOS technology view:

- VDD = 1.0 V
- Load = 20 fF
- Duty-cycle stress = 45%, 50%, 55%
- Final status = PASS
- tpHL approximately 16.1 ps
- tpLH approximately 16.4 ps
- Rise/fall approximately 10.6 ps / 11.9 ps
- Average power approximately 0.478 mW

## How To Review Results

Start with `docs/architecture.md`, then review the inverter walkthrough and the selected plots under `examples/inverter_3GHz_clock_TT27/plots`. The public reports summarize the verified DC, AC, and transient evidence.

## Public Scope

This repository includes sanitized architecture documentation, selected plots, selected reports, public demo specs, and code skeletons. PDK/model files, private LUT databases, raw simulator outputs, full optimizer internals, and private automation code are intentionally excluded.

Demo video: coming soon

## License And IP Note

This is an All Rights Reserved portfolio repository. Review is permitted for hiring, academic, and technical evaluation. Commercial use, redistribution, and reuse of the automation architecture require written permission.

Contact: https://github.com/Circuits-Manmathesh
