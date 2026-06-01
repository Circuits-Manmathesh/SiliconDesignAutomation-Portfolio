\# 04 — Setup / Hold Margin



\## Understanding Final Flip-Flop Timing Closure from Clock Distribution



\---



\## 1. Purpose of This Note



This note explains how a clock signal finally affects \*\*setup and hold timing\*\* at a flip-flop.



The previous notes explained:



```text

PLL → clock source quality

Wire RC → slew/load/delay

Jitter/skew → clock uncertainty and spatial movement

```



Now we reach the final question:



> After the clock has travelled through the whole SoC, can it capture data correctly at the flip-flop?



This is where setup and hold timing decide whether the path is safe.



The \*\*Interactive SoC Clock Distribution Playbook\*\* connects clock distribution to final timing closure using:



```text

Launch clock

Data path delay

Capture clock

Spatial skew

Useful skew

Setup requirement

Hold requirement

Setup slack

Hold slack

PASS / SETUP VIOLATION / HOLD VIOLATION

```



This note explains the theory in simple language and then maps it directly to the playbook.



\---



\## 2. Layman Explanation — What Is a Flip-Flop Doing?



A flip-flop is like a camera.



The clock edge is the camera shutter.



The data is the object being photographed.



For a clear picture:



```text

The object must be ready before the camera clicks.

The object must not move immediately during the click.

```



In digital timing language:



```text

Data must arrive before the capture clock edge.

Data must remain stable long enough around the capture event.

```



These two requirements are called:



```text

Setup requirement

Hold requirement

```



If setup or hold fails, the flip-flop may capture wrong data or become metastable.



\---



\## 3. Launch Flip-Flop and Capture Flip-Flop



A timing path usually starts at one flip-flop and ends at another.



```text

Launch Flip-Flop → Logic Path → Capture Flip-Flop

```



\### Launch Flip-Flop



The launch flip-flop sends data when its clock edge arrives.



\### Logic Path



The data travels through combinational logic.



This logic takes some time.



This is called:



```text

Logic Path Delay

```



\### Capture Flip-Flop



The capture flip-flop samples the data at the next clock edge.



For the path to pass timing:



```text

Data must reach the capture flip-flop before the setup deadline.

Data must not change too early for the hold check.

```



\---



\## 4. Basic Timing Picture



A simplified timing event looks like this:



```text

Launch Clock Edge

&#x20;       ↓

Data starts moving through logic

&#x20;       ↓

Data arrives at capture flip-flop

&#x20;       ↓

Capture Clock Edge samples data

```



If data arrives too late:



```text

Setup violation

```



If data changes too early:



```text

Hold violation

```



This is why setup and hold are both required.



\---



\## 5. Clock Period



Clock period is the time available for one cycle.



The playbook uses:



```text

Tclk = 1000 / fGHz

```



For the default demo:



```text

Clock Frequency = 5 GHz

```



So:



```text

Tclk = 1000 / 5

Tclk = 200 ps

```



At 5 GHz, the complete timing cycle is only 200 ps.



This means:



```text

Data path delay

Setup time

Clock skew

Clock jitter

Slew uncertainty

IR-drop impact

Crosstalk impact

```



all compete inside a very small timing window.



\---



\## 6. What Is Setup Time?



Setup time is the minimum time data must be stable \*\*before\*\* the capture clock edge.



Simple explanation:



> The flip-flop needs data to be ready slightly before the clock captures it.



If the data arrives after the required setup deadline, setup fails.



\---



\## 7. Setup Slack Formula Used in the Playbook



The playbook uses:



```text

SetupSlack = CaptureClock - SetupRequirement - DataArrival

```



Where:



```text

CaptureClock      = time when capture clock edge arrives

SetupRequirement  = required setup time of the flip-flop

DataArrival       = time when data reaches capture flip-flop input

```



Interpretation:



```text

SetupSlack > 0  → setup passes

SetupSlack = 0  → exactly at boundary

SetupSlack < 0  → setup violation

```



