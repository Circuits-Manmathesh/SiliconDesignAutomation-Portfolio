# Automation Flow

The private framework is designed around a one-command project flow:

```bash
python master_product_runner.py --spec Projects/<project>/spec/<project>.yml
```

The public repository includes a sanitized runner skeleton that shows orchestration boundaries without exposing private execution logic.

## Conceptual Flow

```text
spec → strategy selection → LUT query → candidate generation → SPICE → measurement → correction → final report
```

## Flow Stages

1. Parse the project specification.
2. Select a design strategy from `design_type`.
3. Query gm/Id LUT intelligence for feasible operating regions.
4. Generate candidate sizing options.
5. Build simulator testbenches.
6. Run DC, AC, and transient verification.
7. Measure results against the specification.
8. Correct sizing or bias choices if needed.
9. Emit a final evidence package.

