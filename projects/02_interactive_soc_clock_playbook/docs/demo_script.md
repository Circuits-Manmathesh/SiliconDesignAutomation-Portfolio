\# Demo Script — Interactive SoC Clock Distribution Playbook



\## A Step-by-Step Presentation Guide for GitHub, LinkedIn, Professor, and Industry Review



\---



\## 1. Purpose of This Demo Script



This demo script explains how to present the \*\*Interactive SoC Clock Distribution Playbook\*\* in a realistic and technically mature way.



The goal is not to claim that this app replaces production signoff tools.



The correct positioning is:



> This is an architecture-level interactive sensitivity-analysis and learning playbook that makes the PLL-to-flip-flop clock journey visible, measurable, and explainable.



This demo should show that we understand how clock distribution behaves as a full system:



```text

PLL source quality

&#x20;   ↓

Duty-cycle distortion

&#x20;   ↓

Clock conditioning

&#x20;   ↓

Global interconnect RC

&#x20;   ↓

Repeater / buffer tradeoff

&#x20;   ↓

Regional skew

&#x20;   ↓

Local IR-drop

&#x20;   ↓

Crosstalk

&#x20;   ↓

Jitter / uncertainty

&#x20;   ↓

Setup / hold timing closure

&#x20;   ↓

Architecture recommendation

```



The presentation style should be confident, technical, and honest.



Do not overclaim silicon signoff accuracy.



Present the app as a strong educational and architecture-review tool.



\---



\## 2. How to Launch the Application



Open terminal or CMD:



```bat

cd /d C:\\Interactive\_Soc\_Clock\_Playbook

.venv\\Scripts\\activate

streamlit run app.py

```



Or run:



```bat

run\_playbook.bat

```



After this, Streamlit will open the dashboard in the browser.



Expected app title:



```text

Interactive SoC Clock Distribution Playbook

```



Expected tabs:



```text

1\. Overview

2\. SoC Journey Map

3\. Waveform Lab

4\. Live Math

5\. Jitter / Skew Budget

6\. IR-Drop / Crosstalk

7\. Timing Closure

8\. Recommendations

```



\---



\## 3. Opening Statement for the Demo



Use this opening when starting the video or technical discussion:



```text

Today I am demonstrating an Interactive SoC Clock Distribution Playbook.



The objective of this project is to make the complete clock journey from PLL to flip-flop visible and explainable.



In real silicon, a clock is not just a perfect digital square wave. It is an analog timing signal affected by PLL jitter, duty-cycle distortion, interconnect RC, repeater insertion delay, IR-drop, crosstalk, skew, setup margin, and hold margin.



This playbook connects all of these effects into one interactive architecture-level workflow.



It is not a replacement for signoff STA, SI, EMIR, or extracted timing analysis. Instead, it is a visual sensitivity-analysis and learning tool that helps understand how each clock-distribution knob affects waveform quality, timing budget, and final setup/hold closure.

```



\---



\## 4. Default Demo Scenario



Keep the default sidebar values first.



These default values represent a controlled 5 GHz SoC clock-distribution baseline.



\### PLL / Clock Source



```text

Clock Frequency       = 5.0 GHz

PLL Random Jitter     = 120 fs

PLL Duty Cycle        = 51.5 %

```



\### Global Interconnect / CDN



```text

Global Wire Length    = 2400 µm

Top Metal Sheet R     = 28 mΩ/sq

Wire Capacitance      = 95 aF/µm

Repeater Count        = 4

```



\### Real Silicon Enemies



```text

Dynamic VDD Droop     = 45 mV

Crosstalk Mode        = Quiet / Orthogonal

Shielding + Decaps    = ON

```



\### Flip-Flop Timing



```text

Logic Path Delay      = 175 ps

Spatial Clock Skew    = 8 ps

Useful Skew           = 0 ps

Setup Requirement     = 8 ps

Hold Requirement      = 5 ps

```



Say:



```text

I am starting with the default 5 GHz baseline. At 5 GHz, the clock period is only 200 ps, so even picosecond-level effects can become visible in the timing budget.

```



\---



\## 5. Tab 1 — Overview



Open:



```text

1\. Overview

```



Explain:



```text

This overview tab summarizes the current clock architecture condition.



The top metric strip gives a quick health view of the design:

```



Expected baseline values:



