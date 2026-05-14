# SiliconDesignAutomation: Spec-to-SPICE Agentic Analog Design Automation

SiliconDesignAutomation is a public portfolio version of a physics-aware, spec-driven analog design automation framework. It demonstrates how a design specification can be converted into gm/Id-guided candidates, verified through DC, AC, and transient evidence, and packaged for technical review.

## Architecture Flow

```text
User specification
  -> gm/Id transistor intelligence
  -> candidate circuit synthesis
  -> SPICE-style testbench generation
  -> DC / AC / transient verification
  -> final design evidence package
```

## First Inverter Demo

The first public evidence package is a 3 GHz CMOS inverter clock-buffer unit cell using a representative 50 nm CMOS technology view.

- VDD = 1.0 V
- Load = 20 fF
- Duty-cycle stress = 45%, 50%, 55%
- Final status = PASS
- tpHL approximately 16.1 ps
- tpLH approximately 16.4 ps
- Rise/fall approximately 10.6 ps / 11.9 ps
- Average power approximately 0.478 mW

## How To Review Results

Start with `docs/architecture.md`, then review `docs/inverter_demo_walkthrough.md`. The selected plots under `examples/inverter_3GHz_clock_TT27/plots` show the DC VTC, gain behavior, timing markers, power tradeoff, and final dashboards. The public reports summarize the verified DC, AC, and transient evidence without exposing private model paths, private LUT data, raw netlists, or simulator logs.

## Demo Video

Demo video: coming soon

## License And IP Note

This is an All Rights Reserved portfolio repository. Review is permitted for hiring, academic, and technical evaluation. Commercial use, redistribution, and reuse of the automation architecture require written permission.

Contact: https://github.com/Circuits-Manmathesh
