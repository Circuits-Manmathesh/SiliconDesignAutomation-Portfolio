\# 05 — Clock Power and EMIR Awareness



\## Understanding How Power Integrity Becomes Clock Timing Integrity



\---



\## 1. Purpose of This Note



This note explains why \*\*clock power\*\*, \*\*IR-drop\*\*, \*\*electromigration\*\*, \*\*decaps\*\*, \*\*shielding\*\*, and \*\*crosstalk\*\* matter in SoC clock distribution.



The earlier notes explained:



```text

PLL-to-flip-flop clock journey

Clock slew, load and delay

Jitter, skew and uncertainty

Setup and hold margin

```



Now we connect clock distribution to power integrity.



The key idea is:



> A clock network is not only a timing network.

> It is also a high-activity power-consuming network.



Because the clock toggles continuously, it consumes dynamic power, draws current from the power grid, and can be affected by local voltage droop.



In real silicon:



```text

Power grid noise can move clock edges.

Clock edge movement can reduce timing margin.

Therefore, power integrity becomes timing integrity.

```



The \*\*Interactive SoC Clock Distribution Playbook\*\* demonstrates this using:



```text

Dynamic VDD Droop slider

Crosstalk Aggressor Alignment selector

Shielding + Decaps toggle

IR-drop heatmap

Clock waveform shift

PSIJ calculation

Jitter budget

Architecture recommendations

```



\---



\## 2. Layman Explanation — Why Clock Power Matters



Imagine a city where every traffic signal changes at the same time.



Every signal needs electricity.



If too many signals switch together, the power network experiences stress.



A chip clock network is similar.



The clock toggles every cycle and drives a huge number of gates:



```text

Clock buffers

Clock gates

Flip-flop clock pins

Local clock routes

Regional clock trees

Global clock trunks

```



Because the clock switches so frequently, it can consume a significant part of total chip power.



A clock network is not just “one wire”.



It is a large active electrical system.



\---



\## 3. What Is Dynamic Clock Power?



A simple dynamic power expression is:



```text

Pdynamic ≈ C × V² × f

```



Where:



```text

C = switched capacitance

V = supply voltage

f = switching frequency

```



For a clock:



```text

f is high

activity factor is almost always high

capacitance can be large

```



So the clock network can become a major dynamic power contributor.



In simple words:



> More clock capacitance means more charge and discharge every cycle.

> More frequency means this happens more times per second.

> More switching means more current demand.



This current demand affects the power grid.



\---



\## 4. Why Clock Load and Power Are Connected



From the previous note, we saw that a clock route has capacitance.



Default playbook example:



```text

Global Wire Length = 2400 µm

Wire Capacitance   = 95 aF/µm

```



So:



```text

Cwire = 95 × 2400 aF

Cwire = 228000 aF

Cwire = 228 fF

```



This capacitance must be charged and discharged every cycle.



At 5 GHz:



```text

Clock Period = 200 ps

```



That means the clock network is switching extremely frequently.



More wire capacitance creates:



```text

More dynamic power

More current demand

More power-grid stress

More possible local IR-drop

More timing sensitivity

```



This is why clock load is not only a delay problem.



It is also a power and EMIR problem.



\---



\## 5. What Is EMIR?



EMIR stands for:



```text

Electromigration and IR-drop

```



It combines two reliability and power-integrity concerns:



```text

EM  = Electromigration

IR  = Voltage drop due to current through resistance

```



\---



\## 6. What Is IR-Drop?



IR-drop means voltage loss across the power grid due to current flow.



The basic equation is:



```text

Vdrop = I × R

```



Where:



```text

I = current flowing through power grid

R = resistance of the power delivery path

```



If current increases suddenly, voltage drop increases.



In a chip, this means local VDD can become lower than nominal VDD.



Example:



```text

Nominal VDD = 0.75 V

Local VDD droops by 45 mV

Effective local VDD = 0.705 V

```



The circuit still works, but it may become slower.



Clock buffers are also affected by this.



\---



\## 7. Layman Explanation — IR-Drop as Water Pressure



Think of the power grid like water pipes.



Voltage is like water pressure.



Current is like water flow.



If many houses suddenly open taps at the same time, water pressure can drop.



Similarly, if many transistors switch at the same time, local VDD can drop.



This local voltage drop is IR-drop.



For clock distribution, this matters because clock buffers need stable voltage to switch quickly.