```text

Clock Period       = 200.000 ps

RC Segment Tau     = 7.661 ps

Endpoint Jitter    = 485.291 fs

Setup Slack        = 25.000 ps

Hold Slack         = 162.000 ps

```



Explain each metric:



```text

Clock Period is 200 ps because the frequency is 5 GHz.



RC Segment Tau tells us the effective RC severity after repeater segmentation.



Endpoint Jitter is the residual clock uncertainty after mitigation.



Setup Slack and Hold Slack tell us whether the final flip-flop capture is safe under the simplified architecture-level model.

```



Important statement:



```text

This top strip connects the clock-distribution problem to final timing closure. It is not only showing waveform quality; it is showing whether the clock can still support setup and hold timing at the endpoint.

```



\---



\## 6. Tab 2 — SoC Journey Map



Open:



```text

2\. SoC Journey Map

```



Explain:



```text

This tab visualizes the clock journey from PLL to flip-flop.



The path is:

PLL → Divider → Global Trunk → Regional Branch → Local Leaf → Flip-Flop.

```



Clarify:



```text

This is a normalized architecture map, not a physical DEF floorplan. The purpose is to show how clock quality evolves stage by stage.

```



Explain each node:



\### PLL



```text

The PLL is the clock source. This is where the clock starts with source jitter and duty-cycle distortion.

```



\### Divider



```text

The divider or clock-conditioning stage can improve duty-cycle behavior and prepare the clock before global distribution.

```



\### Global Trunk



```text

The global trunk is the long top-metal route that carries the clock across the SoC. This is where interconnect RC becomes important.

```



\### Regional Branch



```text

The regional branch distributes the clock into local SoC regions such as compute blocks, memory regions, NoC regions, or PHY areas.

```



\### Local Leaf



```text

The local leaf is near the final sequential cells. Local IR-drop, buffer mismatch, and local routing effects become important here.

```



\### Flip-Flop



```text

The flip-flop is the final capture point. This is where setup and hold timing decide whether the clock distribution is acceptable.

```



Then point to node table:



```text

Each node has accumulated delay, jitter RMS, local skew, VDD droop, and slew. This helps us understand where clock quality starts degrading.

```



\---



\## 7. Tab 3 — Waveform Lab



Open:



```text

3\. Waveform Lab

```



Explain:



```text

This is the waveform view. It compares ideal, degraded, and mitigated clock waveforms.

```



\### Ideal Clock



```text

The ideal clock is the theoretical reference: 50% duty cycle, no jitter, sharp edge, and no edge shift.

```



\### Degraded Clock



```text

The degraded clock includes PLL jitter, duty-cycle distortion, RC slew degradation, repeater insertion delay, IR-drop edge shift, and crosstalk contribution.

```



\### Mitigated Clock



```text

The mitigated clock shows how architecture-level mitigation improves the final waveform. This includes shielding, decaps, better segmentation, and clock-conditioning effect.

```



Point to metrics:



```text

Before Slew    = 19.186 ps

After Slew     = 6.715 ps

Before Jitter  = 1386.547 fs

After Jitter   = 485.291 fs

DCD            = 1.500 %

```



Say:



```text

The important point is that this waveform is not a static image. It is generated from the current clock architecture values. When we change wire length, repeater count, VDD droop, crosstalk, or PLL jitter, the waveform responds immediately.

```



\---



\## 8. Tab 4 — Live Math



Open:



```text

4\. Live Math

```



Explain:



```text

This is the trust-building tab. Every major value is connected to a formula, substitution, calculated value, physical meaning, and risk/action.

```



Show baseline formulas:



\### Clock Period



```text

Tclk = 1000 / fGHz

Tclk = 1000 / 5

Tclk = 200 ps

```



\### Wire Resistance



```text

Squares = WireLength / WireWidth

Squares = 2400 / 0.08

Squares = 30000



Rwire = Rsheet × Squares

Rwire = 0.028 × 30000

Rwire = 840 Ω

```



\### Wire Capacitance



```text

Cwire = Cper\_um × WireLength

Cwire = 95 aF/µm × 2400 µm

Cwire = 228 fF

```



\### Segment RC



```text

τsegment = τRC / (Nrepeaters + 1)²

τsegment = 191.52 / 25

τsegment = 7.661 ps

```



Say:



```text

This tab prevents the app from becoming a black box. The user can directly see why the waveform, budget, and timing values are changing.

```



\---



\## 9. Tab 5 — Jitter / Skew Budget



Open:



