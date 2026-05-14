"""Public skeleton for sizing optimization."""


def rank_public_candidates(candidates: list[dict]) -> list[dict]:
    return sorted(candidates, key=lambda item: item.get("public_score", 0), reverse=True)
