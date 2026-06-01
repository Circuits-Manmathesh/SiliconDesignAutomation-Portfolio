\# 01 — PLL to Flip-Flop Roadmap



\## Understanding the Complete Life Journey of a SoC Clock Signal



\---



\## 1. Purpose of This Note



This note explains the complete journey of a clock signal inside a modern SoC, starting from the PLL and ending at the flip-flop capture point.



The goal is to understand one core idea:



> A SoC clock is not just a perfect digital square wave.

> It is an analog timing waveform travelling through a complex silicon environment.



During this journey, the clock interacts with:



\* PLL phase noise

\* Duty-cycle distortion

\* Divider / clock-conditioning logic

\* Global metal routing

\* Clock repeaters and buffers

\* RC interconnect delay

\* Slew degradation

\* Regional skew

\* Local IR-drop

\* Crosstalk coupling

\* Flip-flop setup and hold constraints



The \*\*Interactive SoC Clock Distribution Playbook\*\* makes this journey visible and explainable through live sliders, waveforms, node maps, formulas, timing diagrams, and architecture recommendations.



\---



\## 2. Why PLL-to-Flip-Flop Clock Roadmap Matters



In a textbook, a clock is usually drawn like this:



```text

Ideal Clock:

\_‾\_‾\_‾\_‾\_‾\_‾\_

```



But in real silicon, the clock is not ideal.



It has finite transition time, timing uncertainty, noise sensitivity, and spatial arrival differences across the chip.



A real SoC clock must travel through several physical stages before it reaches millions or billions of flip-flops.



The simplified roadmap is:



```text

PLL

&#x20;↓

Divider / Clock Conditioning

&#x20;↓

Global Clock Trunk

&#x20;↓

Regional Clock Branch

&#x20;↓

Local Clock Leaf

&#x20;↓

Flip-Flop Capture

```



Each stage changes the clock in some way.



Some stages add delay.



Some stages add jitter.



Some stages add skew.



Some stages degrade slew.



Some stages make the clock more sensitive to IR-drop or crosstalk.



The final result is judged at the flip-flop, where setup and hold timing must pass.



\---



\## 3. High-Level Roadmap Used in the Playbook



The playbook models the clock journey using six conceptual nodes:



| Node            | Role                                             |

| --------------- | ------------------------------------------------ |

| PLL             | Clock source                                     |

| Divider         | Frequency division and duty-cycle conditioning   |

| Global Trunk    | Long-distance top-metal clock transport          |

| Regional Branch | Distribution into local SoC regions              |

| Local Leaf      | Final local delivery near sequential cells       |

| Flip-Flop       | Final capture point where setup/hold are checked |



Inside the application, this journey is shown in the \*\*SoC Journey Map\*\* tab.



Each node contains live values:



```text

Accumulated Delay

Jitter RMS

Local Skew

VDD Droop

Slew

```



These are not meant to replace extracted signoff data.



They are architecture-level sensitivity indicators that help users understand how the clock quality evolves from source to endpoint.



\---



\## 4. Stage 1 — PLL: The Clock Origin



The PLL is the source of the master clock.



In a perfect world, the PLL would generate a clean clock with perfectly periodic edges.



In real silicon, the PLL output already contains imperfections.



The main effects are:



\* Random jitter

\* Phase noise

\* Duty-cycle distortion

\* Output-driver asymmetry

\* Supply sensitivity



In the playbook, the PLL/source clock is controlled by:



```text

Clock Frequency

PLL Random Jitter RMS

PLL Duty Cycle

```



\---



\### 4.1 Clock Frequency



Clock frequency determines the clock period.



The playbook uses:



```text

Tclk = 1000 / fGHz

```



For the default demo case:



```text

Clock Frequency = 5 GHz



Tclk = 1000 / 5

Tclk = 200 ps

```



This means one complete clock cycle is only 200 ps.



At this speed, even small edge movement can consume real timing margin.



For example:



```text

1 ps is 0.5% of a 200 ps cycle.

10 ps is 5% of a 200 ps cycle.

```



This is why high-frequency clock distribution requires careful treatment of jitter, skew, slew, IR-drop, and setup/hold margin.



\---



\### 4.2 PLL Random Jitter



Jitter means the clock edge does not arrive at exactly the expected time.



Ideal edge positions may be:



```text

0 ps

200 ps

400 ps

600 ps

800 ps

```



But real edge positions may become:



```text

0.08 ps

199.91 ps

400.12 ps

599.86 ps

800.05 ps

```



This edge movement is jitter.



In the playbook, this is controlled by:



```text

PLL Random Jitter RMS

```



Default value:



```text

PLL Random Jitter = 120 fs

```



This is the source-level timing uncertainty before the clock enters the distribution network.