In simple words:



> Positive setup slack means data arrived early enough.



\---



\## 8. What Is Hold Time?



Hold time is the minimum time data must remain stable \*\*after\*\* the clock reference.



Simple explanation:



> After the clock edge happens, the flip-flop still needs the old data to remain stable for a short time.



If data changes too soon, hold fails.



Hold failures usually occur on very short/fast data paths.



\---



\## 9. Hold Slack Formula Used in the Playbook



The playbook uses:



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

```



Where:



```text

DataArrival      = data path arrival time

EffectiveSkew    = SpatialSkew + UsefulSkew

HoldRequirement  = required hold time of the flip-flop

```



Interpretation:



```text

HoldSlack > 0  → hold passes

HoldSlack = 0  → exactly at boundary

HoldSlack < 0  → hold violation

```



In simple words:



> Positive hold slack means data is not changing too early.



\---



\## 10. What Is Clock Skew in Setup/Hold?



Clock skew is the difference between launch clock arrival and capture clock arrival.



In the playbook:



```text

EffectiveSkew = SpatialSkew + UsefulSkew

```



\### Spatial Clock Skew



This is natural clock arrival difference due to physical distribution.



Example:



```text

Launch clock arrives earlier

Capture clock arrives 8 ps later

Spatial skew = 8 ps

```



\### Useful Skew



This is intentional clock movement added to improve timing.



Useful skew can be helpful, but it must be used carefully.



\---



\## 11. Default Timing Example in the Playbook



Default timing values:



```text

Clock Frequency      = 5 GHz

Clock Period         = 200 ps

Logic Path Delay     = 175 ps

Spatial Clock Skew   = 8 ps

Useful Skew          = 0 ps

Setup Requirement    = 8 ps

Hold Requirement     = 5 ps

```



First calculate effective skew:



```text

EffectiveSkew = SpatialSkew + UsefulSkew

EffectiveSkew = 8 + 0

EffectiveSkew = 8 ps

```



Now calculate capture clock:



```text

CaptureClock = Period + EffectiveSkew

CaptureClock = 200 + 8

CaptureClock = 208 ps

```



Data arrival is:



```text

DataArrival = Logic Path Delay

DataArrival = 175 ps

```



\---



\## 12. Default Setup Slack Calculation



Formula:



```text

SetupSlack = CaptureClock - SetupRequirement - DataArrival

```



Substitution:



```text

SetupSlack = 208 - 8 - 175

```



Calculation:



```text

SetupSlack = 25 ps

```



Interpretation:



```text

Setup slack is positive.

Data arrives 25 ps before the setup boundary.

Setup passes.

```



In the playbook top metric strip:



```text

Setup Slack = 25.000 ps

```



\---



\## 13. Default Hold Slack Calculation



Formula:



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

```



Substitution:



```text

HoldSlack = 175 - (8 + 5)

```



Calculation:



```text

HoldSlack = 162 ps

```



Interpretation:



```text

Hold slack is positive.

Data is not changing too early.

Hold passes.

```



In the playbook top metric strip:



```text

Hold Slack = 162.000 ps

```



\---



\## 14. Default Timing Status



For the baseline case:



```text

Setup Slack = 25 ps

Hold Slack  = 162 ps

```



Both are positive.



So the playbook reports:



```text

Timing Status = PASS

```



This means the simplified architecture-level timing model is safe under the current default settings.



\---



\## 15. How the Timing Closure Tab Shows This



The \*\*Timing Closure\*\* tab displays:



```text

Launch Clock

Data Path

Capture Clock

Setup Window

Hold Window

Setup Slack

Hold Slack

Timing Status

```



This tab is important because it converts equations into a visual timing diagram.



The user can directly see:



```text

Where data starts

Where data arrives

Where capture clock arrives

Where setup window exists

Where hold window exists

```



This makes timing closure easier to understand than only reading numbers in a report.



\---



\## 16. Setup Violation — Layman Explanation



Setup violation means:



> Data is late.



Camera analogy:



