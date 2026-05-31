# Final Design Report

Project: demo_differential_pair
Topology: differential_pair
Status: PASS
Model library: C:\Skynet_Setup\skynet_analog_agent\technology_models\models.lib
LUT root: C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut

## Reproducible Device Bias and Sizing Summary
- VDD: 1
- VIN_CM: 0.36
- VBP: 0.58
- ITAIL: 8.97597901026e-06
- CL: 0.2p
- M_NINP: W=1e-06 L=1.8000000000000002e-07 m=1.0 ID=4.49e-06 gm/Id=15.701559020044543 region=saturation VGS=0.336 VDS=0.473 LUT_row=10266
- M_NINN: W=1e-06 L=1.8000000000000002e-07 m=1.0 ID=4.49e-06 gm/Id=15.701559020044543 region=saturation VGS=0.336 VDS=0.473 LUT_row=10266
- M_PLOADP: W=9.544781332754442e-07 L=3.0000000000000004e-07 m=1.0 ID=-4.49e-06 gm/Id=8.68596881959911 region=saturation VGS=-0.42 VDS=-0.503 LUT_row=14077
- M_PLOADN: W=9.544781332754442e-07 L=3.0000000000000004e-07 m=1.0 ID=-4.49e-06 gm/Id=8.68596881959911 region=saturation VGS=-0.42 VDS=-0.503 LUT_row=14077

## Final Device Sizing
- M_NINP: W=1e-06 L=1.8000000000000002e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\nmos_50nm_nominal_27C_full.npz
- M_NINN: W=1e-06 L=1.8000000000000002e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\nmos_50nm_nominal_27C_full.npz
- M_PLOADP: W=9.544781332754442e-07 L=3.0000000000000004e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\pmos_50nm_nominal_27C_full.npz
- M_PLOADN: W=9.544781332754442e-07 L=3.0000000000000004e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\pmos_50nm_nominal_27C_full.npz

## Measurements
- output_common_mode_v: 0.4970555007457733
- output_balance_error_v: 0.0
- tail_current_a: 8.975978744274471e-06
- branch_current_a: 4.4879893721372355e-06
- average_power_w: 8.976630851975642e-06
- differential_gain_vv: -25.587393831023693
- differential_gain_db: 28.16052107339466
- ac_midband_gain_db: 28.160683588375832
- bandwidth_hz: 2151091.2464885674
- ugb_hz: 55136704.54654229
- phase_at_ugb_deg: 91.80404430422611
- phase_margin_deg: 88.19595569577388
- transient_differential_gain_vv: -23.391219661998928
- transient_differential_gain_db: 27.38105734654313

## Reproducibility
Use the listed project-local netlists with the model library path above. Copy final W/L/m, VIN_CM, VBP, VDD and CL from this report.
