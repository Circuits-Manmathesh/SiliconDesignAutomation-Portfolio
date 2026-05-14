# Inverter Demo Walkthrough

The `inverter_3GHz_clock_TT27` example demonstrates a representative 50 nm CMOS inverter clock-buffer unit cell operating from a 1.0 V supply at TT / 27 C.

## Spec

The public spec targets a 3 GHz clock path with a 20 fF load. The input duty cycle is stressed at 45%, 50%, and 55%. Timing, rise/fall time, output swing, and duty-cycle distortion are checked.

## Selected Sizing

The public portfolio does not disclose private sizing internals. The private framework selects a candidate through gm/Id-guided operating-region filtering, speed screening, load estimation, and SPICE verification.

## DC VTC

The DC voltage-transfer curve verifies inverter switching behavior, output swing, static current, static power, and gain around the transition region.

## AC Gain And Phase

AC plots provide small-signal gain, phase, bandwidth, and loading evidence. They show whether the selected device operating point supports the required high-speed clock-buffer behavior.

## Transient Delay And Duty

Transient marker plots verify tpHL, tpLH, rise/fall time, output duty cycle, and timing behavior under duty-cycle stress.

## Why The Design Passes

The selected design passed all 45%, 50%, and 55% input duty-cycle stress cases. Representative public results show tpHL approximately 16.1 ps, tpLH approximately 16.4 ps, rise/fall approximately 10.6 ps / 11.9 ps, and average power approximately 0.478 mW. Output duty cycle remained inside the required 45% to 55% band.

## What The Plots Show

- DC plots show transfer behavior, gain, static current, static power, and gm/Id trend.
- AC plots show gain/phase response, bias sensitivity, bandwidth, and input capacitance.
- Transient plots show waveform timing, delay markers, delay-power tradeoff, and duty-cycle checks.
- Final dashboards collect the project-level result for review.