```text

The camera shutter clicked before the object was ready.

```



Digital timing meaning:



```text

Capture clock edge arrived before data was stable early enough.

```



This can happen when:



```text

Logic path is too slow

Clock period is too small

Setup requirement is large

Capture clock is too early

Clock uncertainty is high

Slew is poor

VDD droop slows data path

Routing delay is large

```



\---



\## 17. Setup Violation Example in the Playbook



Change sidebar values:



```text

Logic Path Delay   = 203 ps

Spatial Clock Skew = 10 ps

Useful Skew        = 0 ps

Setup Requirement  = 8 ps

```



Clock period remains:



```text

Clock Period = 200 ps

```



Effective skew:



```text

EffectiveSkew = 10 + 0

EffectiveSkew = 10 ps

```



Capture clock:



```text

CaptureClock = 200 + 10

CaptureClock = 210 ps

```



Data arrival:



```text

DataArrival = 203 ps

```



Setup slack:



```text

SetupSlack = CaptureClock - SetupRequirement - DataArrival

SetupSlack = 210 - 8 - 203

SetupSlack = -1 ps

```



Result:



```text

Setup Slack = -1 ps

Timing Status = SETUP VIOLATION

```



Interpretation:



```text

Data is 1 ps late.

```



This is a small violation, but at 5 GHz even 1 ps matters.



\---



\## 18. How to Fix Setup Violation



A setup violation can be fixed by increasing available time or reducing data delay.



Common fixes:



```text

Reduce logic path delay

Improve cell sizing

Improve data-path slew

Use faster cells

Reduce routing delay

Pipeline the logic

Improve local power supply

Reduce clock uncertainty

Use useful skew carefully

```



The playbook demonstrates one specific architecture knob:



```text

Useful Skew

```



\---



\## 19. Useful Skew Recovery Example



Starting from the setup violation case:



```text

Logic Path Delay   = 203 ps

Spatial Clock Skew = 10 ps

Useful Skew        = 0 ps

Setup Slack        = -1 ps

```



Now apply:



```text

Useful Skew = +8 ps

```



Effective skew:



```text

EffectiveSkew = SpatialSkew + UsefulSkew

EffectiveSkew = 10 + 8

EffectiveSkew = 18 ps

```



Capture clock:



```text

CaptureClock = 200 + 18

CaptureClock = 218 ps

```



Setup slack:



```text

SetupSlack = 218 - 8 - 203

SetupSlack = 7 ps

```



Result:



```text

Setup Slack = +7 ps

Timing Status = PASS

```



Interpretation:



> Useful skew delayed the capture clock, giving data more time to arrive.



This is why useful skew is powerful.



\---



\## 20. But Useful Skew Is Not Free



Useful skew can improve setup, but it can hurt hold.



Reason:



```text

Positive useful skew delays the capture clock relationship.

For long paths, this can help setup.

For short paths, data may change too early and violate hold.

```



This is one of the most important timing-closure lessons.



The playbook is designed to show this tradeoff interactively.



\---



\## 21. Hold Violation — Layman Explanation



Hold violation means:



> Data changed too early.



Camera analogy:



```text

The object moved while the camera was still trying to capture the old frame.

```



Digital timing meaning:



```text

The receiving flip-flop needed the old data to stay stable longer, but the data changed too soon.

```



Hold violations usually happen on very short/fast paths.



\---



\## 22. Hold Violation Example in the Playbook



Set sidebar values:



```text

Logic Path Delay   = 28 ps

Spatial Clock Skew = 10 ps

Useful Skew        = 18 ps

Hold Requirement   = 5 ps

```



Effective skew:



```text

EffectiveSkew = 10 + 18

EffectiveSkew = 28 ps

```



Data arrival:



```text

DataArrival = 28 ps

```



Hold slack formula:



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

```



Substitution:



```text

HoldSlack = 28 - (28 + 5)

```



Calculation:



```text

HoldSlack = -5 ps

```



Result:



```text

Hold Slack = -5 ps