```text

5\. Jitter / Skew Budget

```



Explain:



```text

This tab decomposes clock uncertainty and skew into visible contributors.

```



\### Jitter Budget



Default values:



```text

PLL Random Jitter       = 120 fs

RC Slew Uncertainty     = 1378.944 fs

PSIJ                    = 81 fs

Crosstalk               = 8 fs

Before Mitigation Total = 1386.547 fs

After Mitigation Total  = 485.291 fs

```



Explain:



```text

The endpoint uncertainty is not coming from one source. It is a combination of PLL jitter, RC slew uncertainty, power-supply-induced jitter, and crosstalk uncertainty.

```



Formula:



```text

Jtotal = sqrt(Jpll² + Jrc² + Jpsij² + Jxtalk²)

```



\### Skew Budget



Default values:



```text

Trunk Mismatch          = 6.00 ps

Regional Mismatch       = 3.50 ps

Local Buffer Mismatch   = 2.85 ps

Spatial Clock Skew      = 8.00 ps

Useful Skew             = 0.00 ps

Final Effective Skew    = 8.00 ps

```



Explain:



```text

Skew is separated into natural spatial skew and intentional useful skew. This is important because skew is not always bad. Controlled useful skew can improve setup, but it can also create hold risk.

```



\---



\## 10. Tab 6 — IR-Drop / Crosstalk



Open:



```text

6\. IR-Drop / Crosstalk

```



Explain:



```text

This tab shows how power integrity and signal integrity become clock timing integrity.

```



Point to default values:



```text

Dynamic VDD Droop = 45 mV

PSIJ Edge Shift   = 0.216 ps

Crosstalk Mode    = Quiet / Orthogonal

Crosstalk Shift   = 0 ps

Shielding + Decaps = ON

```



Explain:



```text

When VDD droops, clock buffers slow down. That delay change moves the clock edge. This is power-supply-induced jitter.

```



Formula:



```text

ΔtPSIJ = kdroop × Vdroop

ΔtPSIJ = 0.0048 × 45

ΔtPSIJ = 0.216 ps

```



Say:



```text

The heatmap is synthetic and normalized. It is not an extracted EMIR map. Its purpose is to show how droop hotspots can overlap with clock paths.

```



\---



\## 11. Interactive Stress Example — Increase Dynamic Droop



Change sidebar:



```text

Dynamic VDD Droop = 70 mV

```



Explain:



```text

Now PSIJ increases.

```



Calculation:



```text

ΔtPSIJ = 0.0048 × 70

ΔtPSIJ = 0.336 ps

```



```text

Jpsij = 1.8 × 70

Jpsij = 126 fs

```



Say:



```text

As droop increases, the clock edge becomes more sensitive to local power conditions. This is why decap placement and power-grid strength matter for timing.

```



\---



\## 12. Interactive Stress Example — Crosstalk



Change sidebar:



```text

Crosstalk Aggressor Alignment = In-Phase

```



Explain:



```text

Now the aggressor alignment creates deterministic edge shift.

```



Expected model behavior:



```text

Crosstalk Edge Shift = +0.75 ps

Crosstalk Jitter     = 32 fs

```



Say:



```text

This demonstrates that crosstalk is not only an SI issue. If the victim is a clock, crosstalk becomes a timing issue.

```



Now change:



```text

Crosstalk Aggressor Alignment = Out-of-Phase

```



Explain:



```text

Now the crosstalk edge shift becomes negative. This shows that aggressor alignment affects the direction of clock edge movement.

```



\---



\## 13. Shielding + Decaps Demonstration



Toggle:



```text

Enable Shielding + Decaps = OFF

```



Explain:



```text

When mitigation is disabled, residual endpoint uncertainty becomes higher and the waveform becomes more sensitive to droop and crosstalk.

```



Then toggle it back:



```text

Enable Shielding + Decaps = ON

```



Explain:



```text

When shielding and decaps are enabled, the model reduces residual noise impact. This demonstrates the architectural fix path: identify the physical issue, apply mitigation, and observe improved waveform and budget behavior.

```



\---



\## 14. Tab 7 — Timing Closure



Open:



```text

7\. Timing Closure

```



Explain:



```text

This is where clock distribution meets the final flip-flop timing decision.

```



Default baseline:



```text

Clock Period      = 200 ps

Logic Delay       = 175 ps

Spatial Skew      = 8 ps

Useful Skew       = 0 ps

Setup Requirement = 8 ps

Hold Requirement  = 5 ps

```