If voltage droops:



```text

Clock buffer drive strength reduces

Buffer delay increases

Clock edge arrives later

Timing uncertainty increases

```



\---



\## 8. What Is Dynamic IR-Drop?



Static IR-drop is due to relatively steady current.



Dynamic IR-drop happens when current changes quickly due to switching activity.



In AI SoCs or high-performance SoCs, large blocks can switch together:



```text

AI compute tiles

SRAM banks

NoC regions

Clock-gated blocks waking up

PHY logic

Vector engines

MAC arrays

```



This sudden switching creates transient current demand.



That demand creates dynamic VDD droop.



The playbook models this using:



```text

Dynamic VDD Droop (mV)

```



Default value:



```text

Dynamic VDD Droop = 45 mV

```



\---



\## 9. Why Dynamic IR-Drop Affects Clock Timing



Clock buffers are voltage-sensitive.



When VDD reduces:



```text

PMOS/NMOS drive current reduces

Clock buffer delay increases

Clock edge shifts later

Clock uncertainty increases

```



This is called:



```text

Power Supply Induced Jitter

```



or:



```text

PSIJ

```



In simple words:



> Supply noise becomes clock edge movement.



This is one of the most important connections between EMIR and timing closure.



\---



\## 10. PSIJ Edge Shift Model in the Playbook



The playbook models supply-induced clock edge shift as:



```text

ΔtPSIJ = kdroop × Vdroop

```



Where:



```text

ΔtPSIJ = clock edge shift due to power droop

kdroop  = delay sensitivity coefficient

Vdroop  = dynamic VDD droop

```



Default playbook constants:



```text

kdroop = 0.0048 ps/mV

Vdroop = 45 mV

```



So:



```text

ΔtPSIJ = 0.0048 × 45

ΔtPSIJ = 0.216 ps

```



The playbook shows:



```text

PSIJ Edge Shift = 0.216 ps

```



This value may look small, but at high frequency it is meaningful.



At 5 GHz:



```text

Clock Period = 200 ps

```



So:



```text

0.216 ps is a real edge movement inside a 200 ps timing window.

```



\---



\## 11. PSIJ Jitter Model in the Playbook



The playbook also models jitter contribution due to dynamic droop:



```text

Jpsij = psij\_jitter\_coeff × Vdroop

```



Default:



```text

psij\_jitter\_coeff = 1.8 fs/mV

Vdroop            = 45 mV

```



So:



```text

Jpsij = 1.8 × 45

Jpsij = 81 fs

```



This appears in the jitter budget.



The important concept is:



```text

Droop does not only create voltage error.

Droop creates timing error.

```



\---



\## 12. What the IR-Drop / Crosstalk Tab Shows



The playbook has an \*\*IR-Drop / Crosstalk Awareness\*\* tab.



This tab shows:



```text

Synthetic normalized IR-drop heatmap

Clock path overlay

Dynamic VDD droop value

PSIJ edge shift

Crosstalk mode

Crosstalk edge shift

Shielding + decaps status

```



The heatmap is intentionally normalized.



It does not claim to be an extracted EMIR map.



Its purpose is educational:



```text

Show where droop hotspots may exist.

Show whether the clock path crosses active regions.

Show why local power conditions matter for clock timing.

```



Future versions can replace the synthetic heatmap with real EMIR droop map data.



\---



\## 13. Default IR-Drop Example



Default playbook values:



```text

Dynamic VDD Droop  = 45 mV

Shielding + Decaps = ON

Crosstalk Mode     = Quiet / Orthogonal

```



Computed:



```text

PSIJ Edge Shift = 0.216 ps

PSIJ Jitter     = 81 fs

```



Interpretation:



```text

The clock edge is slightly shifted by local supply droop.

Mitigation reduces the residual effect visible at endpoint.

```



This helps users understand why local decap and power-grid planning are needed near clock buffers.



\---



\## 14. Interactive Experiment 1 — Increase Dynamic VDD Droop



In the sidebar, increase:



```text

Dynamic VDD Droop = 70 mV

```



Now calculate PSIJ edge shift:



```text

ΔtPSIJ = 0.0048 × 70

ΔtPSIJ = 0.336 ps

```



Calculate PSIJ jitter:



```text

Jpsij = 1.8 × 70

Jpsij = 126 fs

```



Observe in the playbook:



