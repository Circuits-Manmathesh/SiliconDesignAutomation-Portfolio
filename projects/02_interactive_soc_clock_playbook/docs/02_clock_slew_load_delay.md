\# 02 — Clock Slew, Load and Delay



\## Understanding Why a Clock Edge Becomes Slow Inside a SoC



\---



\## 1. Purpose of This Note



This note explains three very important clock-distribution concepts:



```text

Clock Slew

Clock Load

Clock Delay

```



These three concepts are strongly connected.



In a real SoC, the clock does not travel like a perfect square wave. When the clock leaves the PLL and moves through long metal wires, buffers, repeaters, and local branches, its edge can become slower, shifted, and more sensitive to noise.



The \*\*Interactive SoC Clock Distribution Playbook\*\* makes this visible by showing:



```text

Ideal Clock

Degraded Clock

Mitigated Clock

```



The goal of this note is to explain why the degraded clock waveform becomes slow and how the playbook calculates that effect using simple, transparent formulas.



\---



\## 2. Layman Explanation — What Is Clock Slew?



Imagine switching on a light.



In an ideal world:



```text

OFF → immediately ON

```



But in the real world, the transition may take a tiny amount of time.



Similarly, a clock signal does not jump from 0 V to VDD instantly.



It rises gradually:



```text

Slow edge:

0 V  / / / / /  VDD

```



A faster edge looks sharper:



```text

Fast edge:

0 V | VDD

```



This transition speed is called \*\*slew\*\*.



In simple words:



> Clock slew tells us how fast the clock edge rises or falls.



A good clock edge is sharp enough to be interpreted clearly by flip-flops and clock buffers.



A poor clock edge is slow and rounded.



\---



\## 3. Why Clock Slew Matters



Clock slew is important because the clock edge is the timing reference for the whole chip.



If the edge is slow:



\* The exact switching moment becomes less clear.

\* Flip-flop sampling becomes more sensitive.

\* Clock buffer delay can vary more.

\* Noise can move the apparent edge position.

\* Setup and hold timing margins can reduce.

\* Short-circuit current inside receiving gates can increase.



For a low-speed design, a small slew issue may not be critical.



But at multi-GHz operation, timing windows are very small.



For example, in our default playbook case:



```text

Clock Frequency = 5 GHz

Clock Period    = 200 ps

```



So even a few picoseconds of clock-edge degradation can matter.



\---



\## 4. What Is Clock Load?



Clock load is the electrical burden that the clock driver must drive.



A clock route must charge and discharge:



```text

Wire capacitance

Input capacitance of buffers

Input capacitance of clock gates

Flip-flop clock pin capacitance

Coupling capacitance from nearby wires

```



A simple analogy:



> Driving a small load is like pushing a light bicycle.

> Driving a large load is like pushing a heavy truck.



The heavier the load, the harder it is for the clock driver to switch quickly.



In electrical terms, more load usually means more capacitance.



More capacitance means the clock edge becomes slower unless the driver or repeater strategy is improved.



\---



\## 5. Why Long Wires Create Delay and Slow Slew



A long metal wire inside a chip is not ideal.



It has:



```text

Resistance

Capacitance

Coupling to nearby wires

```



For this playbook, we use a clean architecture-level RC model:



```text

R = resistance

C = capacitance

RC = delay/slew severity indicator

```



The longer the wire:



```text

Resistance increases

Capacitance increases

RC severity increases

Clock edge becomes slower

```



This is why global clock distribution is difficult in large SoCs.



The clock must travel far, but it must still remain sharp and well-timed.



\---



\## 6. Wire Resistance Model Used in the Playbook



The playbook calculates wire resistance using sheet resistance.



First, it calculates the number of wire squares:



```text

Squares = Wire Length / Wire Width

```



Then:



```text

Rwire = Rsheet × Squares

```



Where:



```text

Wire Length = length of the clock route

Wire Width  = effective top-metal clock wire width

Rsheet      = sheet resistance of the routing layer

```



\---



\## 7. Default Example — Wire Resistance Calculation



In our default 5 GHz AI SoC example:



```text

Global Wire Length = 2400 µm

Wire Width         = 0.08 µm

Sheet Resistance   = 28 mΩ/sq

```



Convert sheet resistance:



```text

28 mΩ/sq = 0.028 Ω/sq

```



Calculate wire squares:



```text

Squares = 2400 / 0.08

Squares = 30000

```



Now calculate wire resistance:



```text

Rwire = 0.028 × 30000

Rwire = 840 Ω

```



So the playbook shows:



```text

Wire Resistance = 840 Ω

```



This tells us that the long clock route has significant resistance.



\---



\## 8. Wire Capacitance Model Used in the Playbook



Wire capacitance is calculated as:



```text

Cwire = Cper\_um × Wire Length

```



Where:



```text

Cper\_um = capacitance per micron

```



In our default example:



```text

Wire Capacitance = 95 aF/µm

Wire Length      = 2400 µm

```



Calculate:



```text

Cwire = 95 × 2400 aF

Cwire = 228000 aF

```



Convert attofarad to femtofarad:



```text

1000 aF = 1 fF

```



So:



```text

Cwire = 228 fF

```



The playbook shows:



```text

Wire Capacitance = 228 fF

```



This is the load that the clock network must charge and discharge.



\---



\## 9. RC Time Constant



The basic RC severity indicator is:



```text

τRC = Rwire × Cwire

```



For our default example:



```text

Rwire = 840 Ω

Cwire = 228 fF

```



So:



```text

τRC = 840 × 228 fF

τRC = 191.52 ps

```



The playbook shows:



```text

Total RC Tau = 191.52 ps

```



Important interpretation:



> This is not claiming that the final clock delay is exactly 191.52 ps.



It is an architecture-level indicator showing how severe the long unbuffered route would be.



In real clock distribution, we do not usually drive a very long global trunk as one unbuffered wire. We insert repeaters or buffers.



\---



\## 10. Why Repeaters Are Needed



A repeater is a clock buffer inserted along the wire.



Its job is to regenerate the signal.



Without repeaters:



```text

Long wire

Large RC

Slow edge

Poor slew

More timing uncertainty

```



With repeaters:



```text

Long wire split into smaller segments

Each segment has smaller effective RC

Clock edge is restored periodically

Slew improves

```



Layman analogy:



> Imagine shouting a message across a very long distance.

> If one person shouts from one end to the other, the message becomes weak.

> If several people repeat the message along the way, the message remains stronger and clearer.



Repeaters do the same thing for the clock edge.



\---



\## 11. Repeater Segmentation Formula



The playbook uses:



```text

Segments = RepeaterCount + 1

```



Then:



```text

τsegment = τRC / Segments²

```



This means that as the route is divided into more segments, the effective RC per segment reduces strongly.



For the default case:



```text

Repeater Count = 4

Segments       = 4 + 1 = 5

```



Now:



```text

τsegment = 191.52 / 5²

τsegment = 191.52 / 25

τsegment = 7.6608 ps

```



The playbook shows:



```text

RC Segment Tau = 7.661 ps

```



This segment value is more practical for understanding buffered clock delivery.



\---



\## 12. Repeater Insertion Delay



Repeaters improve slew, but they are not free.



Every repeater adds some delay.



The playbook uses:



```text

Insertion Delay = RepeaterCount × BufferDelay

```



Default case:



```text

Repeater Count = 4

Buffer Delay   = 3.2 ps

```



So:



```text

Insertion Delay = 4 × 3.2

Insertion Delay = 12.8 ps

```



This shows the key clock-tree tradeoff:



```text

More repeaters → better slew

More repeaters → more insertion delay

More repeaters → more clock power

```



This is why clock-tree synthesis is an optimization problem, not just a routing task.



\---



\## 13. Slew Model Used in the Playbook



The playbook uses a simple explainable slew model:



```text

Slewbefore = BaseSlew + k × τsegment

```



Where:



```text

BaseSlew = minimum idealized local edge slew

k        = sensitivity factor

τsegment = effective segment RC

```



Default values:



```text

BaseSlew = 0.8 ps

k        = 2.4

τsegment = 7.6608 ps

```



So:



```text

Slewbefore = 0.8 + 2.4 × 7.6608

Slewbefore = 0.8 + 18.38592

Slewbefore = 19.18592 ps

```



The playbook shows:



```text

Before Slew = 19.186 ps

```



This is the degraded clock edge slew before mitigation.