Calculate:



```text

EffectiveSkew = 8 + 0

EffectiveSkew = 8 ps

```



```text

CaptureClock = Period + EffectiveSkew

CaptureClock = 200 + 8

CaptureClock = 208 ps

```



```text

SetupSlack = CaptureClock - SetupRequirement - DataArrival

SetupSlack = 208 - 8 - 175

SetupSlack = 25 ps

```



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

HoldSlack = 175 - (8 + 5)

HoldSlack = 162 ps

```



Say:



```text

Both setup and hold are positive, so the baseline timing path passes.

```



\---



\## 15. Interactive Timing Example — Create Setup Violation



Change sidebar:



```text

Logic Path Delay   = 203 ps

Spatial Clock Skew = 10 ps

Useful Skew        = 0 ps

```



Explain:



```text

Now the data path is slower.

```



Calculation:



```text

CaptureClock = 200 + 10 + 0

CaptureClock = 210 ps

```



```text

SetupSlack = 210 - 8 - 203

SetupSlack = -1 ps

```



Say:



```text

Setup slack is negative. This means the data arrives 1 ps too late. The app should show SETUP VIOLATION.

```



\---



\## 16. Interactive Timing Example — Recover Setup Using Useful Skew



Now change:



```text

Useful Skew = +8 ps

```



Calculation:



```text

EffectiveSkew = 10 + 8

EffectiveSkew = 18 ps

```



```text

CaptureClock = 200 + 18

CaptureClock = 218 ps

```



```text

SetupSlack = 218 - 8 - 203

SetupSlack = 7 ps

```



Say:



```text

Useful skew delayed the capture edge and gave the data more time. Setup is recovered.

```



Important warning:



```text

But this does not mean useful skew is always safe. We must check hold.

```



\---



\## 17. Interactive Timing Example — Create Hold Violation



Change sidebar:



```text

Logic Path Delay   = 28 ps

Spatial Clock Skew = 10 ps

Useful Skew        = 18 ps

Hold Requirement   = 5 ps

```



Calculation:



```text

EffectiveSkew = 10 + 18

EffectiveSkew = 28 ps

```



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

HoldSlack = 28 - (28 + 5)

HoldSlack = -5 ps

```



Say:



```text

Now hold slack is negative. This means the data changes too early. The app should show HOLD VIOLATION.

```



Key lesson:



```text

Useful skew can fix setup, but it can create hold risk on short paths.

```



\---



\## 18. Tab 8 — Recommendations



Open:



```text

8\. Recommendations

```



Explain:



```text

This tab converts live calculations into architecture recommendations.

```



Examples:



```text

If clock period is tight, track clock uncertainty and skew carefully.

If duty-cycle distortion is present, keep clock conditioning visible in the budget.

If dynamic IR-drop is active, review decaps, power grid, and clock-buffer placement.

If endpoint jitter is high, separate PLL, RC, PSIJ, and crosstalk contributors.

If setup fails, reduce logic delay, improve slew, pipeline, or apply useful skew carefully.

If hold fails, add hold buffers or reduce harmful useful skew.

```



Say:



```text

This is useful because the app does not stop at visualization. It maps physical observations into architecture actions.

```



\---



\## 19. Full Demo Flow Summary



For a short demo, follow this order:



```text

1\. Launch app

2\. Explain objective

3\. Show Overview metrics

4\. Show SoC Journey Map

5\. Show Waveform Lab

6\. Show Live Math

7\. Show Jitter / Skew Budget

8\. Show IR-Drop / Crosstalk

9\. Show Timing Closure baseline

10\. Create setup violation

11\. Recover setup using useful skew

12\. Create hold violation

13\. Show Recommendations

14\. Close with scope and takeaway

```



\---



\## 20. Short 3-Minute Demo Version



Use this if the demo must be short.



