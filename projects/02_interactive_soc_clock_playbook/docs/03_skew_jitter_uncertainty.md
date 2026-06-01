\# 03 — Skew, Jitter and Uncertainty



\## Understanding Why Clock Edges Do Not Arrive Perfectly in Real Silicon



\---



\## 1. Purpose of This Note



This note explains three important clock-distribution concepts:



```text

Jitter

Skew

Clock Uncertainty

```



These three terms are related, but they are not the same.



In a real SoC, the clock edge does not arrive perfectly at every flip-flop. It can move in time, it can arrive at different locations at different moments, and timing tools must reserve margin for these effects.



The \*\*Interactive SoC Clock Distribution Playbook\*\* helps users understand this through:



```text

Live jitter budget

Live skew budget

Waveform movement

SoC journey map

Timing diagram

Setup/Hold slack calculation

Architecture recommendations

```



The goal is to make these concepts understandable from theory to practical architecture-level analysis.



\---



\## 2. Layman Explanation — What Is Jitter?



Imagine a train that is supposed to arrive at a station every 10 minutes.



Ideally:



```text

10:00

10:10

10:20

10:30

```



But in reality, it may arrive slightly early or late:



```text

10:00:01

10:09:59

10:20:02

10:29:58

```



The train is still following the schedule, but each arrival time has a small variation.



Clock jitter is similar.



A clock edge is expected at a certain time, but in real silicon it may arrive slightly early or late.



Ideal clock edge positions:



```text

0 ps

200 ps

400 ps

600 ps

800 ps

```



Real clock edge positions:



```text

0.05 ps

199.91 ps

400.14 ps

599.87 ps

800.09 ps

```



This movement of the edge over time is called \*\*jitter\*\*.



In simple words:



> Jitter means the clock edge moves randomly or deterministically around its ideal time.



\---



\## 3. Why Jitter Matters



The clock edge decides when the flip-flop samples data.



If the edge moves, the available time for data capture changes.



At low speed, small jitter may not matter much.



At high speed, it matters a lot.



In our playbook default case:



```text

Clock Frequency = 5 GHz

Clock Period    = 200 ps

```



At 5 GHz:



```text

1 ps  = 0.5% of the clock period

10 ps = 5% of the clock period

```



So even picosecond-level edge movement can consume real timing margin.



This is why jitter is critical in:



```text

High-speed SoCs

AI accelerators

HBM/DDR clocking

SerDes clocking

High-frequency clock distribution

Low-margin timing paths

```



\---



\## 4. Sources of Jitter in a SoC Clock



Jitter can come from many sources.



In the playbook, we focus on four architecture-level contributors:



```text

PLL random jitter

RC slew uncertainty

Power supply induced jitter

Crosstalk-related uncertainty

```



\### 4.1 PLL Random Jitter



The PLL is the clock source.



Because of phase noise, VCO noise, supply noise, and circuit noise, the PLL output edge is not perfectly stable.



In the playbook, this is controlled by:



```text

PLL Random Jitter RMS

```



Default value:



```text

PLL Random Jitter = 120 fs

```



This means the source clock already has timing uncertainty before entering the distribution network.



\---



\### 4.2 RC Slew Uncertainty



When the clock travels through long wires, the edge becomes slower because of wire resistance and capacitance.



A slow edge is more sensitive to noise.



The playbook links this uncertainty to effective segment RC:



```text

RC Uncertainty ∝ τsegment

```



The model uses:



```text

Jrc = rc\_uncertainty\_coeff × τsegment × 1000

```



Default values:



```text

rc\_uncertainty\_coeff = 0.18

τsegment             = 7.6608 ps

```



So:



```text

Jrc = 0.18 × 7.6608 × 1000

Jrc = 1378.944 fs

```



This is an architecture-level sensitivity metric.



It shows that if effective segment RC becomes large, the edge becomes slower and uncertainty increases.



Important note:



> The playbook uses segment RC, not total unbuffered RC, because real clock trunks are divided by repeaters.



\---



\### 4.3 Power Supply Induced Jitter



Clock buffers depend on supply voltage.



If VDD droops, the buffer becomes slower.



That moves the clock edge.



This effect is called:



```text

Power Supply Induced Jitter

```



or:



```text

PSIJ

```



The playbook models the jitter term as:



```text

Jpsij = psij\_jitter\_coeff × Vdroop

```



Default values:



```text

psij\_jitter\_coeff = 1.8 fs/mV

Vdroop            = 45 mV

```



So:



```text

Jpsij = 1.8 × 45

Jpsij = 81 fs

```



The playbook also models edge shift due to droop:



```text

ΔtPSIJ = kdroop × Vdroop

```



Default:



```text

kdroop = 0.0048 ps/mV

Vdroop = 45 mV

```



So:



```text

ΔtPSIJ = 0.0048 × 45

ΔtPSIJ = 0.216 ps

```



This helps users understand that power integrity becomes timing integrity.



\---



\### 4.4 Crosstalk-Related Uncertainty



Clock wires can run near high-toggle aggressor wires.



When nearby wires switch, coupling capacitance can disturb the victim clock line.



The playbook uses three crosstalk modes:



```text

Quiet / Orthogonal

In-Phase

Out-of-Phase

```



Conceptually:



```text

Quiet / Orthogonal      → small residual coupling

In-Phase Aggressor      → edge shifts in one direction

Out-of-Phase Aggressor  → edge shifts in the opposite direction

```



Default case:



```text

Crosstalk Mode = Quiet / Orthogonal

Crosstalk Jitter = 8 fs

Crosstalk Edge Shift = 0 ps

```



If user selects:



```text

Crosstalk Mode = In-Phase

```



the playbook shows:



```text

Crosstalk Edge Shift = +0.75 ps

Crosstalk Jitter     = 32 fs

```



This demonstrates that crosstalk is not just a signal-integrity issue. It can directly become a timing issue.



\---



\## 5. Jitter Budget Formula Used in the Playbook



The playbook combines jitter contributors using a root-sum-square model:



```text

Jtotal = sqrt(Jpll² + Jrc² + Jpsij² + Jxtalk²)

```



Where:



```text

Jpll   = PLL random jitter

Jrc    = RC slew uncertainty

Jpsij  = power-supply-induced jitter

Jxtalk = crosstalk-related uncertainty

```



This is a common way to combine independent uncertainty-like contributors at architecture level.



\---



\## 6. Default Jitter Budget Example



Default playbook values:



```text

PLL Random Jitter   = 120 fs

RC Slew Uncertainty = 1378.944 fs

PSIJ                = 81 fs

Crosstalk           = 8 fs

```



Now calculate:



```text

Jtotal = sqrt(120² + 1378.944² + 81² + 8²)

```



Step by step:



```text

120²       = 14400

1378.944² ≈ 1901486.57

81²        = 6561

8²         = 64

```



Sum:



```text

Total = 14400 + 1901486.57 + 6561 + 64

Total ≈ 1922511.57

```



Square root:



```text

Jtotal ≈ 1386.547 fs

```



So the playbook shows:



```text

Before Mitigation Total Jitter = 1386.547 fs

```



With mitigation enabled:



```text

Mitigation Factor = 0.35

```



So:



```text

After Mitigation Total = 1386.547 × 0.35

After Mitigation Total = 485.291 fs

```



This is the endpoint jitter metric shown in the top metric strip and budget tab.



\---



\## 7. How the Playbook Shows Jitter



The playbook shows jitter in multiple places:



| Location            | What It Shows                                       |

| ------------------- | --------------------------------------------------- |

| Top metric strip    | Endpoint jitter after mitigation                    |

| Waveform Lab        | Clock edge movement and degraded/mitigated waveform |

| SoC Journey Map     | Jitter RMS at each node                             |

| Jitter Budget tab   | Individual jitter contributors                      |

| Live Math tab       | Formula, substitution, calculated value             |

| Recommendations tab | Action when endpoint uncertainty becomes large      |



This is important because the user can see jitter as:



```text

A number

A formula

A waveform behavior

A node trend

A design recommendation

```



That is more useful than only seeing a spreadsheet entry.



\---



\## 8. Layman Explanation — What Is Skew?



Now let us understand skew.



Imagine a loudspeaker announcement in a large stadium.



If you stand near the speaker, you hear it first.



