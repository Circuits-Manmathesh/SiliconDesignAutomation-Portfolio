"""Public skeleton for inverter testbench construction."""


def build_public_inverter_tests(spec: dict) -> list[str]:
    return ["dc_vtc", "ac_gain_phase", "transient_delay_power"]
