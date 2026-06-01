\# Interactive SoC Clock Distribution Playbook



An interactive, visual, and explainable Python/Streamlit playbook for understanding how a clock signal travels from \*\*PLL to flip-flop\*\* across a modern SoC clock distribution network.



This project converts clock distribution from a scattered report-based topic into a connected, interactive architecture review:



```text

PLL

&#x20;↓

Divider

&#x20;↓

Global Clock Trunk

&#x20;↓

Regional Clock Branch

&#x20;↓

Local Clock Leaf

&#x20;↓

Flip-Flop Capture

```



The main objective is \*\*complexity reduction\*\*: to make clock degradation, jitter accumulation, skew movement, IR-drop sensitivity, crosstalk effects, and setup/hold timing closure easier to understand through live waveforms, live formulas, SoC path visualization, and architecture recommendations.



\---



\## 1. Project Motivation



In real silicon, a clock is not just a perfect digital square wave.



It is an analog timing signal travelling through a complex physical environment:



\* PLL phase noise moves the clock edge.

\* Duty-cycle distortion changes high/low pulse symmetry.

\* Long global wires introduce resistance, capacitance, delay, and slew degradation.

\* Repeaters restore edge quality but add insertion delay and power.

\* Dynamic IR-drop slows clock buffers and creates power-supply-induced jitter.

\* Crosstalk from nearby aggressor nets shifts the victim clock edge.

\* Spatial clock skew changes setup and hold margins.

\* Useful skew can fix setup but may create hold risk.

\* Flip-flop setup/hold checks finally decide whether the design is timing-safe.



Traditional clock analysis often involves separate views:



```text

STA reports

CTS reports

SI reports

EMIR reports

Excel budget sheets

Waveform debug

```



This playbook does not replace those signoff tools. Instead, it gives a single interactive explanation layer where the user can change architecture parameters and immediately see how the clock waveform, clock journey, mathematical budget, timing closure, and recommendation engine respond together.



\---



\## 2. What This Application Demonstrates



The application demonstrates a complete clock-distribution learning and architecture-analysis flow:



```text

Clock Source Quality

&#x20;       ↓

Interconnect RC Degradation

&#x20;       ↓

Repeater / Buffer Tradeoff

&#x20;       ↓

IR-Drop and Crosstalk Sensitivity

&#x20;       ↓

Jitter / Skew Budgeting

&#x20;       ↓

Setup / Hold Timing Closure

&#x20;       ↓

Architecture Recommendation

```



The app is designed for:



\* Students learning clock distribution.

\* Engineers preparing for SoC/STA/CTS discussions.

\* Physical-design and timing engineers explaining clock risk.

\* Architecture-level reviews where early sensitivity analysis is needed.

\* GitHub/LinkedIn demonstration of system-level silicon understanding.



\---



\## 3. Screenshots



Place screenshots inside the `screenshots/` folder using the following names.



\### Project Overview



!\[Project Overview](screenshots/overview.png)



\### SoC Clock Journey Map



!\[SoC Journey Map](screenshots/soc\_journey\_map.png)



\### Waveform Lab



!\[Waveform Lab](screenshots/waveform\_lab.png)



\### Live Math Analysis



!\[Live Math Analysis](screenshots/live\_math.png)



\### Jitter / Skew Budget



!\[Jitter Skew Budget](screenshots/jitter\_skew\_budget.png)



\### IR-Drop / Crosstalk Awareness



!\[IR Drop Crosstalk](screenshots/ir\_drop\_crosstalk.png)



\### Timing Closure



!\[Timing Closure](screenshots/timing\_closure.png)



\### Architecture Recommendations



!\[Architecture Recommendations](screenshots/recommendations.png)



\---



\## 4. Key Features



\### 4.1 Interactive Sidebar Controls



The user can control the complete clock scenario from the sidebar:



\#### PLL / Clock Source



\* Clock frequency

\* PLL random jitter

\* PLL duty cycle



\#### Global Interconnect / Clock Distribution Network



\* Global wire length

\* Top-metal sheet resistance

\* Wire capacitance

\* Repeater / buffer count



\#### Real Silicon Enemies



\* Dynamic VDD droop

\* Crosstalk aggressor alignment

\* Shielding + decap mitigation toggle



\#### Flip-Flop Timing



\* Logic path delay

\* Spatial clock skew

\* Useful skew

\* Setup requirement

\* Hold requirement



Every slider updates the full dashboard live.



\---



\## 5. Application Tabs



The Streamlit app is organized into eight technical tabs.



\---



\### Tab 1 — Overview



This tab introduces the complete PLL-to-flip-flop clock-distribution problem.