If you stand far away, you hear it later.



The announcement is the same, but it reaches different people at different times.



Clock skew is similar.



The same clock signal reaches different flip-flops at different times.



Example:



```text

Launch flip-flop clock arrival  = 100 ps

Capture flip-flop clock arrival = 108 ps

```



Then:



```text

Clock Skew = 8 ps

```



In simple words:



> Skew means the clock arrives at different physical locations at different times.



\---



\## 9. Jitter vs Skew



Jitter and skew are different.



| Concept | Simple Meaning                                         | Example                                                         |

| ------- | ------------------------------------------------------ | --------------------------------------------------------------- |

| Jitter  | Same clock edge moves over time                        | Edge expected at 200 ps arrives at 199.9 ps or 200.1 ps         |

| Skew    | Same clock reaches different places at different times | Launch clock arrives at 100 ps, capture clock arrives at 108 ps |



Another way to remember:



```text

Jitter = time variation at a point

Skew   = time difference between points

```



Both affect timing closure.



\---



\## 10. Sources of Skew



Skew can come from:



```text

Different clock path lengths

Different buffer counts

Different clock loads

Regional routing imbalance

Clock tree asymmetry

Local IR-drop

Different process variation

Different local temperature

Useful skew intentionally added by CTS/timing optimization

```



In large SoCs, skew is unavoidable.



The goal is not always zero skew.



The goal is controlled and budgeted skew.



\---



\## 11. Skew Budget in the Playbook



The playbook separates skew into multiple components:



```text

Trunk Mismatch

Regional Mismatch

Local Buffer Mismatch

Spatial Clock Skew

Useful Skew

Final Effective Skew

```



This is shown in the \*\*Jitter / Skew Budget\*\* tab.



\---



\### 11.1 Trunk Mismatch



The global trunk can introduce mismatch due to length and routing differences.



The playbook uses a simple architecture-level trend:



```text

Trunk Mismatch = 0.0025 × Global Wire Length

```



Default:



```text

Global Wire Length = 2400 µm

```



So:



```text

Trunk Mismatch = 0.0025 × 2400

Trunk Mismatch = 6 ps

```



\---



\### 11.2 Regional Mismatch



Regional distribution can introduce mismatch because different regions have different buffering and routing conditions.



The playbook uses:



```text

Regional Mismatch = 2.5 + 0.25 × RepeaterCount

```



Default:



```text

Repeater Count = 4

```



So:



```text

Regional Mismatch = 2.5 + 0.25 × 4

Regional Mismatch = 3.5 ps

```



\---



\### 11.3 Local Buffer Mismatch



Local leaf buffers can be affected by local droop and variation.



The playbook uses:



```text

Local Buffer Mismatch = 1.5 + 0.03 × Vdroop

```



Default:



```text

Vdroop = 45 mV

```



So:



```text

Local Buffer Mismatch = 1.5 + 0.03 × 45

Local Buffer Mismatch = 2.85 ps

```



\---



\### 11.4 Spatial Clock Skew



Spatial clock skew is directly controlled by the user in the sidebar.



Default:



```text

Spatial Clock Skew = 8 ps

```



This represents the clock arrival difference between launch and capture domains.



\---



\### 11.5 Useful Skew



Useful skew is intentional clock movement used to improve timing.



Default:



```text

Useful Skew = 0 ps

```



If the user increases useful skew, the capture clock is intentionally shifted.



This may improve setup timing but can reduce hold margin.



\---



\### 11.6 Final Effective Skew



The timing engine uses:



```text

EffectiveSkew = SpatialSkew + UsefulSkew

```



Default:



```text

EffectiveSkew = 8 + 0

EffectiveSkew = 8 ps

```



The playbook shows this as:



```text

Final Effective Skew = 8 ps

```



\---



\## 12. Why Useful Skew Is Powerful



Useful skew means intentionally shifting the capture clock to help timing.



Suppose the data is arriving slightly late.



If we delay the capture clock, the data gets more time to arrive.



This improves setup slack.



Example:



```text

Clock Period  = 200 ps

Spatial Skew  = 10 ps

Useful Skew   = 0 ps

Logic Delay   = 203 ps

Setup Req     = 8 ps

```



Capture clock:



```text

CaptureClock = 200 + 10 + 0

CaptureClock = 210 ps

```



Setup slack:



```text

SetupSlack = 210 - 8 - 203

SetupSlack = -1 ps

```



This is setup violation.



Now apply:



```text

Useful Skew = +8 ps

```



New capture clock:



```text

CaptureClock = 200 + 10 + 8

CaptureClock = 218 ps

```



Setup slack:



```text

SetupSlack = 218 - 8 - 203

SetupSlack = 7 ps

```



Setup is recovered.



This is why useful skew is important.



\---



\## 13. Why Useful Skew Can Be Dangerous



Useful skew can help setup, but it can hurt hold.



For a short path:



```text

Logic Delay      = 28 ps

Spatial Skew     = 10 ps

Useful Skew      = 18 ps

Hold Requirement = 5 ps

```



Effective skew:



```text

EffectiveSkew = 10 + 18

EffectiveSkew = 28 ps

```



Hold slack:



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

HoldSlack = 28 - (28 + 5)

HoldSlack = -5 ps

```



This is a hold violation.



Meaning:



```text

Data changes too early relative to the hold boundary.

```



This is one of the most important timing lessons:



> Useful skew can fix setup, but it can create hold risk.



The playbook demonstrates this directly in the Timing Closure tab.



\---



\## 14. What Is Clock Uncertainty?



Clock uncertainty is a timing margin used to protect against clock variation.



In real STA, uncertainty can include:



```text

PLL jitter

Clock tree jitter

Skew margin

OCV/AOCV/POCV margin

SI effects

Modeling pessimism

Power-noise margin

Additional guardband

```



In simple words:



> Clock uncertainty is the timing margin reserved because the clock is not perfectly predictable.



The playbook separates major contributors so users can see where uncertainty is coming from.



\---



\## 15. Why Uncertainty Reduces Timing Margin



Suppose setup slack is:



```text

Setup Slack = 25 ps

```



If endpoint jitter sensitivity is:



```text

Endpoint Jitter = 485.291 fs = 0.485 ps

```



Then an uncertainty-aware view can consider:



```text

Uncertainty-Aware Setup Margin ≈ 25 - 0.485

Uncertainty-Aware Setup Margin ≈ 24.515 ps

```



The current playbook keeps nominal setup/hold slack transparent and separately shows endpoint uncertainty.



This is intentional.



It helps users understand:



```text

Base slack formula

\+

Uncertainty impact

```



instead of hiding everything inside one number.



\---



\## 16. How Jitter and Skew Affect Setup/Hold



Setup timing is affected by:



```text

Data path delay

Capture clock arrival

Setup requirement

Clock skew

Clock jitter / uncertainty

```



Hold timing is affected by:



```text

Short data path delay

Effective skew

Hold requirement

Clock uncertainty

Local variation

```



General behavior:



```text

More positive useful skew → setup improves

More positive useful skew → hold margin may reduce

More jitter              → effective timing margin reduces

More uncontrolled skew   → timing closure becomes harder

```



The playbook makes this interactive.



\---



\## 17. Interactive Experiment 1 — Increase PLL Jitter



In the sidebar, increase:



```text

PLL Random Jitter RMS

```



Observe:



```text

Jitter budget increases

Endpoint jitter increases

Waveform edge uncertainty increases

Recommendations may warn about endpoint uncertainty

```



Interpretation:



> Source clock quality directly affects endpoint clock reliability.



\---



\## 18. Interactive Experiment 2 — Increase Wire Length



Increase:



```text

Global Wire Length

```



Observe:



```text

RC segment tau increases

RC slew uncertainty increases

Endpoint jitter increases

Waveform slew degrades

SoC node jitter trend increases

```



Interpretation:



> Interconnect RC can become a major contributor to clock uncertainty.



\---



\## 19. Interactive Experiment 3 — Increase VDD Droop



Increase:



```text

Dynamic VDD Droop

```



Observe:



```text

PSIJ increases

IR-drop heatmap becomes stronger

Clock edge shift increases

Recommendations suggest decaps and power-grid review

```



Interpretation:



> Power-grid noise can directly become timing noise.



\---



\## 20. Interactive Experiment 4 — Change Crosstalk Mode



Change:



```text