```text

PSIJ edge shift increases

Jitter budget changes

Heatmap intensity increases

Recommendations mention power-grid / decap review

```



Interpretation:



> Higher droop means stronger clock edge movement and higher power-noise-related timing uncertainty.



\---



\## 15. Why Sub-Picosecond Edge Shift Still Matters



A value like:



```text

0.216 ps

```



may look small.



But modern high-speed clocks operate with small timing budgets.



At 5 GHz:



```text

Tclk = 200 ps

```



If multiple effects combine:



```text

PLL jitter

RC uncertainty

PSIJ

Crosstalk

Skew

Slew degradation

Setup requirement

```



then even small edge shifts become important.



Clock architecture must therefore track the full budget, not only one number.



\---



\## 16. What Is Electromigration?



Electromigration is a long-term reliability issue.



When high current flows through metal wires over time, metal atoms can slowly move.



This can create:



```text

Void formation

Metal thinning

Resistance increase

Open failure

Reliability degradation

```



Clock networks matter because:



```text

Clock toggles frequently

Clock buffers draw dynamic current

Clock routes can carry repeated switching current

Clock mesh/tree structures may concentrate current

```



Electromigration is not directly simulated in the current playbook, but the app includes EMIR awareness because clock power and power-grid stress are strongly related to timing and reliability.



\---



\## 17. Why EM and IR Are Discussed Together



EM and IR are often reviewed together because both depend on current flow.



High current can cause:



```text

Voltage drop problem  → IR-drop

Reliability problem   → electromigration

```



A clock network can contribute to both.



For early architecture discussion, the important questions are:



```text

Is clock power too high?

Are too many repeaters being inserted?

Are local clock buffers clustered too tightly?

Is the power grid strong enough?

Are there decaps near critical clock buffers?

Are clock routes crossing high-activity regions?

```



The playbook helps users build this awareness.



\---



\## 18. What Is Crosstalk?



Crosstalk happens when one signal affects another nearby signal through coupling.



In SoC routing, nearby wires have coupling capacitance.



If an aggressor wire switches near a victim clock wire, it can disturb the victim.



For a clock, this matters because any disturbance can shift the edge.



The playbook models crosstalk using:



```text

Crosstalk Aggressor Alignment

```



Options:



```text

Quiet / Orthogonal

In-Phase

Out-of-Phase

```



\---



\## 19. Layman Explanation — Crosstalk as Road Interference



Imagine two people walking side by side on a narrow bridge.



If one person suddenly moves sideways, the other person may be pushed slightly.



Similarly, if a nearby signal switches strongly, it can disturb the clock route.



The clock is the victim.



The nearby switching net is the aggressor.



This disturbance can move the clock edge.



\---



\## 20. Crosstalk Modes in the Playbook



\### Quiet / Orthogonal



This means the aggressor is not strongly aligned with the victim clock.



Default:



```text

Crosstalk Edge Shift = 0 ps

Crosstalk Jitter     = 8 fs

```



\### In-Phase



The aggressor switches in a way that pushes the victim edge in one direction.



Playbook model:



```text

Crosstalk Edge Shift = +0.75 ps

Crosstalk Jitter     = 32 fs

```



\### Out-of-Phase



The aggressor switches in the opposite alignment.



Playbook model:



```text

Crosstalk Edge Shift = -0.75 ps

Crosstalk Jitter     = 38 fs

```



The exact values are architecture-level sensitivity values.



The important concept is that crosstalk can create deterministic edge shift and additional uncertainty.



\---



\## 21. Interactive Experiment 2 — Enable In-Phase Crosstalk



In the sidebar:



```text

Crosstalk Aggressor Alignment = In-Phase

```



Observe:



```text

Crosstalk edge shift becomes positive

Crosstalk jitter increases

Waveform edge movement changes

Recommendation suggests shielding and SI-aware routing

```



Interpretation:



> The clock route is sensitive to nearby switching activity.



\---



\## 22. Interactive Experiment 3 — Enable Out-of-Phase Crosstalk



Change:



```text

Crosstalk Aggressor Alignment = Out-of-Phase

```



Observe:



```text

Crosstalk edge shift becomes negative

Waveform shifts in the opposite direction

Crosstalk jitter changes

```



Interpretation:



> Aggressor alignment affects the direction and nature of clock edge movement.



This demonstrates why SI-aware routing is important for clock nets.



\---



\## 23. Shielding



Shielding protects a critical clock route by placing stable reference wires around it.