It explains that the clock is not only a digital signal but a physical timing waveform affected by:



\* Source jitter

\* Duty-cycle distortion

\* Interconnect RC

\* Repeater insertion delay

\* IR-drop

\* Crosstalk

\* Skew

\* Setup/hold timing



The top metric strip gives immediate visibility into:



```text

Clock Period

RC Segment Tau

Endpoint Jitter

Setup Slack

Hold Slack

```



For the default 5 GHz demo case:



```text

Clock Period       = 200.000 ps

RC Segment Tau     = 7.661 ps

Endpoint Jitter    = 485.291 fs

Setup Slack        = 25.000 ps

Hold Slack         = 162.000 ps

```



\---



\### Tab 2 — SoC Journey Map



This tab shows a normalized clock journey:



```text

PLL → Divider → Global Trunk → Regional Branch → Local Leaf → Flip-Flop

```



Each node displays:



\* Accumulated delay

\* Jitter RMS

\* Local skew

\* VDD droop

\* Slew



The purpose is to show that clock quality evolves gradually as the signal travels across the SoC.



The node coordinates are normalized visualization coordinates, not physical DEF floorplan coordinates. Future versions can replace these with actual placement/floorplan data.



\---



\### Tab 3 — Waveform Lab



This tab generates live mathematical waveforms:



```text

Ideal Clock

Degraded Clock

Mitigated Clock

```



The ideal clock is the theoretical reference.



The degraded clock includes:



\* PLL random jitter

\* Duty-cycle distortion

\* RC slew degradation

\* Repeater insertion delay

\* PSIJ edge shift

\* Crosstalk edge shift



The mitigated clock includes the improvement from architecture-level mitigation such as:



\* Shielding

\* Decaps

\* Clock conditioning

\* Better segmentation

\* Reduced sensitivity to noise sources



The waveform is not a static image. It is generated programmatically from the current slider values.



\---



\### Tab 4 — Live Math Analysis



This is the trust-building tab.



Every major output is connected to:



```text

Formula

Input substitution

Calculated value

Physical meaning

Risk / action

```



Example:



```text

Tclk = 1000 / fGHz

Tclk = 1000 / 5 = 200 ps

```



The tab explains why waveform and timing values change when sliders move.



This is important because the app is not a black-box visualization. It is an explainable architecture model.



\---



\### Tab 5 — Jitter / Skew Budget



This tab decomposes uncertainty into budget components.



\#### Jitter Budget



The app tracks:



\* PLL random jitter

\* RC slew uncertainty

\* PSIJ

\* Crosstalk

\* Total before mitigation

\* Total after mitigation



The model uses a root-sum-square style combination:



```text

Jtotal = sqrt(Jpll² + Jrc² + Jpsij² + Jxtalk²)

```



\#### Skew Budget



The app separates:



\* Trunk mismatch

\* Regional mismatch

\* Local buffer mismatch

\* Spatial clock skew

\* Useful skew

\* Final effective skew



This distinction is important because skew is not always bad. Controlled useful skew can improve setup margin, but excessive skew may create hold risk.



\---



\### Tab 6 — IR-Drop / Crosstalk Awareness



This tab shows a normalized synthetic IR-drop heatmap with the clock path overlay.



The purpose is to explain how power integrity becomes timing integrity.



When many logic blocks switch together, current demand increases. Because the power grid is not ideal, local VDD droop appears. Clock buffers operating in that droop region become slower, so the clock edge shifts.



This is modeled as:



```text

ΔtPSIJ = kdroop × Vdroop

```



The tab also shows how crosstalk alignment can shift the clock edge:



```text

In-Phase Aggressor      → positive edge shift

Out-of-Phase Aggressor  → negative edge shift

Quiet / Orthogonal      → small residual coupling

```



This helps explain why shielding, spacing, and decap planning are important for clock distribution.



\---



\### Tab 7 — Timing Closure



This tab connects waveform behavior to flip-flop capture.



It visualizes:



```text

Launch Clock

Data Path

Capture Clock

Setup Window

Hold Window

```



The setup equation is:



```text

SetupSlack = CaptureClock - SetupRequirement - DataArrival

```



The hold equation is:



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

