# Final Design Report

Project: demo_two_stage_opamp
Topology: two_stage_opamp
Status: PASS
Model library: C:\Skynet_Setup\skynet_analog_agent\technology_models\models.lib
LUT root: C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut

## Reproducible Device Bias and Sizing Summary
- VDD: None
- VIN_CM: None
- VBP: None
- CL: None
- M_NINP: W=1e-06 L=3.0000000000000004e-07 m=1.0 ID=9.98e-07 gm/Id=18.7374749498998 region=saturation VGS=0.296 VDS=0.385 LUT_row=14352
- M_NINN: W=1e-06 L=3.0000000000000004e-07 m=1.0 ID=None gm/Id=14.000068199568279 region=weak VGS=0.2962702065706253 VDS=None LUT_row=14352
- M_PLOAD_DIODE: W=3.2053326901083183e-07 L=4.2e-07 m=1 ID=None gm/Id=9.083107857176895 region=strong VGS=None VDS=None LUT_row=16540
- M_PLOAD_MIRROR: W=3.2053326901083183e-07 L=4.2e-07 m=1 ID=None gm/Id=9.083107857176895 region=strong VGS=None VDS=None LUT_row=16540
- M_NCS2: W=1.6812448747524575e-06 L=4.2e-07 m=1 ID=None gm/Id=10.991306723726774 region=moderate VGS=None VDS=None LUT_row=16594
- M_PLOAD2: W=3.2053326901083184e-06 L=4.2e-07 m=1 ID=None gm/Id=9.083107857176895 region=strong VGS=None VDS=None LUT_row=16540

## Final Device Sizing
- M_NINP: W=1e-06 L=3.0000000000000004e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\nmos_50nm_nominal_27C_full.npz
- M_NINN: W=1e-06 L=3.0000000000000004e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\nmos_50nm_nominal_27C_full.npz
- M_PLOAD_DIODE: W=3.2053326901083183e-07 L=4.2e-07 m=1 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\pmos_50nm_nominal_27C_full.npz
- M_PLOAD_MIRROR: W=3.2053326901083183e-07 L=4.2e-07 m=1 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\pmos_50nm_nominal_27C_full.npz
- M_NCS2: W=1.6812448747524575e-06 L=4.2e-07 m=1 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\nmos_50nm_nominal_27C_full.npz
- M_PLOAD2: W=3.2053326901083184e-06 L=4.2e-07 m=1 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\pmos_50nm_nominal_27C_full.npz

## Measurements
- output_bias_v: 0.5537757277488708
- bias_current_a: 4.714154056273401e-05
- average_power_w: 4.714154056273401e-05
- dc_gain_vv: -178.7769118435954
- dc_gain_db: 45.04622862181894
- output_swing_low_v: 0.14587348699569702
- output_swing_high_v: 0.9914889335632324
- ac_midband_gain_db: 46.204745457616625
- bandwidth_hz: 79653.00366876957
- ugb_hz: 15626228.529554041
- phase_at_ugb_deg: -115.24691072056092
- phase_margin_deg: 64.75308927943908
- slew_rate_v_per_s: 15962712.366085947
- settling_time_1pct_s: 1.895270000000274e-07

## Reproducibility
Use the listed project-local netlists with the model library path above. Copy final W/L/m, VIN_CM, VBP, VDD and CL from this report.