Shielding can help reduce:



```text

Coupling noise

Crosstalk sensitivity

Aggressor-induced edge movement

Clock uncertainty

```



Common shielding strategies include:



```text

Ground shield

Power/ground shield

Spacing from aggressors

Dedicated protected routing tracks

Higher metal layer routing

```



The playbook models shielding as part of:



```text

Enable Shielding + Decaps

```



\---



\## 24. Decaps



Decaps are decoupling capacitors.



They act like small local charge reservoirs.



When a nearby circuit suddenly needs current, decaps can supply some of that current locally.



This helps reduce fast local VDD droop.



In simple words:



> A decap is like a small local battery that helps stabilize voltage during sudden switching.



Decaps help reduce:



```text

Dynamic VDD droop

Power supply noise

Clock buffer delay shift

PSIJ

Timing uncertainty

```



\---



\## 25. Shielding + Decaps Toggle in the Playbook



The playbook provides:



```text

Enable Shielding + Decaps

```



When enabled:



```text

Mitigation factor = 0.35

```



When disabled or partial:



```text

Mitigation factor = 0.72

```



This affects:



```text

After slew

After total jitter

After edge shift

Heatmap effective droop

```



The point is not to claim exact signoff mitigation.



The point is to demonstrate:



```text

Physical problem

&#x20;   ↓

Architecture mitigation

&#x20;   ↓

Improved waveform / budget behavior

```



\---



\## 26. Interactive Experiment 4 — Disable Shielding + Decaps



In the sidebar:



```text

Enable Shielding + Decaps = OFF

```



Observe:



```text

Residual endpoint jitter becomes higher

After-mitigation waveform becomes worse

IR-drop heatmap effect becomes stronger

Recommendations warn when noise exists without mitigation

```



Interpretation:



> Without mitigation, the clock path becomes more sensitive to droop and crosstalk.



Now enable it again.



Observe:



```text

Waveform improves

Endpoint uncertainty reduces

Architecture recommendation confirms mitigation path

```



\---



\## 27. Why Clock Buffers Should Avoid Hotspots



Clock buffers placed inside high-switching regions can experience stronger local VDD droop.



If a critical clock buffer sits inside a droop hotspot:



```text

Local VDD reduces

Buffer delay increases

Clock edge shifts

Endpoint uncertainty increases

Setup/hold margin may reduce

```



So physical implementation should consider:



```text

Clock buffer placement

Power-grid strength

Decap placement

Switching activity maps

Local EMIR hotspots

```



This is why clock planning is not isolated from power planning.



\---



\## 28. AI SoC Context



In AI SoCs, power integrity is especially important because large compute arrays can switch together.



Examples:



```text

Matrix multiply arrays

MAC units

Vector engines

SRAM read/write bursts

NoC traffic bursts

HBM interface activity

Clock-gated blocks waking up

```



These activities create dynamic current demand.



That current demand creates droop.



Droop affects clock buffers.



Clock buffer delay movement affects timing.



The chain is:



```text

High switching activity

&#x20;   ↓

Dynamic current spike

&#x20;   ↓

Local VDD droop

&#x20;   ↓

Clock buffer delay shift

&#x20;   ↓

Clock edge movement

&#x20;   ↓

Timing uncertainty

&#x20;   ↓

Setup/Hold margin risk

```



The playbook makes this chain visible.



\---



\## 29. How EMIR Awareness Connects to Setup/Hold



Setup and hold timing depend on clock edge position.



If IR-drop shifts the clock edge:



```text

Capture clock may move

Effective skew may change

Setup margin may reduce

Hold margin may reduce

```



If crosstalk shifts the clock edge:



```text

Clock arrival becomes less predictable

Timing uncertainty increases

Endpoint jitter increases

```



Therefore, EMIR and SI effects must be considered in timing closure.



The playbook does not perform signoff EMIR timing correlation, but it explains why that correlation is necessary.



\---



\## 30. Mapping This Note to the Playbook



| Concept              | Playbook Location                     |

| -------------------- | ------------------------------------- |

| Dynamic VDD droop    | Sidebar → Real Silicon Enemies        |

| PSIJ edge shift      | IR-Drop / Crosstalk tab and Live Math |

| PSIJ jitter          | Jitter Budget tab                     |

| Crosstalk mode       | Sidebar selector                      |

| Crosstalk edge shift | IR-Drop / Crosstalk tab               |