\---



\## 14. Mitigated Slew



The playbook also shows a mitigated clock waveform.



Mitigation may represent:



```text

Better repeater strategy

Shielding

Decaps

Clock conditioning

Reduced noise sensitivity

Improved local delivery

```



The playbook uses:



```text

Slewafter = max(BaseSlew, Slewbefore × MitigationFactor)

```



For the default case:



```text

Slewbefore        = 19.18592 ps

MitigationFactor  = 0.35

BaseSlew          = 0.8 ps

```



So:



```text

Slewafter = max(0.8, 19.18592 × 0.35)

Slewafter = max(0.8, 6.715072)

Slewafter = 6.715072 ps

```



The playbook shows:



```text

After Slew = 6.715 ps

```



This means the mitigated clock edge is much sharper than the degraded clock edge.



\---



\## 15. What the Waveform Lab Shows



In the \*\*Waveform Lab\*\* tab, the playbook shows three waveforms:



```text

Ideal Clock

Degraded Clock

Mitigated Clock

```



\### Ideal Clock



The ideal clock has:



```text

50% duty cycle

No jitter

Sharp edge

No edge shift

```



It is the reference.



\### Degraded Clock



The degraded clock includes:



```text

PLL duty-cycle distortion

PLL random jitter

RC slew degradation

Repeater insertion delay

IR-drop edge shift

Crosstalk edge shift

```



It appears slower and shifted.



\### Mitigated Clock



The mitigated clock shows improvement after architecture-level cleanup:



```text

Lower endpoint uncertainty

Better slew

Reduced noise-induced edge movement

Partially corrected duty behavior

```



This is where the user can visually understand why clock-distribution architecture matters.



\---



\## 16. Interactive Experiment 1 — Increase Wire Length



In the playbook sidebar, increase:



```text

Global Wire Length = 3500 µm

```



Keep:



```text

Repeater Count = 4

```



Now observe:



```text

Wire resistance increases

Wire capacitance increases

Total RC tau increases

Segment RC tau increases

Before slew becomes worse

Waveform edge becomes slower

```



Calculation:



```text

Squares = 3500 / 0.08

Squares = 43750

```



```text

Rwire = 0.028 × 43750

Rwire = 1225 Ω

```



```text

Cwire = 95 × 3500 aF

Cwire = 332500 aF

Cwire = 332.5 fF

```



```text

τRC = 1225 × 332.5 fF

τRC = 407.3125 ps

```



With 4 repeaters:



```text

Segments = 5

τsegment = 407.3125 / 25

τsegment = 16.2925 ps

```



Slew:



```text

Slewbefore = 0.8 + 2.4 × 16.2925

Slewbefore = 39.902 ps

```



Interpretation:



> The longer trunk makes the clock edge slower because RC severity increases.



\---



\## 17. Interactive Experiment 2 — Change Repeater Count



Now keep:



```text

Global Wire Length = 3500 µm

```



First try:



```text

Repeater Count = 2

```



Then:



```text

Segments = 3

τsegment = 407.3125 / 9

τsegment ≈ 45.257 ps

```



Slew:



```text

Slewbefore = 0.8 + 2.4 × 45.257

Slewbefore ≈ 109.417 ps

```



This is very slow.



Now increase:



```text

Repeater Count = 8

```



Then:



```text

Segments = 9

τsegment = 407.3125 / 81

τsegment ≈ 5.029 ps

```



Slew:



```text

Slewbefore = 0.8 + 2.4 × 5.029

Slewbefore ≈ 12.869 ps

```



This is much better.



But insertion delay increases:



```text

InsertionDelay = 8 × 3.2

InsertionDelay = 25.6 ps

```



Interpretation:



> More repeaters improved slew, but also increased insertion delay.



This is exactly the clock-distribution tradeoff the playbook is designed to demonstrate.



\---



\## 18. Why Too Few Repeaters Are Bad



If repeaters are too few:



```text

Each wire segment is too long

Segment RC becomes large

Clock edge becomes slow

Clock uncertainty increases

Downstream timing becomes more sensitive

```



The waveform looks rounded and delayed.



This can hurt setup timing because the effective edge is less sharp and more uncertain.



\---



\## 19. Why Too Many Repeaters Are Also Not Always Good