\---



\### 4.3 Duty-Cycle Distortion



An ideal clock has 50% duty cycle:



```text

50% HIGH

50% LOW

```



But real circuits may create:



```text

51.5% HIGH

48.5% LOW

```



or:



```text

48% HIGH

52% LOW

```



This is duty-cycle distortion.



The playbook calculates duty-cycle error as:



```text

DCD = |Duty - 50%|

```



For the default case:



```text

Duty = 51.5%



DCD = |51.5 - 50|

DCD = 1.5%

```



Duty-cycle distortion matters because some clocking schemes, especially high-speed interfaces, DDR-style timing, latch-based paths, or divided clock domains, can be sensitive to high/low pulse symmetry.



\---



\### 4.4 How the Playbook Shows PLL Behavior



The playbook shows the PLL/source behavior in two ways:



1\. In the sidebar, the user controls:



&#x20;  \* Frequency

&#x20;  \* PLL jitter

&#x20;  \* Duty cycle



2\. In the Waveform Lab, the user sees:



&#x20;  \* Ideal clock

&#x20;  \* Degraded clock

&#x20;  \* Mitigated clock



When PLL jitter increases, the degraded clock edge becomes more uncertain.



When duty cycle moves away from 50%, the high/low pulse symmetry changes.



This directly connects the theory of PLL imperfection to a visible waveform.



\---



\## 5. Stage 2 — Divider / Clock Conditioning



After the PLL, the clock may pass through divider or clock-conditioning logic.



This stage can perform several roles:



\* Divide frequency

\* Improve clock symmetry

\* Generate cleaner internal phases

\* Reduce duty-cycle imbalance

\* Provide a more controlled clock before distribution



A divide-by-2 stage often helps duty-cycle correction because it can regenerate a more balanced 50% clock under suitable design conditions.



In the playbook, the divider is represented as the second node in the SoC Journey Map.



\---



\### 5.1 Why Divider Matters



The PLL output may be good, but it may not be perfect.



A clock-conditioning stage can help clean the signal before it enters the global distribution network.



This is important because any clock error at the source can propagate through the rest of the clock tree.



If source clock quality is poor, the downstream clock tree cannot fully recover it without additional conditioning.



\---



\### 5.2 Divider Tradeoff



A divider can improve duty cycle, but it is not free.



It may add:



\* Small delay

\* Residual jitter

\* Power

\* Area

\* Local supply sensitivity



Therefore, a clock architect does not simply add conditioning blindly.



The divider must be balanced against timing, power, jitter, and duty-cycle requirements.



\---



\### 5.3 Playbook Interpretation



In the SoC Journey Map, the Divider node shows that the clock has moved from raw PLL generation to early conditioning.



In the waveform view, the mitigated waveform represents the idea that the clock can become cleaner after architecture-level correction and mitigation.



The playbook does not claim transistor-level divider simulation.



It explains the architectural role of clock conditioning.



\---



\## 6. Stage 3 — Global Clock Trunk



The global clock trunk is the main long-distance route carrying the clock across the SoC.



This is where interconnect physics becomes very important.



A clock wire is not ideal.



It has:



\* Resistance

\* Capacitance

\* Coupling capacitance

\* Finite driver strength

\* Routing-dependent delay

\* Local loading



The global trunk may travel across:



\* AI compute arrays

\* SRAM regions

\* HBM PHY regions

\* SerDes blocks

\* NoC fabric

\* Control logic



In large SoCs, the global clock trunk can span thousands of microns.



\---



\### 6.1 Wire Resistance



The playbook estimates wire resistance using sheet resistance.



First, it calculates wire squares:



```text

Squares = WireLength / WireWidth

```



Then:



```text

Rwire = Rsheet × Squares

```



For the default case:



```text

Wire Length = 2400 µm

Wire Width  = 0.08 µm

Rsheet      = 28 mΩ/sq = 0.028 Ω/sq

```



So:



```text

Squares = 2400 / 0.08

Squares = 30000

```



Then:



```text

Rwire = 0.028 × 30000

Rwire = 840 Ω

```



This tells us that a long global wire can create significant resistance.



\---



\### 6.2 Wire Capacitance



The playbook estimates capacitance as:



```text

Cwire = Cper\_um × WireLength

```



For the default case:



```text

Cper\_um = 95 aF/µm

Wire Length = 2400 µm

```



So:



```text

Cwire = 95 × 2400 aF

Cwire = 228000 aF

Cwire = 228 fF

```



This capacitance is the load that the clock network must charge and discharge.



\---



\### 6.3 RC Time Constant



The basic RC severity is:



```text

τRC = Rwire × Cwire

```



For the default case:



```text

τRC = 840 Ω × 228 fF

τRC = 191.52 ps

```



