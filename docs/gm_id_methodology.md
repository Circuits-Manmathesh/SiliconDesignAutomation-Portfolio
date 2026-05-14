# gm/Id Methodology

gm/Id is treated as a transistor design API. Instead of starting with arbitrary widths, the flow reasons about operating region, inversion level, current density, gain, speed, and capacitance before emitting device dimensions.

## Width Is Output, Not Input

In the private framework, width is a sizing result. The optimizer chooses a target operating region and current density, then computes the required width from current demand and normalized device data.

## Id/W For Width Sizing

The LUT stores drain-current density as Id/W. Once the required branch current is known, the tool can estimate width from:

```text
W = Id_required / (Id/W)
```

This keeps sizing tied to physics instead of hard-coded trial widths.

## gm/gds For Intrinsic Gain

gm/gds is used as an intrinsic gain indicator. Candidate operating points with insufficient intrinsic gain can be filtered before expensive verification.

## ft And gm/Cgg For Speed

Transition frequency and gm/Cgg are used as speed indicators. They help reject candidates that cannot support the required edge rate, bandwidth, or clock frequency.

## Cgg/W For Loading

Cgg/W estimates input capacitance per unit width. It lets the framework reason about load presented to a previous stage and avoid passing timing by creating an unacceptable input load.

## Saturation Margin And Region Filtering

Operation-region filtering is mandatory for analog-aware automation. Candidates are checked for saturation margin, bias consistency, and region validity before they are promoted into full verification.

