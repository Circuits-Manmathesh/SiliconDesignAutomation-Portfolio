# Final CTLE Design Summary

Project: demo_ctle_nrz_2gbps
Topology: NMOS differential pair CTLE with LUT-selected PMOS active loads
VDD: 1.0 V
Data rate: 2000000000.0 bps
Nyquist: 1000000000.0 Hz
UI: 5e-10 s
PMOS active load valid: 1.0
RD resistor load used: false

## Key Metrics
- Channel loss @ Nyquist: 11.255471881944324 dB
- CTLE LF gain: 2.622415937809413 dB
- CTLE peaking: 7.450108476938258 dB
- CTLE peak frequency: 1496235656.0944567 Hz
- Cascade residual loss @ Nyquist: 3.9252683781526656 dB
- Eye height before/after: 0.018697082996368408 / 0.05981588363647461 V
- Eye width before/after: 0.18 / 1.0 UI
- Total power: 3.559113611117937e-05 W

## Devices
- M_NINP nmos: W=1e-06 L=1.5000000000000002e-07 m=1.0 gm/Id=9.720670391061452 gm/gds=28.903654485049834 ft=5710408535.255012 region=saturation sat_margin=0.333 LUT_row=9150
- M_NINN nmos: W=1e-06 L=1.5000000000000002e-07 m=1.0 gm/Id=9.720670391061452 gm/gds=28.903654485049834 ft=5710408535.255012 region=saturation sat_margin=0.333 LUT_row=9150
- M_PLOADP pmos: W=6.677707400243209e-07 L=7.500000000000001e-08 m=1.0 gm/Id=6.853932584269663 gm/gds=20.06578947368421 ft=8981964397.355549 region=saturation sat_margin=0.23500000000000001 LUT_row=4173
- M_PLOADN pmos: W=6.677707400243209e-07 L=7.500000000000001e-08 m=1.0 gm/Id=6.853932584269663 gm/gds=20.06578947368421 ft=8981964397.355549 region=saturation sat_margin=0.23500000000000001 LUT_row=4173

## Plots
- 01_channel_only_loss_response.png
- 02_channel_only_eye_diagram.png
- 03_ctle_only_gain_peaking_response.png
- 04_channel_ctle_cascade_response.png
- 05_gain_phase_group_delay_diagnostic.png
- 06_prbs_input_channel_ctle_waveform.png
- 06a_prbs_input_channel_response.png
- 06b_prbs_input_channel_ctle_response.png
- 07_eye_before_after_comparison.png
- 08_eye_after_ctle.png
- 09_output_headroom_summary.png
- 10_device_operating_point_gmid_summary.png
- 11_rs_cs_zero_pole_tuning_summary.png
- 12_power_current_summary.png
- 13_spec_status_summary.png
