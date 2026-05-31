# inverter_3GHz_clock_TT27 Results

Final status: PASS

## Rerun
Run from `C:\SiliconDesignAutomation`:

```bat
.venv\Scripts\activate
python master_product_runner.py --spec Projects\inverter_3GHz_clock_TT27\spec\inverter_3GHz_clock_TT27.yml
```

## Open First
Open `plots/final/inverter_characterization_dashboard.png`, then `reports/final_summary.txt`.

## Key Files
- Final summary: `reports/final_summary.txt`
- DC report: `reports/dc_operating_point_report.txt`
- DC characterization report: `reports/dc_characterization_report.txt`
- AC report: `reports/ac_small_signal_report.txt`
- Transient report: `reports/transient_verification_report.txt`
- Best design CSV: `results/best_design.csv`
- Best netlist: `generated_netlists/best/best_inverter.sp`
- Final dashboard: `plots/final/final_summary_dashboard.png`
- Characterization dashboard: `plots/final/inverter_characterization_dashboard.png`

## Result Folders
- DC evidence: `results/dc`, `generated_netlists/dc`, `plots/dc`
- AC evidence: `results/ac`, `generated_netlists/ac`, `plots/ac`
- Transient evidence: `results/tran`, `generated_netlists/tran`, `plots/tran`

## Manual LTspice Verification
Open or batch-run the generated netlists under `generated_netlists/dc`, `generated_netlists/ac`, and `generated_netlists/tran/candidates`.