```



The app demonstrates a real timing tradeoff:



\* Positive useful skew can improve setup slack.

\* The same useful skew can reduce hold margin on short paths.



This makes the setup/hold relationship visible instead of only showing it as a report number.



\---



\### Tab 8 — Architecture Recommendations



This tab converts live calculations into design actions.



Example recommendations include:



\* Track clock uncertainty when frequency is high.

\* Review duty-cycle correction if DCD is present.

\* Improve repeater strategy when segment RC is high.

\* Strengthen decaps and power grid when droop is active.

\* Use shielding and spacing when crosstalk is active.

\* Use useful skew carefully for setup recovery.

\* Add hold buffers or reduce useful skew for hold risk.

\* Preserve timing margin even when nominal timing passes.



The recommendation cards are generated from live parameter values and timing status.



\---



\## 6. Default Demo Scenario



The default scenario is a 5 GHz AI SoC clock-distribution case.



\### Clock Source



```text

Clock Frequency       = 5.0 GHz

PLL Random Jitter     = 120 fs

PLL Duty Cycle        = 51.5 %

```



\### Global Interconnect / CDN



```text

Global Wire Length    = 2400 µm

Wire Width Assumption = 0.08 µm

Sheet Resistance      = 28 mΩ/sq

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



\---



\## 7. Baseline Calculation Reference



For the default 5 GHz scenario:



\### Clock Period



```text

Tclk = 1000 / fGHz

Tclk = 1000 / 5

Tclk = 200 ps

```



\### Wire Squares



```text

Squares = Wire Length / Wire Width

Squares = 2400 / 0.08

Squares = 30000

```



\### Wire Resistance



```text

Rwire = Rsheet × Squares

Rwire = 0.028 × 30000

Rwire = 840 Ω

```



\### Wire Capacitance



```text

Cwire = Cper\_um × Length

Cwire = 95 aF/µm × 2400 µm

Cwire = 228 fF

```



\### Total RC Tau



```text

τRC = Rwire × Cwire

τRC = 840 Ω × 228 fF

τRC = 191.52 ps

```



This is an architecture-level unbuffered RC severity indicator, not a final extracted clock delay.



\### Segment RC Tau



```text

Segments = RepeaterCount + 1

Segments = 4 + 1 = 5



τsegment = τRC / Segments²

τsegment = 191.52 / 25

τsegment = 7.6608 ps

```



\### Insertion Delay



```text

Insertion Delay = RepeaterCount × BufferDelay

Insertion Delay = 4 × 3.2

Insertion Delay = 12.8 ps

```



\### Setup Slack



```text

CaptureClock = Period + SpatialSkew + UsefulSkew

CaptureClock = 200 + 8 + 0

CaptureClock = 208 ps



SetupSlack = CaptureClock - SetupReq - DataArrival

SetupSlack = 208 - 8 - 175

SetupSlack = 25 ps

```



\### Hold Slack



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldReq)

HoldSlack = 175 - (8 + 5)

HoldSlack = 162 ps

```



\---



\## 8. Mathematical Models Used



The current playbook uses transparent architecture-level models.



\### Clock Period



```text

Tclk = 1000 / fGHz

```



\### Duty-Cycle Error



```text

DCD = |Duty - 50%|

```



\### Wire Resistance



```text

Squares = WireLength / WireWidth

Rwire = Rsheet × Squares

```



\### Wire Capacitance



```text

Cwire = Cper\_um × WireLength

```



\### RC Time Constant



```text

τRC = Rwire × Cwire

```



\### Repeater Segmentation



```text

Segments = Nrepeaters + 1

τsegment = τRC / Segments²

```



\### Repeater Insertion Delay



```text

Delayinsert = Nrepeaters × BufferDelay

```



\### Slew Approximation



```text

Slewbefore = BaseSlew + k × τsegment

Slewafter  = max(BaseSlew, Slewbefore × MitigationFactor)

```



\### Power Supply Induced Jitter / Edge Shift



```text

ΔtPSIJ = kdroop × Vdroop

```



\### Jitter Budget



```text

Jtotal = sqrt(Jpll² + Jrc² + Jpsij² + Jxtalk²)

```



\### Setup Slack



```text

SetupSlack = CaptureClock - SetupRequirement - DataArrival

```



\### Hold Slack



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

```



\---



\## 9. Installation



\### Requirements



\* Python 3.10+

\* Windows, Linux, or macOS

\* Recommended: Python virtual environment



\### Python Libraries



The project uses:



```text

streamlit

plotly

numpy

pandas

scipy

networkx

pydantic

rich

```



Install using:



```bat

pip install -r requirements.txt

```



\---



\## 10. Run Locally



\### Option 1 — One-click Windows runner



```bat

run\_playbook.bat

```



\### Option 2 — Manual terminal run



```bat

cd /d C:\\Interactive\_Soc\_Clock\_Playbook

.venv\\Scripts\\activate

streamlit run app.py

```



If the virtual environment has not been created yet:



```bat

cd /d C:\\Interactive\_Soc\_Clock\_Playbook

python -m venv .venv

.venv\\Scripts\\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

streamlit run app.py

```



\---



\## 11. Project Structure



```text

Interactive\_Soc\_Clock\_Playbook/

│

├── app.py

├── requirements.txt

├── run\_playbook.bat

├── README.md

│

├── core/

│   ├── \_\_init\_\_.py

│   ├── models.py

│   ├── clock\_math.py

│   ├── waveform\_engine.py

│   ├── soc\_path\_engine.py

│   ├── timing\_engine.py

│   ├── recommendation\_engine.py

│   └── validation\_cases.py

│

├── ui/

│   ├── \_\_init\_\_.py

│   ├── styles.py

│   ├── cards.py

│   ├── plots.py

│   ├── sidebar.py

│   └── tabs.py

│

├── docs/

│   ├── 01\_pll\_to\_flipflop\_roadmap.md

│   ├── 02\_clock\_slew\_load\_delay.md

│   ├── 03\_skew\_jitter\_uncertainty.md

│   ├── 04\_setup\_hold\_margin.md

│   ├── 05\_clock\_power\_emir\_awareness.md

│   └── demo\_script.md

│

├── examples/

│   └── ai\_soc\_5ghz\_baseline.json

│

├── screenshots/

│   ├── overview.png

│   ├── soc\_journey\_map.png

│   ├── waveform\_lab.png

│   ├── live\_math.png

│   ├── jitter\_skew\_budget.png

│   ├── ir\_drop\_crosstalk.png

│   ├── timing\_closure.png

│   └── recommendations.png

│

└── assets/

```



\---



\## 12. Internal Validation



The project includes internal validation cases.



Run:



```bat

python -m core.validation\_cases

```



The validation checks:



\* Baseline 5 GHz core math

\* Long-wire RC stress

\* Repeater tradeoff

\* IR-drop and crosstalk stress

\* Baseline setup/hold timing

\* Setup violation and useful-skew recovery

\* Hold violation case

\* Waveform vector sanity

\* Recommendation engine smoke test



Expected result:



```text

All validation cases passed: 9/9

```



This confirms internal model consistency.



\---



\## 13. Technical Scope and Limitations



This project is an architecture-level educational and sensitivity-analysis playbook.



It is not a replacement for production signoff tools.



Final silicon signoff still requires:



```text

SPEF extraction

Liberty timing models

STA

SI analysis

EMIR analysis

PVT corners

OCV / AOCV / POCV

CTS implementation data

Real floorplan and placement data

```



The current models are intentionally transparent and explainable. They are useful for:



\* Learning

\* Early architecture review

\* Sensitivity analysis

\* Demo explanation

\* System-level discussion



They are not intended to claim foundry-accurate signoff numbers.



\---



\## 14. Why This Is Useful Beyond a Spreadsheet



Spreadsheets are useful for tabular budgeting.



However, clock distribution is a multi-domain problem:



```text

Waveform shape

RC delay

Slew degradation

Jitter accumulation

Skew movement

IR-drop sensitivity

Crosstalk shift

Setup/hold closure

Architecture mitigation

```



This playbook complements spreadsheet-based analysis by connecting:



```text

Slider input

&#x20;   ↓

Formula

&#x20;   ↓

Calculated value

&#x20;   ↓

Waveform behavior

&#x20;   ↓

SoC map

&#x20;   ↓

Budget table

&#x20;   ↓

Timing diagram

&#x20;   ↓

Architecture recommendation

```



This makes the clock-distribution problem easier to communicate across architecture, timing, CTS, SI, EMIR, and design teams.



\---



\## 15. Future Roadmap



Planned future extensions:



\* Import real SPEF parasitics.

\* Import Liberty timing tables.

\* Import STA timing reports.

\* Import EMIR droop maps.

\* Add DEF/floorplan-based clock path coordinates.

\* Add real clock-tree graph visualization.

\* Add frequency sweep and margin sweep.

\* Add PVT corner comparison.

\* Add CSV export for budgets and recommendations.

\* Add SerDes / HBM clocking case studies.

\* Add optimization mode for repeater count, wire length, and skew strategy.



\---



\## 16. Final Takeaway



A modern SoC clock is not merely a square wave.



It is a fragile analog timing signal moving through:



```text

PLL noise

Duty-cycle distortion

RC interconnect

Clock buffers

Dynamic IR-drop

Crosstalk aggressors

Spatial skew

Useful skew

Setup/hold timing windows

```



This playbook makes that journey visible, measurable, and explainable.



It helps users understand not only what is failing, but why it is failing and which architecture knob can improve it.



