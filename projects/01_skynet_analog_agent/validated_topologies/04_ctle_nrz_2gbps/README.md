# CTLE Equalizer 2 Gb/s

## Validated CTLE Equalizer Demo — 2 Gb/s NRZ Receiver Front-End

This project demonstrates a physics-aware, gm/Id LUT-driven CTLE equalizer design flow for a 2 Gb/s NRZ serial-link front-end using a 1.0 V supply.

The goal is to show how the automation engine moves from a user-level high-speed link requirement to a validated analog circuit result:

```text
2 Gb/s NRZ requirement
-> 1 GHz Nyquist target
-> lossy channel fixture
-> CTLE knowledge pack
-> gm/Id LUT-aware NMOS/PMOS device selection
-> PMOS active-load CTLE netlist generation
-> SPICE operating-point / AC / transient validation
-> PRBS waveform and eye-diagram extraction
-> headroom, power, saturation, and truth-gate checks
-> final reusable evidence package
```

### Design Intent

The CTLE is designed as an NMOS differential-pair equalizer with PMOS active loads.
The public demo does not use confidential PDKs, proprietary design files, client data, or commercial IP. It is a sanitized methodology demonstration using open educational model infrastructure and local automation scripts.

### Key Validated Results

* Data rate: **2 Gb/s**
* UI: **500 ps**
* Nyquist frequency: **1 GHz**
* Supply voltage: **1.0 V**
* Channel loss at Nyquist: **11.25 dB**
* CTLE low-frequency gain: **2.62 dB**
* CTLE gain at Nyquist: **9.92 dB**
* CTLE peak gain: **10.07 dB**
* CTLE peaking: **7.45 dB**
* CTLE peak frequency: **1.49 GHz**
* Residual cascade loss at Nyquist: **3.93 dB**
* Cascade improvement at Nyquist: **7.33 dB**
* Eye height before CTLE: **18.7 mV**
* Eye height after CTLE: **59.8 mV**
* Eye-height improvement: **3.2×**
* Eye width before CTLE: **0.18 UI**
* Eye width after CTLE: **1.0 UI**
* Output common-mode: **0.55 V**
* Total power: **35.6 µW**
* All NMOS and PMOS devices are validated in saturation through operating-point checks.

### Evidence Plots

#### Channel-only loss response

![Channel-only loss response](projects/05_ctle_nrz_2gbps/plots/01_channel_only_loss_response.png)

#### Channel-only eye diagram

![Channel-only eye diagram](projects/05_ctle_nrz_2gbps/plots/02_channel_only_eye_diagram.png)

#### CTLE-only gain peaking response

![CTLE gain peaking response](projects/05_ctle_nrz_2gbps/plots/03_ctle_only_gain_peaking_response.png)

#### Channel + CTLE cascade response

![Channel CTLE cascade response](projects/05_ctle_nrz_2gbps/plots/04_channel_ctle_cascade_response.png)

#### Gain, phase, and group-delay diagnostic

![Gain phase group delay diagnostic](projects/05_ctle_nrz_2gbps/plots/05_gain_phase_group_delay_diagnostic.png)

#### PRBS input and channel response

![PRBS input and channel response](projects/05_ctle_nrz_2gbps/plots/06a_prbs_input_channel_response.png)

#### PRBS input, channel, and CTLE response

![PRBS input channel CTLE response](projects/05_ctle_nrz_2gbps/plots/06b_prbs_input_channel_ctle_response.png)

#### Eye before and after CTLE

![Eye before after CTLE](projects/05_ctle_nrz_2gbps/plots/07_eye_before_after_comparison.png)

#### Equalized eye after CTLE

![Equalized eye after CTLE](projects/05_ctle_nrz_2gbps/plots/08_eye_after_ctle.png)

#### Output headroom summary

![Output headroom summary](projects/05_ctle_nrz_2gbps/plots/09_output_headroom_summary.png)

#### Device operating-point gm/Id summary

![Device operating point gmId summary](projects/05_ctle_nrz_2gbps/plots/10_device_operating_point_gmid_summary.png)

#### RS/CS zero-pole tuning summary

![RS CS zero pole tuning summary](projects/05_ctle_nrz_2gbps/plots/11_rs_cs_zero_pole_tuning_summary.png)

#### Power and current summary

![Power current summary](projects/05_ctle_nrz_2gbps/plots/12_power_current_summary.png)

#### Spec status summary

![Spec status summary](projects/05_ctle_nrz_2gbps/plots/13_spec_status_summary.png)

### Why This Project Matters

This CTLE project extends the engine beyond low-frequency analog blocks into a high-speed serial-link receiver front-end problem. It demonstrates that the same automation philosophy can handle:

* topology-aware analog design,
* gm/Id LUT-based device selection,
* active-load verification,
* channel-loss modeling,
* peaking and zero-pole tuning,
* PRBS transient simulation,
* eye-diagram measurement,
* output common-mode and headroom validation,
* power/current checks,
* device saturation checks,
* and final plot/report generation.

The result is a reusable CTLE methodology block that can be extended later toward receiver front-end design, SerDes modeling, equalization studies, and mixed-signal link-analysis automation.
