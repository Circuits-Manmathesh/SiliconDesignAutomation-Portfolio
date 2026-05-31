# Final Design Report

Project: demo_common_source_amplifier
Topology: common_source_amplifier
Status: PASS
Model library: C:\Skynet_Setup\skynet_analog_agent\technology_models\models.lib
LUT root: C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut

## Reproducible Device Bias and Sizing Summary
- VDD: 1
- VIN_CM: 0.36
- VBP: 0.62
- CL: 1p
- M_NCS: W=1.27546944407973e-06 L=1.8000000000000002e-07 m=1.0 ID=9.29e-06 gm/Id=13.778256189451021 region=saturation VGS=0.36 VDS=0.549 LUT_row=10378
- M_PLOAD: W=3.483678155334179e-06 L=4e-07 m=1.0 ID=-9.29e-06 gm/Id=10.118406889128094 region=saturation VGS=-0.38 VDS=-0.451 LUT_row=16539

## Final Device Sizing
- M_NCS: W=1.27546944407973e-06 L=1.8000000000000002e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\nmos_50nm_nominal_27C_full.npz
- M_PLOAD: W=3.483678155334179e-06 L=4e-07 m=1.0 LUT=C:\Skynet_Setup\skynet_analog_agent\lut_characterizer\generated_lut\pmos_50nm_nominal_27C_full.npz

## Measurements
- output_bias_v: 0.5494044423103333
- bias_current_a: 9.288323781220242e-06
- average_power_w: 9.288323781220242e-06
- dc_gain_vv: 24.90687370300291
- dc_gain_db: 27.92638437108979
- output_swing_low_v: 0.016366181895136833
- output_swing_high_v: 0.9999420046806335
- ac_midband_gain_db: 27.928936302874774
- bandwidth_hz: 807537.0808647823
- ugb_hz: 20152032.71852511
- phase_at_ugb_deg: 92.15083657259552
- phase_margin_deg: 87.8491634274045
- slew_rate_v_per_s: 1563820.7876552779
- settling_time_1pct_s: 9.1215e-09

## Reproducibility
Use the listed project-local netlists with the model library path above. Copy final W/L/m, VIN_CM, VBP, VDD and CL from this report.
