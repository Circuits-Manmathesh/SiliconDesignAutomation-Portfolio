"""Public skeleton for the SiliconDesignAutomation product runner."""


class PublicProductRunner:
    """Coordinates a sanitized spec-to-evidence demo flow."""

    def run(self, spec_path: str) -> dict[str, str]:
        return {
            "spec": spec_path,
            "status": "public skeleton only",
            "scope": "private implementation omitted",
        }
