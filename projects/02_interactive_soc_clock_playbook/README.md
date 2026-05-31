# Interactive SoC Clock Distribution Playbook

This is a separate system-level playbook for studying clock distribution from PLL to flip-flop.

## Planned Study Flow

```text
PLL / Clock Source
-> Root Clock Buffer
-> Global Clock Spine / H-Tree
-> Regional Clock Distribution
-> Clock Gating
-> Local Leaf Buffers
-> Flip-Flop / Macro Load
-> Timing Margin and Clock Power Study
```

## Topics

- PLL to flop roadmap
- 5 GHz clock demo
- slew / load / delay / skew study
- setup / hold timing margin
- duty-cycle distortion
- jitter and uncertainty
- clock power and EMIR awareness
- failure modes and debug