Timing Status = HOLD VIOLATION

```



Interpretation:



```text

Data changes 5 ps too early.

```



This shows that useful skew can create hold risk on short paths.



\---



\## 23. How to Fix Hold Violation



Common hold fixes:



```text

Add hold buffers

Reduce positive useful skew

Balance local clock tree

Add delay to short data paths

Review minimum-delay path

Check local CTS skew

Check fast PVT corners

Reduce overly aggressive capture-clock delay

```



Unlike setup fixes, hold fixes usually add delay to short paths or reduce harmful skew.



\---



\## 24. Setup vs Hold — Core Difference



| Timing Check | Simple Meaning                       | Main Risk      |

| ------------ | ------------------------------------ | -------------- |

| Setup        | Data must arrive before capture edge | Data too late  |

| Hold         | Data must not change too early       | Data too early |



Setup is mainly a long-path problem.



Hold is mainly a short-path problem.



In simple terms:



```text

Setup failure → path is too slow

Hold failure  → path is too fast

```



Both must pass.



\---



\## 25. Why Setup and Hold Must Be Checked Together



A design is not timing-safe if only setup passes.



It must satisfy:



```text

Setup Slack >= 0

Hold Slack  >= 0

```



If setup fails, the chip may capture old or incorrect data.



If hold fails, the chip may capture unstable or wrong data.



A fix for setup can create hold risk.



Example:



```text

Increase useful skew

&#x20;   → setup improves

&#x20;   → hold may degrade

```



Therefore, timing closure is always a balance.



\---



\## 26. How Clock Distribution Affects Setup/Hold



Clock distribution affects setup/hold through:



```text

Clock period

Clock insertion delay

Clock skew

Clock jitter

Clock uncertainty

Slew

IR-drop induced edge shift

Crosstalk induced edge shift

Useful skew strategy

```



The clock does not only tell the flip-flop when to capture.



It also defines the timing window available for data.



That is why clock quality directly affects setup and hold margins.



\---



\## 27. Where Previous Playbook Concepts Enter Timing



The earlier concepts connect to timing like this:



| Clock Concept            | Timing Impact                                  |

| ------------------------ | ---------------------------------------------- |

| PLL jitter               | Reduces effective timing confidence            |

| Duty-cycle distortion    | Can affect clocking windows in sensitive paths |

| RC slew degradation      | Makes clock edge slower and more uncertain     |

| Repeater insertion delay | Shifts clock arrival                           |

| Spatial skew             | Changes launch/capture relationship            |

| Useful skew              | Can improve setup but hurt hold                |

| IR-drop                  | Moves clock edge through buffer delay shift    |

| Crosstalk                | Shifts edge deterministically                  |

| Local leaf variation     | Affects final clock arrival at endpoint        |



This is why clock distribution and timing closure must be studied together.



\---



\## 28. Timing Margin Budget in the Playbook



The playbook also shows a timing-margin budget.



It includes:



```text

Nominal Setup Slack

Nominal Hold Slack

Endpoint Jitter Sensitivity

Uncertainty-Aware Setup Margin

Uncertainty-Aware Hold Margin

```



Endpoint jitter is converted from femtoseconds to picoseconds:



```text

Endpoint Jitter ps = Endpoint Jitter fs / 1000

```



Default:



```text

Endpoint Jitter = 485.291 fs

Endpoint Jitter = 0.485 ps

```



So an uncertainty-aware setup margin can be interpreted as:



```text

Uncertainty-Aware Setup Margin ≈ 25 - 0.485

Uncertainty-Aware Setup Margin ≈ 24.515 ps

```



The playbook keeps nominal slack and uncertainty effect separate so the user can clearly understand both.



\---



\## 29. Interactive Experiment 1 — Create Setup Violation



In the sidebar:



```text

Logic Path Delay = 203 ps

Spatial Skew     = 10 ps

Useful Skew      = 0 ps

```



Observe:



```text

Setup Slack becomes negative

Timing status changes to SETUP VIOLATION