```text

This is an Interactive SoC Clock Distribution Playbook.



It follows the clock from PLL to flip-flop and shows how clock quality changes through PLL jitter, duty-cycle distortion, interconnect RC, repeaters, IR-drop, crosstalk, skew, and final setup/hold timing.



At 5 GHz, the clock period is 200 ps. The baseline shows 7.661 ps segment RC, 485 fs endpoint jitter, 25 ps setup slack, and 162 ps hold slack.



The SoC Journey Map shows clock quality node by node from PLL to flip-flop.



The Waveform Lab shows ideal, degraded, and mitigated waveforms.



The Live Math tab shows every formula and calculated value, so the app is explainable rather than a black box.



The Budget tab separates PLL jitter, RC uncertainty, PSIJ, crosstalk, spatial skew, and useful skew.



The IR-Drop tab shows how power-grid droop can shift clock edges and why decaps and shielding matter.



The Timing Closure tab demonstrates that useful skew can recover setup margin, but it can also create hold violation on short paths.



The Recommendation tab converts these observations into architecture actions.



This app is not a signoff replacement. Final silicon signoff still requires SPEF, Liberty, STA, SI, EMIR, PVT, and OCV correlation. But this playbook makes the clock-distribution problem visible, measurable, and easier to explain.

```



\---



\## 21. Longer 8–10 Minute Demo Version



Use this if you are presenting to a professor, interviewer, or senior engineer.



\### Step 1 — Start with the problem



```text

Modern SoCs have large clock-distribution networks. The clock travels across long wires, multiple buffers, regional branches, and local leaf cells before reaching the flip-flop. During this journey, the edge degrades, shifts, accumulates uncertainty, and becomes sensitive to power and coupling noise.

```



\### Step 2 — Show the baseline



```text

I am using a 5 GHz baseline. The clock period is 200 ps. This gives a realistic sense of timing pressure.

```



\### Step 3 — Explain RC



```text

The global wire length is 2400 µm. The app calculates wire resistance, wire capacitance, total RC tau, and effective segment RC after repeaters.

```



\### Step 4 — Explain waveform



```text

The degraded waveform is generated from the live architecture parameters. The mitigated waveform shows how shielding, decaps, and clock-conditioning reduce residual degradation.

```



\### Step 5 — Explain uncertainty



```text

The app decomposes endpoint jitter into PLL jitter, RC uncertainty, PSIJ, and crosstalk. This helps identify the dominant contributor.

```



\### Step 6 — Explain power/timing link



```text

Dynamic VDD droop changes clock-buffer delay. This creates PSIJ and edge shift. This is why EMIR awareness is necessary for clock timing.

```



\### Step 7 — Explain timing closure



```text

The final flip-flop timing check uses setup and hold equations. Useful skew can improve setup but can also reduce hold margin.

```



\### Step 8 — Show recommendations



```text

The app maps current risks into architecture actions, such as repeater optimization, decap placement, shielding, power-grid strengthening, useful-skew review, and hold-buffer insertion.

```



\### Step 9 — Finish with scope



```text

This is not replacing production signoff. It is an architecture-level explanation and sensitivity-analysis layer. Final signoff still needs extracted parasitics, Liberty models, STA, SI, EMIR, PVT, and OCV correlation.

```



\---



\## 22. Suggested LinkedIn Caption



```text

I built an Interactive SoC Clock Distribution Playbook to make PLL-to-flip-flop clock behavior visible.



The app shows how a clock edge degrades and shifts due to PLL jitter, duty-cycle distortion, interconnect RC, repeater insertion delay, dynamic IR-drop, crosstalk, skew, and setup/hold constraints.



It includes live waveforms, SoC journey mapping, formulas, jitter/skew budgets, IR-drop awareness, timing closure diagrams, and architecture recommendations.



This is not a signoff replacement; it is an architecture-level sensitivity-analysis and learning tool to make clock distribution easier to understand and explain.

```



\---



\## 23. Suggested GitHub Short Description



```text

Interactive Streamlit playbook for SoC clock distribution analysis: PLL jitter, RC slew, repeater tradeoff, IR-drop, crosstalk, skew, setup/hold timing, and architecture recommendations.

```



\---



\## 24. Suggested Repository Tags



```text

vlsi

soc

clock-distribution

timing-analysis

sta

cts

jitter

skew

ir-drop

emir

streamlit

plotly

python

semiconductor

physical-design

digital-design

```



\---



\## 25. Final Closing Statement



Use this closing statement for a strong but technically safe ending:



```text

The biggest learning from this playbook is that clock distribution is not only a routing task.



It is a system-level timing architecture problem.



A clock edge starts with PLL quality, passes through RC interconnect, repeaters, regional branches, local power noise, crosstalk, skew, and finally reaches the flip-flop setup/hold window.



This app makes that complete journey visible and explainable.



It helps identify not only what changed, but why it changed and which architecture knob can improve it.

```