| Shielding + decaps   | Sidebar toggle                        |

| Droop hotspot        | IR-drop heatmap                       |

| Clock path exposure  | Heatmap overlay                       |

| Architecture fix     | Recommendations tab                   |



\---



\## 31. Default Power / EMIR Awareness Summary



Default values:



```text

Dynamic VDD Droop  = 45 mV

Crosstalk Mode     = Quiet / Orthogonal

Shielding + Decaps = ON

```



Calculated:



```text

PSIJ Edge Shift    = 0.216 ps

PSIJ Jitter        = 81 fs

Crosstalk Shift    = 0 ps

Crosstalk Jitter   = 8 fs

Mitigation Factor  = 0.35

```



Interpretation:



```text

Droop creates a measurable clock edge shift.

Crosstalk is quiet in the default case.

Mitigation is enabled, so residual endpoint impact is reduced.

```



\---



\## 32. Practical Review Questions



A mature SoC clock review should ask:



```text

Is the clock network consuming too much dynamic power?

Are repeaters increasing power and EMIR stress?

Is local VDD droop affecting clock buffers?

Are critical clock buffers placed near switching hotspots?

Are decaps placed near sensitive clock regions?

Is the power grid strong enough for clock activity?

Are clock routes shielded from aggressors?

Is crosstalk alignment creating deterministic edge shift?

Is EMIR correlated with timing uncertainty?

Are setup and hold margins still safe under droop?

```



The playbook helps users explore these questions interactively.



\---



\## 33. Architecture Actions



If dynamic VDD droop is high:



```text

Strengthen local power grid

Add decaps near clock buffers

Avoid clock-buffer placement in hotspots

Spread switching activity where possible

Review clock power

Review EMIR maps

Use power-aware CTS

```



If crosstalk is high:



```text

Add shielding

Increase spacing

Use higher metal layers

Avoid long parallel aggressor-victim routes

Use SI-aware routing

Review clock/data adjacency

```



If clock power is high:



```text

Optimize repeater count

Reduce unnecessary clock loading

Use clock gating carefully

Review clock mesh/tree choice

Reduce over-buffering

Check EM current density

```



If setup/hold becomes risky under droop:



```text

Correlate timing with EMIR

Review endpoint voltage condition

Improve local supply

Reduce clock uncertainty

Avoid aggressive useful skew without hold analysis

```



\---



\## 34. Why This App Is Useful for EMIR Awareness



Traditional EMIR analysis may show voltage drop maps.



STA may show timing violations.



SI tools may show coupling effects.



But these are often reviewed separately.



The playbook connects them conceptually:



```text

Droop slider

&#x20;   ↓

PSIJ calculation

&#x20;   ↓

Waveform edge shift

&#x20;   ↓

Jitter budget

&#x20;   ↓

Timing margin awareness

&#x20;   ↓

Architecture recommendation

```



This makes it easier to understand why EMIR, SI, CTS, and STA must be reviewed together.



\---



\## 35. What This Model Does Not Claim



The playbook does not claim final EMIR signoff accuracy.



It does not replace:



```text

RedHawk / Voltus style EMIR analysis

Extracted power-grid simulation

Vector-based dynamic IR-drop

Foundry EM rules

Current-density signoff

Thermal-aware reliability analysis

SI extraction

Full STA correlation

```



The current heatmap is synthetic and normalized.



The current PSIJ and crosstalk values are architecture-level sensitivity values.



The purpose is:



```text

Education

Early design review

Concept demonstration

Interactive what-if analysis

Communication between timing, PD, SI, and EMIR teams

```



\---



\## 36. Final Takeaway



Clock distribution is connected to power integrity.



A clock network:



```text

Consumes power

Drives large capacitance

Uses many buffers

Creates switching current

Depends on stable VDD

Can be disturbed by nearby aggressors

Can suffer from local droop

Can contribute to EMIR stress

```



Therefore, clock signoff is not only about tree balance.



It must also consider:



```text

Power grid

Decaps

Shielding

Crosstalk

Local activity

EMIR hotspots

Timing uncertainty

Setup/Hold margin

```



The \*\*Interactive SoC Clock Distribution Playbook\*\* makes this connection visible.



It shows how power and noise effects move the clock edge, increase uncertainty, and influence final timing closure.



The core lesson is:



> In modern SoCs, clock timing cannot be separated from power integrity.