If repeaters are too many:



```text

Slew improves

But insertion delay increases

Clock power increases

Area increases

More buffers can create more mismatch

EMIR stress can increase

```



So the best repeater count is not simply the highest value.



The goal is to balance:



```text

Slew

Insertion delay

Power

Skew

Jitter

EMIR

Area

```



This is why clock-tree planning is an architecture decision.



\---



\## 20. How Load Affects Power



Clock dynamic power is related to capacitance:



```text

Pdynamic ≈ C × V² × f

```



This is not directly plotted as signoff power in the current playbook, but the concept is important.



If wire capacitance increases:



```text

More charge/discharge every cycle

More dynamic clock power

More current demand

More possible IR-drop

More timing sensitivity

```



This connects clock load to EMIR awareness.



Clock distribution is not only a delay problem.



It is also a power and reliability problem.



\---



\## 21. Practical Interpretation for a SoC Designer



A SoC designer or timing engineer should ask:



```text

Is the global trunk too long?

Is the wire layer strong enough?

Is the effective segment RC acceptable?

Is the repeater count too low?

Is the repeater count too high?

Is slew controlled at the endpoint?

Is insertion delay still acceptable?

Is the clock power reasonable?

Is the route exposed to droop or crosstalk?

```



The playbook helps answer these questions interactively.



\---



\## 22. Mapping This Note to the Playbook



| Theory Topic        | Playbook Location                    |

| ------------------- | ------------------------------------ |

| Wire length         | Sidebar → Global Wire Length         |

| Sheet resistance    | Sidebar → Top Metal Sheet Resistance |

| Wire capacitance    | Sidebar → Wire Capacitance           |

| Repeater count      | Sidebar → Repeater / Buffer Count    |

| Wire resistance     | Live Math tab                        |

| Wire capacitance    | Live Math tab                        |

| Total RC tau        | Live Math tab                        |

| Segment RC tau      | Top metric strip and Live Math tab   |

| Slew degradation    | Waveform Lab                         |

| Insertion delay     | Live Math tab                        |

| Architecture action | Recommendations tab                  |



The key benefit is that the user does not only read the formula.



The user can move the slider and see the formula, waveform, timing, and recommendation update together.



\---



\## 23. Default Example Summary



Default values:



```text

Clock Frequency    = 5 GHz

Wire Length        = 2400 µm

Wire Width         = 0.08 µm

Sheet Resistance   = 28 mΩ/sq

Wire Capacitance   = 95 aF/µm

Repeater Count     = 4

```



Calculated values:



```text

Wire Squares       = 30000

Wire Resistance    = 840 Ω

Wire Capacitance   = 228 fF

Total RC Tau       = 191.52 ps

Segment RC Tau     = 7.6608 ps

Insertion Delay    = 12.8 ps

Before Slew        = 19.18592 ps

After Slew         = 6.715072 ps

```



Engineering reading:



```text

The long wire has meaningful RC severity.

Repeater segmentation reduces effective segment RC.

Mitigation improves the final edge quality.

The clock still needs timing, jitter, skew, IR-drop, and crosstalk review.

```



\---



\## 24. What This Model Does Not Claim



The playbook does not claim transistor-level or foundry-signoff accuracy.



It does not replace:



```text

SPICE simulation

Extracted SPEF timing

Liberty-based STA

CTS reports

SI analysis

EMIR analysis

PVT/OCV signoff

```



The model is intentionally simple and transparent.



Its purpose is to explain:



```text

Why long wires hurt clock edges

Why repeaters help

Why repeaters also add delay

Why slew matters

Why load affects power and timing

How architecture knobs influence waveform behavior

```



\---



\## 25. Final Takeaway



Clock slew, load, and delay are connected.



A long wire creates resistance and capacitance.



Resistance and capacitance create RC severity.



RC severity slows the clock edge.



Repeaters reduce effective segment RC and improve slew.



But repeaters add insertion delay and power.



Therefore, clock distribution is a tradeoff between:



```text

Fast edge

Low delay

Low power

Low skew

Low jitter

Good timing margin

Reliable EMIR behavior

```



The Interactive SoC Clock Distribution Playbook makes this tradeoff visible through formulas, waveforms, node maps, timing diagrams, and recommendations.