This number should be interpreted carefully.



It is not the final extracted clock delay.



It is an architecture-level unbuffered RC severity indicator.



The reason is that real clock trunks are not normally driven as one long unbuffered wire.



They are segmented using repeaters or buffers.



\---



\### 6.4 Repeater Segmentation



Repeaters divide the long route into shorter effective segments.



The playbook uses:



```text

Segments = RepeaterCount + 1

τsegment = τRC / Segments²

```



For the default case:



```text

RepeaterCount = 4

Segments = 5

```



Then:



```text

τsegment = 191.52 / 25

τsegment = 7.6608 ps

```



This segment RC is more meaningful for buffered clock delivery.



It explains why repeater planning is critical in clock distribution.



\---



\### 6.5 Repeater Insertion Delay



Repeaters improve slew, but they add delay.



The playbook models insertion delay as:



```text

InsertionDelay = RepeaterCount × BufferDelay

```



Default:



```text

BufferDelay = 3.2 ps

RepeaterCount = 4

```



So:



```text

InsertionDelay = 4 × 3.2

InsertionDelay = 12.8 ps

```



This shows the tradeoff:



```text

More repeaters → better slew

More repeaters → more insertion delay and clock power

```



\---



\## 7. Stage 4 — Regional Clock Branch



After the global trunk, the clock branches into different SoC regions.



This stage is important because different regions behave differently.



Examples:



```text

Compute array

SRAM macro region

HBM PHY

SerDes block

NoC router region

Control logic island

```



Each region can have different:



\* Local loading

\* Activity profile

\* Power-grid condition

\* Routing congestion

\* Coupling environment

\* Clock-buffer depth

\* Skew behavior



The playbook represents this using the \*\*Regional Branch\*\* node.



\---



\### 7.1 Why Regional Branches Create Skew



The same source clock may reach different regions at different times.



This happens due to:



\* Unequal path lengths

\* Different buffer counts

\* Different local loads

\* Different IR-drop conditions

\* Different routing layers

\* Different congestion

\* Different physical placement



This difference in clock arrival time is called skew.



\---



\### 7.2 Regional Branch in the Playbook



In the SoC Journey Map, the Regional Branch node shows:



```text

Accumulated delay

Jitter RMS

Local skew

VDD droop

Slew

```



The goal is to show that clock quality does not remain constant after the global trunk.



It changes depending on the region.



This is especially important in AI SoCs, where compute-heavy regions may create stronger local switching activity and power droop.



\---



\## 8. Stage 5 — Local Clock Leaf



The local leaf is the final local delivery network near sequential cells.



This stage is close to flip-flops and local logic.



It may include:



\* Local clock buffers

\* Clock gates

\* Short local routes

\* Local clock branches

\* Leaf-level loading

\* Local decaps

\* Local IR-drop exposure



This stage is very sensitive because it is close to active switching logic.



\---



\### 8.1 Local IR-Drop Sensitivity



When nearby logic switches heavily, local current demand increases.



This can cause local VDD droop.



Clock buffers operating under lower VDD become slower.



That means the clock edge can shift later.



This effect is called:



```text

Power Supply Induced Jitter

```



or:



```text

PSIJ

```



The playbook models it as:



```text

ΔtPSIJ = kdroop × Vdroop

```



For the default case:



```text

Vdroop = 45 mV

kdroop = 0.0048 ps/mV

```



So:



```text

ΔtPSIJ = 0.0048 × 45

ΔtPSIJ = 0.216 ps

```



This shows how power integrity becomes timing integrity.



\---



\### 8.2 Local Leaf in the Playbook



The Local Leaf node shows stronger sensitivity to:



\* VDD droop

\* Local skew

\* Final slew

\* Endpoint jitter



This helps users understand that even if the global trunk looks acceptable, the final local clock delivery may still become risky.



\---



\## 9. Stage 6 — Flip-Flop Capture



The flip-flop is the final destination.



At this point, the clock must capture data correctly.



The full clock journey finally reduces to two key timing questions:



```text

Did data arrive early enough before the capture edge?

Did data remain stable long enough after the clock reference?

```



These are setup and hold checks.



\---



\### 9.1 Setup Slack



Setup slack is calculated as:



```text

SetupSlack = CaptureClock - SetupRequirement - DataArrival

```



For the default case:



```text

Clock Period = 200 ps

Spatial Skew = 8 ps

Useful Skew = 0 ps

Data Arrival = 175 ps

Setup Requirement = 8 ps

```



First:



```text

CaptureClock = Period + SpatialSkew + UsefulSkew

CaptureClock = 200 + 8 + 0

CaptureClock = 208 ps

```



Then:



```text

SetupSlack = 208 - 8 - 175

SetupSlack = 25 ps

```