Timing diagram shows data arriving too late

Recommendation suggests setup repair actions

```



Learning:



> Setup failure means data is late.



\---



\## 30. Interactive Experiment 2 — Recover Setup with Useful Skew



Now set:



```text

Useful Skew = +8 ps

```



Observe:



```text

Capture clock moves later

Setup slack becomes positive

Timing status returns to PASS

```



Learning:



> Useful skew can recover setup margin by delaying the capture edge.



\---



\## 31. Interactive Experiment 3 — Create Hold Violation



Set:



```text

Logic Path Delay = 28 ps

Spatial Skew     = 10 ps

Useful Skew      = 18 ps

Hold Requirement = 5 ps

```



Observe:



```text

Hold Slack becomes -5 ps

Timing status becomes HOLD VIOLATION

Timing diagram shows short-path risk

Recommendation suggests hold buffers or reduced skew

```



Learning:



> A setup fix can create hold risk if short paths are not checked.



\---



\## 32. Mapping This Note to the Playbook



| Theory Topic      | Playbook Location                       |

| ----------------- | --------------------------------------- |

| Clock period      | Top metric strip and Live Math tab      |

| Logic path delay  | Sidebar timing section                  |

| Spatial skew      | Sidebar timing section                  |

| Useful skew       | Sidebar timing section                  |

| Setup requirement | Sidebar timing section                  |

| Hold requirement  | Sidebar timing section                  |

| Setup slack       | Timing Closure tab and top metric strip |

| Hold slack        | Timing Closure tab and top metric strip |

| Timing status     | Timing Closure tab                      |

| Timing formulas   | Live Math tab and Timing Closure tab    |

| Architecture fix  | Recommendations tab                     |



\---



\## 33. Default Timing Summary



Default case:



```text

Clock Period      = 200 ps

Logic Delay       = 175 ps

Spatial Skew      = 8 ps

Useful Skew       = 0 ps

Setup Requirement = 8 ps

Hold Requirement  = 5 ps

```



Calculated:



```text

Effective Skew = 8 ps

Capture Clock  = 208 ps

Setup Slack    = 25 ps

Hold Slack     = 162 ps

Timing Status  = PASS

```



Interpretation:



```text

The baseline timing path is safe in the simplified architecture-level model.

```



\---



\## 34. Practical SoC Designer Interpretation



A SoC timing engineer should ask:



```text

Is the logic path too long?

Is the clock period too small?

Is useful skew helping or hurting?

Is setup margin still positive?

Is hold margin still positive?

Is endpoint jitter consuming timing margin?

Is local IR-drop moving the clock edge?

Is crosstalk affecting capture timing?

Are short paths protected?

Are long paths optimized?

```



The playbook helps answer these questions interactively.



\---



\## 35. What This Model Does Not Claim



The playbook timing engine is simplified and transparent.



It does not replace production STA.



It does not include:



```text

Full timing graph traversal

Real Liberty timing arcs

Setup/hold arc interpolation

Clock reconvergence pessimism removal

AOCV/POCV derates

SI delay shifts

EMIR-aware timing derates

Multi-mode multi-corner signoff

```



Final silicon signoff requires:



```text

STA

SPEF

Liberty

SI

EMIR

PVT

OCV

CTS reports

Timing ECO validation

```



The playbook is designed for learning, architecture review, and explainable sensitivity analysis.



\---



\## 36. Final Takeaway



Setup and hold are the final proof of clock-distribution quality.



A clock may look good at the PLL.



It may look acceptable at the global trunk.



It may survive regional distribution.



But the final question is:



```text

Can the flip-flop capture data safely?

```



That requires:



```text

Setup Slack >= 0

Hold Slack  >= 0

```



The Interactive SoC Clock Distribution Playbook makes this final timing decision visible through:



```text

Live equations

Timing diagram

Setup/hold bars

Useful skew control

Slack calculation

Architecture recommendations

```



The core lesson is:



> Clock distribution is not complete until setup and hold both close at the endpoint.