Crosstalk Aggressor Alignment = In-Phase

```



Observe:



```text

Crosstalk edge shift becomes positive

Crosstalk jitter increases

Waveform shifts

Recommendation suggests shielding and spacing

```



Change:



```text

Crosstalk Aggressor Alignment = Out-of-Phase

```



Observe:



```text

Crosstalk edge shift becomes negative

Clock edge movement direction changes

```



Interpretation:



> Crosstalk alignment can change deterministic clock edge movement.



\---



\## 21. Interactive Experiment 5 — Apply Useful Skew



Increase:



```text

Useful Skew

```



Observe:



```text

Capture clock moves

Setup slack may improve

Hold slack may reduce

Timing diagram changes

```



Interpretation:



> Skew can be used as a timing knob, but it must be checked for both setup and hold.



\---



\## 22. Mapping This Note to the Playbook



| Theory Topic        | Playbook Location                    |

| ------------------- | ------------------------------------ |

| PLL jitter          | Sidebar and Jitter Budget tab        |

| RC uncertainty      | Live Math and Jitter Budget tab      |

| PSIJ                | IR-Drop / Crosstalk tab              |

| Crosstalk           | Crosstalk mode selector and waveform |

| Jitter total        | Top metric strip and budget tab      |

| Trunk mismatch      | Skew Budget tab                      |

| Regional mismatch   | Skew Budget tab                      |

| Local mismatch      | Skew Budget tab                      |

| Spatial skew        | Sidebar and Timing Closure tab       |

| Useful skew         | Sidebar and Timing Closure tab       |

| Setup/Hold impact   | Timing Closure tab                   |

| Architecture action | Recommendations tab                  |



\---



\## 23. Default Budget Summary



Default jitter budget:



```text

PLL Random Jitter       = 120 fs

RC Slew Uncertainty     = 1378.944 fs

PSIJ                    = 81 fs

Crosstalk               = 8 fs

Before Mitigation Total = 1386.547 fs

After Mitigation Total  = 485.291 fs

```



Default skew budget:



```text

Trunk Mismatch          = 6.00 ps

Regional Mismatch       = 3.50 ps

Local Buffer Mismatch   = 2.85 ps

Spatial Clock Skew      = 8.00 ps

Useful Skew             = 0.00 ps

Final Effective Skew    = 8.00 ps

```



Timing baseline:



```text

Setup Slack = 25 ps

Hold Slack  = 162 ps

Status      = PASS

```



This baseline is intentionally stable so users can start from a safe scenario and then introduce stress.



\---



\## 24. Practical SoC Designer Interpretation



A clock architect, STA engineer, or physical-design engineer should ask:



```text

Is source jitter acceptable?

Is RC uncertainty dominating the budget?

Is the clock edge too slow?

Is endpoint uncertainty too high?

Is spatial skew controlled?

Is useful skew intentional?

Does setup still pass?

Does hold still pass?

Is droop moving the clock edge?

Is crosstalk shifting the clock edge?

Is there a mitigation plan?

```



The playbook helps answer these questions interactively.



\---



\## 25. What This Model Does Not Claim



This playbook does not claim final signoff jitter, skew, or uncertainty.



It does not replace:



```text

PLL phase-noise integration

Extracted SPEF timing

Liberty timing models

Production STA

SI analysis

EMIR analysis

PVT and OCV correlation

CTS implementation reports

```



The model is intentionally transparent and architecture-level.



Its purpose is to explain:



```text

What jitter means

What skew means

How uncertainty accumulates

How skew affects setup/hold

Why useful skew is powerful but risky

How physical effects map into timing behavior

```



\---



\## 26. Final Takeaway



Jitter, skew, and uncertainty are different but connected.



```text

Jitter      = clock edge movement over time

Skew        = clock arrival difference across locations

Uncertainty = timing margin reserved for imperfect clock behavior

```



A robust SoC clock architecture must control all three.



The Interactive SoC Clock Distribution Playbook makes these effects visible through:



```text

Waveforms

Node maps

Budget charts

Live formulas

Timing diagrams

Recommendations

```



This helps users understand not just the final timing result, but the physical reason behind it.



