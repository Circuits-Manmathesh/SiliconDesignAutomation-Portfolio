"""Public skeleton for operating-region checks."""


def check_region_summary(candidate: dict) -> dict[str, str]:
    return {"status": "reviewable", "detail": "sanitized region summary only"}