Positive setup slack means setup passes.



\---



\### 9.2 Hold Slack



Hold slack is calculated as:



```text

HoldSlack = DataArrival - (EffectiveSkew + HoldRequirement)

```



For the default case:



```text

EffectiveSkew = 8 ps

HoldRequirement = 5 ps

DataArrival = 175 ps

```



Then:



```text

HoldSlack = 175 - (8 + 5)

HoldSlack = 162 ps

```



Positive hold slack means hold passes.



\---



\### 9.3 Useful Skew Tradeoff



Useful skew means intentionally shifting the capture clock.



Positive useful skew can help setup because it delays the capture edge.



However, it can hurt hold because short paths may change too early relative to the delayed capture relationship.



The playbook demonstrates this with sliders:



```text

Increase Useful Skew

&#x20;   → Setup Slack improves

&#x20;   → Hold Slack may reduce

```



This is one of the most important timing-closure lessons.



\---



\## 10. How the Playbook Connects Theory to Interaction



The playbook maps theory into interaction as follows:



| Theory Concept        | Playbook Control / View                         |

| --------------------- | ----------------------------------------------- |

| Clock frequency       | Frequency slider and clock-period metric        |

| PLL jitter            | PLL jitter slider and jitter budget             |

| Duty-cycle distortion | Duty-cycle slider and waveform symmetry         |

| Wire RC               | Wire length, resistance, capacitance sliders    |

| Repeater tradeoff     | Repeater slider, segment RC and insertion delay |

| Slew degradation      | Waveform Lab and slew metrics                   |

| IR-drop               | VDD droop slider and heatmap                    |

| Crosstalk             | Aggressor alignment selector                    |

| Skew                  | Spatial skew and useful skew sliders            |

| Setup/Hold timing     | Timing Closure tab                              |

| Architecture actions  | Recommendations tab                             |



The important idea is that all these effects are connected.



Changing one architecture knob updates the waveform, math, map, budget, timing, and recommendations together.



\---



\## 11. Default 5 GHz Roadmap Summary



Default playbook condition:



```text

Clock Frequency       = 5.0 GHz

PLL Random Jitter     = 120 fs

PLL Duty Cycle        = 51.5 %



Global Wire Length    = 2400 µm

Top Metal Sheet R     = 28 mΩ/sq

Wire Capacitance      = 95 aF/µm

Repeater Count        = 4



Dynamic VDD Droop     = 45 mV

Crosstalk Mode        = Quiet / Orthogonal

Shielding + Decaps    = ON



Logic Path Delay      = 175 ps

Spatial Clock Skew    = 8 ps

Useful Skew           = 0 ps

Setup Requirement     = 8 ps

Hold Requirement      = 5 ps

```



Calculated reference values:



```text

Clock Period       = 200.000 ps

Wire Resistance    = 840.000 Ω

Wire Capacitance   = 228.000 fF

Total RC Tau       = 191.520 ps

Segment RC Tau     = 7.661 ps

Insertion Delay    = 12.800 ps

Setup Slack        = 25.000 ps

Hold Slack         = 162.000 ps

```



This creates a controlled baseline for learning and demonstration.



\---



\## 12. Engineering Interpretation



A mature clock-distribution review should not only ask:



```text

Is the clock connected?

```



It should ask:



```text

Is the clock source clean enough?

Is duty-cycle distortion controlled?

Is the global trunk properly segmented?

Is slew acceptable?

Is clock uncertainty budgeted?

Is skew intentional and controlled?

Is local IR-drop affecting clock buffers?

Is crosstalk shifting the edge?

Are setup and hold both safe?

Is there a clear mitigation path?

```



The playbook helps answer these questions interactively.



\---



\## 13. What This Roadmap Does Not Claim



This roadmap is not a production signoff flow.



It does not replace:



```text

SPEF extraction

Liberty timing

STA

SI analysis

EMIR analysis

CTS implementation data

PVT and OCV correlation

```



The current model is an architecture-level educational and sensitivity-analysis model.



Its purpose is:



```text

Learning

Early architecture review

Failure-mode understanding

Communication between teams

Interactive demonstration

```



Final silicon readiness still requires full signoff correlation.



\---



\## 14. Final Takeaway



The PLL-to-flip-flop clock path is a complete physical journey.



A clock starts as a source waveform, but by the time it reaches a flip-flop, it has interacted with:



```text

PLL noise

Duty-cycle distortion

Divider conditioning

RC interconnect

Clock repeaters

Regional skew

Local IR-drop

Crosstalk

Setup/hold timing windows

```



The Interactive SoC Clock Distribution Playbook makes this journey visible, measurable, and explainable.



It helps users understand not only what happens to the clock, but why it happens and which architecture knobs can improve it.



